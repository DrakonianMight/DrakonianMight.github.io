# Droplet

An interactive maritime and weather forecast dashboard, built with Next.js, MapLibre GL, and
Recharts. It visualises point forecasts, ensembles, marine/wave data, and satellite observations
from [Open-Meteo](https://open-meteo.com/), and is deployed as a static site to GitHub Pages at
**[drakonianmight.github.io](https://drakonianmight.github.io/)**.

> This repository was migrated from the original OceanView Jekyll site. The previous data-fetching
> scripts are preserved under [`legacy/`](legacy/).

## Features

- **Forecast themes** — Weather, Renewables, Maritime, and Risk, each with a tailored parameter set
- **Multi-model** — overlay deterministic models (ECMWF IFS/AIFS, GFS, DWD ICON) and ensembles
  (ECMWF, GEFS, ICON EPS) as spaghetti plots
- **Maritime** — wave/swell forecasts via the Open-Meteo Marine API (ECMWF WAM, GFS Wave)
- **Interactive map** — click anywhere or pick a city; radar and satellite overlays
- **Data Sources page** — full attribution of every forecast, model, basemap, and overlay provider

## Getting started

```bash
npm install
npm run dev        # http://localhost:3000
```

## Commands

```bash
npm run dev        # Development server
npm run build      # Static export to out/
npm run lint       # ESLint
npm test           # Run test suite (vitest)
npm run test:watch # Watch mode
npm run test:coverage
```

## Project structure

```
app/               Next.js App Router
  page.tsx           Dashboard (/)
  sources/page.tsx   Data Sources & attribution (/sources)
  layout.tsx         Root layout — mounts the site nav
components/         React components
  site-nav.tsx       Floating top-center navigation bar
  weather-*.tsx      Dashboard, map, and chart
  ui/                shadcn/ui primitives
lib/               Logic and data
  weather-api.ts     Open-Meteo fetching and processing
  weather-types.ts   Models, themes, parameters
  nav.ts             Nav links + active-link logic
  sources.ts         Data-source attribution content
  __tests__/         Vitest unit tests
legacy/            Original OceanView data scripts (archived)
.github/workflows/ deploy.yml — build + deploy to GitHub Pages
```

## Adding a page

1. Create `app/<name>/page.tsx`.
2. Add `{ href: "/<name>", label: "..." }` to `NAV_LINKS` in [`lib/nav.ts`](lib/nav.ts) — it appears
   in the nav automatically.

## Deployment

Pushing to `master` triggers [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which
runs `npm ci && npm run build` and publishes the `out/` export via GitHub Pages.

> **One-time setup:** in the repository **Settings → Pages → Source**, select **GitHub Actions**.
> This replaces the default Jekyll build with the workflow above.

The site is a static export (`output: 'export'` in [`next.config.mjs`](next.config.mjs)); because it
is served from the root of a user Pages site, no `basePath` is required.

## Data & attribution

Forecasts come from Open-Meteo (CC BY 4.0); maps use CARTO, OpenFreeMap, and OpenStreetMap data via
MapLibre GL; overlays come from RainViewer and NASA GIBS. See the in-app
[Data Sources page](https://drakonianmight.github.io/sources) for full credits.
