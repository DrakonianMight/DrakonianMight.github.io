export interface Source {
  name: string
  href: string
  detail: string
}

export interface SourceSection {
  heading: string
  blurb: string
  sources: Source[]
}

export const SOURCE_SECTIONS: SourceSection[] = [
  {
    heading: "Forecast & observation data",
    blurb:
      "All point forecasts, ensembles, marine and satellite-radiation data are served through the Open-Meteo API, which aggregates the national weather services listed below.",
    sources: [
      {
        name: "Open-Meteo",
        href: "https://open-meteo.com/",
        detail:
          "Forecast, ensemble, marine and satellite-radiation APIs. Data licensed under CC BY 4.0.",
      },
    ],
  },
  {
    heading: "Numerical weather prediction models",
    blurb:
      "Deterministic and ensemble guidance is drawn from the following global models, accessed via Open-Meteo.",
    sources: [
      { name: "ECMWF IFS & AIFS", href: "https://www.ecmwf.int/", detail: "European Centre for Medium-Range Weather Forecasts — physics-based and AI forecast models." },
      { name: "NOAA GFS & GEFS", href: "https://www.noaa.gov/", detail: "US National Oceanic and Atmospheric Administration — Global Forecast System and its ensemble." },
      { name: "DWD ICON & ICON-EPS", href: "https://www.dwd.de/", detail: "Deutscher Wetterdienst — German Weather Service global model and ensemble." },
      { name: "ECMWF WAM & GFS Wave", href: "https://www.ecmwf.int/", detail: "Wave Action Model (ECMWF) and NOAA GFS Wave — maritime wave and swell forecasts." },
    ],
  },
  {
    heading: "Maps & basemaps",
    blurb: "Interactive maps are rendered with MapLibre GL using the following basemap styles.",
    sources: [
      { name: "CARTO", href: "https://carto.com/attribution/", detail: "Positron and Dark Matter basemap styles." },
      { name: "OpenFreeMap", href: "https://openfreemap.org/", detail: "Liberty basemap style, served from open data." },
      { name: "OpenStreetMap contributors", href: "https://www.openstreetmap.org/copyright", detail: "Underlying basemap data, © OpenStreetMap contributors, licensed under the ODbL." },
      { name: "MapLibre GL", href: "https://maplibre.org/", detail: "Open-source library used to render the interactive maps." },
    ],
  },
  {
    heading: "Weather overlays",
    blurb: "Animated map overlays come from the following providers.",
    sources: [
      { name: "RainViewer", href: "https://www.rainviewer.com/", detail: "Precipitation radar tiles." },
      { name: "NASA GIBS / EOSDIS", href: "https://earthdata.nasa.gov/", detail: "MODIS Terra true-colour satellite imagery via the Global Imagery Browse Services." },
    ],
  },
]
