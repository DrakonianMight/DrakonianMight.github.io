export interface NavLink {
  href: string
  label: string
}

export const NAV_LINKS: NavLink[] = [
  { href: "/", label: "Dashboard" },
  { href: "/sources", label: "Data Sources" },
]

/**
 * Whether a nav link should be shown as active for the current path.
 * The home link ("/") only matches exactly; other links match any
 * sub-path (e.g. "/sources" is active on "/sources/anything").
 */
export function isActiveLink(pathname: string, href: string): boolean {
  return href === "/" ? pathname === "/" : pathname.startsWith(href)
}
