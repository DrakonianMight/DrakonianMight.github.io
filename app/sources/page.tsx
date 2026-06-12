import type { Metadata } from "next"
import { SOURCE_SECTIONS } from "@/lib/sources"

export const metadata: Metadata = {
  title: "Data Sources — Droplet",
  description:
    "The forecast models, observation feeds, map tiles, and open-source software that power Droplet, with attribution.",
}

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
          {SOURCE_SECTIONS.map((section) => (
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
