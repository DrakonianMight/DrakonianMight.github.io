"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

interface NavLink {
  href: string
  label: string
}

const NAV_LINKS: NavLink[] = [
  { href: "/", label: "Dashboard" },
  { href: "/sources", label: "Data Sources" },
]

export function SiteNav() {
  const pathname = usePathname()

  return (
    <nav className="fixed left-1/2 top-4 z-50 -translate-x-1/2">
      <div className="flex items-center gap-1 rounded-lg border border-border bg-card/95 p-1 shadow-md backdrop-blur-sm">
        {NAV_LINKS.map(({ href, label }) => {
          const isActive = href === "/" ? pathname === "/" : pathname.startsWith(href)
          return (
            <Link
              key={href}
              href={href}
              className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-accent text-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
              }`}
            >
              {label}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
