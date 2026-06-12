import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Data Sources — Droplet",
  description:
    "The forecast models, observation feeds, map tiles, and open-source software that power Droplet, with attribution.",
}

interface Source {
  name: string
  href: string
  detail: string
}

interface Section {
  heading: string
  blurb: string
  sources: Source[]
}

const SECTIONS: Section[] = [
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

export default function SourcesPage() {
  return (
    <main className="min-h-screen bg-background px-6 pb-20 pt-24 text-foreground">
      <div className="mx-auto max-w-3xl">
        <h1 className="text-3xl font-semibold tracking-tight">Data sources & attribution</h1>
        <p className="mt-3 text-muted-foreground">
          Droplet is built on open data and open-source software. The forecasts, observations, and
          map layers shown here are provided by the organisations and projects below — full credit
          to them.
        </p>

        <div className="mt-10 space-y-10">
          {SECTIONS.map((section) => (
            <section key={section.heading}>
              <h2 className="text-xl font-semibold">{section.heading}</h2>
              <p className="mt-1 text-sm text-muted-foreground">{section.blurb}</p>
              <ul className="mt-4 space-y-3">
                {section.sources.map((source) => (
                  <li
                    key={source.name}
                    className="rounded-lg border border-border bg-card p-4"
                  >
                    <a
                      href={source.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-foreground underline-offset-4 hover:underline"
                    >
                      {source.name}
                    </a>
                    <p className="mt-1 text-sm text-muted-foreground">{source.detail}</p>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>

        <p className="mt-12 border-t border-border pt-6 text-xs text-muted-foreground">
          Droplet is a non-commercial visualisation project. Where a provider requires attribution,
          it is given above; please refer to each provider&rsquo;s own terms for reuse of their data.
        </p>
      </div>
    </main>
  )
}
