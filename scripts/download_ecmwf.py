"""
Download the latest ECMWF IFS surface forecast from ECMWF Open Data,
convert to Zarr with chunking suitable for titiler-xarray tile serving.

Chunking strategy:
  time=1  — each step is a separate S3 chunk (critical for tile server perf)
  lat/lon — 100x100 (matches existing Zarr convention)

Usage:
  conda run -n metd python scripts/download_ecmwf.py
"""

from pathlib import Path
import numpy as np
import xarray as xr
from ecmwf.opendata import Client

DATA_DIR = Path(__file__).parent.parent / "data"
GRIB_DIR = DATA_DIR / "grib"
ZARR_PATH = DATA_DIR / "ecmwf_surface.zarr"
GRIB_DIR.mkdir(parents=True, exist_ok=True)

# Forecast steps to download (hours): 0–120 in 6h steps + key longer steps
STEPS = list(range(0, 121, 6))

# Surface parameters: GRIB shortName → friendly name in output Zarr
PARAMS = {
    "2t":   "t2m",    # 2m temperature (K)
    "10u":  "u10",    # 10m U wind component (m/s)
    "10v":  "v10",    # 10m V wind component (m/s)
    "tp":   "tp",     # total precipitation (m, accumulated)
    "msl":  "msl",    # mean sea level pressure (Pa)
    "ssrd": "ssrd",   # surface solar radiation downwards (J/m², accumulated)
}

client = Client(source="ecmwf")


def download_param(shortname: str) -> Path:
    target = GRIB_DIR / f"{shortname}.grib2"
    if target.exists():
        print(f"  {shortname}: already downloaded, skipping")
        return target
    print(f"  {shortname}: downloading …")
    client.retrieve(
        type="fc",
        param=shortname,
        step=STEPS,
        target=str(target),
    )
    return target


def open_grib(path: Path, shortname: str) -> xr.DataArray:
    ds = xr.open_dataset(
        str(path),
        engine="cfgrib",
        backend_kwargs={"indexpath": ""},
    )
    # cfgrib exposes the variable under its cf name; grab the first data var
    var = list(ds.data_vars)[0]
    da = ds[var]
    # Rename step→time if needed so all datasets share the same dim name
    if "step" in da.dims and "valid_time" in da.coords:
        da = da.swap_dims({"step": "valid_time"}).rename({"valid_time": "time"})
    elif "time" not in da.dims and "valid_time" in da.coords:
        da = da.assign_coords(time=da.valid_time).expand_dims("time")
    da.name = PARAMS[shortname]
    return da


def main():
    print("=== Downloading ECMWF Open Data surface forecast ===")
    arrays = {}
    for shortname in PARAMS:
        grib_path = download_param(shortname)
        print(f"  {shortname}: opening …")
        arrays[PARAMS[shortname]] = open_grib(grib_path, shortname)

    print("\n=== Building dataset ===")
    ds = xr.Dataset(arrays)

    # Rename lat/lon to standard names if cfgrib used 'latitude'/'longitude'
    rename = {}
    if "latitude" in ds.dims:
        rename["latitude"] = "lat"
    if "longitude" in ds.dims:
        rename["longitude"] = "lon"
    if rename:
        ds = ds.rename(rename)

    # Convert units to human-friendly values
    if "t2m" in ds:
        ds["t2m"] = ds["t2m"] - 273.15
        ds["t2m"].attrs["units"] = "degC"
        ds["t2m"].attrs["long_name"] = "2m Temperature"

    if "tp" in ds:
        ds["tp"] = ds["tp"] * 1000  # m → mm
        ds["tp"].attrs["units"] = "mm"
        ds["tp"].attrs["long_name"] = "Total Precipitation"

    # Derive wind speed and direction
    if "u10" in ds and "v10" in ds:
        ds["wind_speed"] = np.sqrt(ds["u10"] ** 2 + ds["v10"] ** 2)
        ds["wind_speed"].attrs["units"] = "m/s"
        ds["wind_speed"].attrs["long_name"] = "10m Wind Speed"

        ds["wind_dir"] = (np.arctan2(ds["u10"], ds["v10"]) * 180 / np.pi) % 360
        ds["wind_dir"].attrs["units"] = "degrees"
        ds["wind_dir"].attrs["long_name"] = "10m Wind Direction (meteorological)"

    print(ds)

    print("\n=== Writing Zarr ===")
    print(f"  target: {ZARR_PATH}")
    # Chunk: time=1 so each forecast step is a separate S3 chunk (critical for tile server).
    # Spatial 100x100 matches existing convention; fits within typical tile read area.
    chunk_lat = min(100, ds.sizes.get("lat", 100))
    chunk_lon = min(100, ds.sizes.get("lon", 100))
    ds_chunked = ds.chunk({"time": 1, "lat": chunk_lat, "lon": chunk_lon})

    ds_chunked.to_zarr(str(ZARR_PATH), mode="w", consolidated=True)
    print(f"  done — {ds.sizes['time']} time steps, "
          f"{ds.sizes.get('lat')}×{ds.sizes.get('lon')} grid")
    print(f"\nTime range: {ds.time.values[0]}  →  {ds.time.values[-1]}")
    print(f"Variables:  {list(ds.data_vars)}")


if __name__ == "__main__":
    main()
