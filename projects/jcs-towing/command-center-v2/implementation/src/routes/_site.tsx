import { createFileRoute, Link, Outlet } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { Menu, Phone, X } from "lucide-react";
import { BrandLogo } from "@/components/brand/BrandLogo";
import { Button } from "@/components/ui/button";
import { businessQuery, type BusinessTruth } from "@/lib/business";
import { trackJctEvent } from "@/lib/analytics";
import { captureAttribution } from "@/lib/attribution";

export const Route = createFileRoute("/_site")({
  loader: ({ context }) => context.queryClient.ensureQueryData(businessQuery),
  component: SiteLayout,
  errorComponent: () => (
    <div className="p-10 text-center">
      Something went wrong loading this page. Please call{" "}
      <a className="font-bold text-primary underline" href="tel:+18154747384">(815) 474-7384</a>.
    </div>
  ),
});

const NAV = [
  { to: "/services", label: "Services" },
  { to: "/service-area", label: "Service Area" },
  { to: "/reviews", label: "Reviews" },
  { to: "/resources", label: "Resources" },
  { to: "/about", label: "About" },
] as const;

function structuredData(b: BusinessTruth) {
  const data: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "TowingService",
    name: b.name,
    telephone: b.phone_e164,
    url: `https://${b.domain}`,
    areaServed: b.service_areas.map((c) => ({ "@type": "City", name: `${c}, ${b.state}` })),
    address: { "@type": "PostalAddress", addressLocality: b.city, addressRegion: b.state, addressCountry: "US" },
  };
  if (b.email) data["email"] = b.email;
  return JSON.stringify(data);
}

function SiteLayout() {
  const { data: b } = useSuspenseQuery(businessQuery);
  const [open, setOpen] = useState(false);
  const nav = b.services.commercial ? [...NAV.slice(0, 2), { to: "/commercial" as const, label: "Commercial" }, ...NAV.slice(2)] : NAV;

  useEffect(() => {
    captureAttribution();
  }, []);

  return (
    <div className="flex min-h-screen flex-col bg-background pb-20 md:pb-0">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: structuredData(b) }} />
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:bg-primary focus:p-3 focus:text-primary-foreground">Skip to content</a>

      <header className="sticky top-0 z-40 border-b border-sidebar-border bg-ink text-ink-foreground">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
          <Link to="/" aria-label="JC's Towing home" onClick={() => setOpen(false)}><BrandLogo size="sm" logoUrl={b.logo_url} /></Link>
          <nav aria-label="Main" className="hidden items-center gap-1 lg:flex">
            {nav.map((n) => <Link key={n.to} to={n.to} className="px-3 py-2 font-display text-sm font-semibold uppercase tracking-wider text-silver hover:text-ink-foreground" activeProps={{ className: "text-primary" }}>{n.label}</Link>)}
          </nav>
          <div className="flex items-center gap-2">
            <Button asChild variant="hero" className="hidden sm:inline-flex">
              <a href={`tel:${b.phone_e164}`} onClick={() => trackJctEvent("call_click", { placement: "header" })}><Phone /> {b.phone}</a>
            </Button>
            <Button asChild variant="chrome" className="hidden md:inline-flex">
              <Link to="/contact" onClick={() => trackJctEvent("request_service_click", { placement: "header" })}>Request Service</Link>
            </Button>
            <Button variant="ghost" size="icon" className="h-11 w-11 text-ink-foreground lg:hidden" aria-label={open ? "Close menu" : "Open menu"} aria-expanded={open} onClick={() => setOpen(!open)}>
              {open ? <X /> : <Menu />}
            </Button>
          </div>
        </div>
        <div className="slash-divider" aria-hidden />
        {open && (
          <nav aria-label="Mobile" className="border-t border-sidebar-border px-4 py-3 lg:hidden">
            {[...nav, { to: "/contact", label: "Request Service" } as const].map((n) => <Link key={n.to} to={n.to} onClick={() => setOpen(false)} className="block py-3 font-display text-lg font-semibold uppercase tracking-wider text-silver">{n.label}</Link>)}
          </nav>
        )}
      </header>

      <main id="main" className="flex-1"><Outlet /></main>

      <footer className="bg-ink text-silver">
        <div className="slash-divider" aria-hidden />
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-12 md:grid-cols-3">
          <div><BrandLogo size="md" logoUrl={b.logo_url} showTagline />{b.tagline && <p className="mt-4 font-display text-lg italic text-ink-foreground">{b.tagline}</p>}</div>
          <div>
            <h2 className="font-display text-sm font-bold uppercase tracking-widest text-primary">Contact</h2>
            <p className="mt-3"><a className="text-xl font-bold text-ink-foreground hover:text-primary" href={`tel:${b.phone_e164}`} onClick={() => trackJctEvent("call_click", { placement: "footer" })}>{b.phone}</a></p>
            <p className="mt-1">{b.city}, {b.state}</p>
            {b.show_hours && b.hours && <p className="mt-1 whitespace-pre-line">{b.hours}</p>}
            {b.email && <p className="mt-1"><a href={`mailto:${b.email}`} className="underline">{b.email}</a></p>}
          </div>
          <div>
            <h2 className="font-display text-sm font-bold uppercase tracking-widest text-primary">Pages</h2>
            <ul className="mt-3 grid grid-cols-2 gap-2">
              {nav.map((n) => <li key={n.to}><Link to={n.to} className="hover:text-ink-foreground">{n.label}</Link></li>)}
              <li><Link to="/contact" className="hover:text-ink-foreground">Request Service</Link></li>
              <li><Link to="/privacy" className="hover:text-ink-foreground">Privacy</Link></li>
              <li><Link to="/accessibility" className="hover:text-ink-foreground">Accessibility</Link></li>
              <li><Link to="/auth" className="hover:text-ink-foreground">Staff</Link></li>
            </ul>
          </div>
        </div>
        <p className="border-t border-sidebar-border py-4 text-center text-xs">© {new Date().getFullYear()} {b.name} — {b.city}, {b.state}</p>
      </footer>

      <div className="fixed inset-x-0 bottom-0 z-50 grid grid-cols-2 gap-2 border-t-4 border-primary bg-ink p-2 md:hidden">
        <Button asChild variant="hero" size="xl" className="w-full">
          <a href={`tel:${b.phone_e164}`} aria-label={`Call JC's Towing at ${b.phone}`} onClick={() => trackJctEvent("call_click", { placement: "mobile_bar" })}><Phone /> Call Now</a>
        </Button>
        <Button asChild variant="chrome" size="xl" className="w-full">
          <Link to="/contact" onClick={() => trackJctEvent("request_service_click", { placement: "mobile_bar" })}>Request</Link>
        </Button>
      </div>
    </div>
  );
}
