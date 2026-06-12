import { describe, it, expect } from "vitest"
import { NAV_LINKS, isActiveLink } from "../nav"

describe("NAV_LINKS", () => {
  it("every link has a non-empty label and an absolute path href", () => {
    for (const link of NAV_LINKS) {
      expect(link.label.length).toBeGreaterThan(0)
      expect(link.href.startsWith("/")).toBe(true)
    }
  })

  it("includes the dashboard home link", () => {
    expect(NAV_LINKS.some(l => l.href === "/")).toBe(true)
  })

  it("has no duplicate hrefs or labels", () => {
    const hrefs = NAV_LINKS.map(l => l.href)
    const labels = NAV_LINKS.map(l => l.label)
    expect(new Set(hrefs).size).toBe(hrefs.length)
    expect(new Set(labels).size).toBe(labels.length)
  })
})

describe("isActiveLink", () => {
  it("matches the home link only on the exact root path", () => {
    expect(isActiveLink("/", "/")).toBe(true)
    expect(isActiveLink("/sources", "/")).toBe(false)
    expect(isActiveLink("/anything", "/")).toBe(false)
  })

  it("matches a non-home link on its path and sub-paths", () => {
    expect(isActiveLink("/sources", "/sources")).toBe(true)
    expect(isActiveLink("/sources/detail", "/sources")).toBe(true)
  })

  it("does not match an unrelated path", () => {
    expect(isActiveLink("/", "/sources")).toBe(false)
    expect(isActiveLink("/about", "/sources")).toBe(false)
  })
})
