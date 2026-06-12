import { describe, it, expect } from "vitest"
import { SOURCE_SECTIONS } from "../sources"

const allSources = SOURCE_SECTIONS.flatMap(s => s.sources)

describe("SOURCE_SECTIONS", () => {
  it("has at least one section, each with a heading, blurb, and sources", () => {
    expect(SOURCE_SECTIONS.length).toBeGreaterThan(0)
    for (const section of SOURCE_SECTIONS) {
      expect(section.heading.length).toBeGreaterThan(0)
      expect(section.blurb.length).toBeGreaterThan(0)
      expect(section.sources.length).toBeGreaterThan(0)
    }
  })

  it("every source has a non-empty name, detail, and an https href", () => {
    for (const source of allSources) {
      expect(source.name.length).toBeGreaterThan(0)
      expect(source.detail.length).toBeGreaterThan(0)
      expect(source.href).toMatch(/^https:\/\/.+/)
    }
  })

  it("has no duplicate source names", () => {
    const names = allSources.map(s => s.name)
    expect(new Set(names).size).toBe(names.length)
  })

  it("attributes the core providers used by the app", () => {
    const names = allSources.map(s => s.name).join(" | ")
    for (const provider of ["Open-Meteo", "OpenStreetMap", "MapLibre", "RainViewer", "NASA GIBS"]) {
      expect(names).toContain(provider)
    }
  })
})
