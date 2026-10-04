import { createFileRoute, Link } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { Phone, ClipboardList, MapPin, CarFront, Route as RouteIcon, Settings2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHero, Section, SectionTitle } from "@/components/site/Section";
import { SafeFaq } from "@/components/site/SafeFaq";
import { VerifiedTrustStrip } from "@/components/site/VerifiedTrustStrip";
import { businessQuery } from "@/lib/business";
import { pageMeta } from "@/lib/seo";

export const Route = createFileRoute("/_site/services/towing")({
  head: () => pageMeta(
    "Towing in Lockport, IL — JC's Towing",
    "Contact JC's Towing in Lockport, Illinois about towing. Call (815) 474-7384 or request service online.",
    "/services/towing",
  ),
  component: TowingPage,
});

function TowingPage() {
  const { data: b } = useSuspenseQuery(businessQuery);

  return (
    <>
      <PageHero eyebrow="Towing" title="Need a tow? Start with the details.">
        Call JC's Towing or send a service request. We'll confirm the next step directly.
      </PageHero>

      <VerifiedTrustStrip b={b} />

      <Section>
        <div className="grid gap-10 lg:grid-cols-[1.1fr_.9fr]">
          <div>
            <SectionTitle sub="Sharing a few details up front helps us understand the situation.">Before you call or request</SectionTitle>
            <ul className="grid gap-4">
              {[
                [MapPin, "Your location", "Address, intersection, or nearest landmark."],
                [CarFront, "Your vehicle", "Year, make, and model if you know them."],
                [RouteIcon, "Where it needs to go", "Destination, if known."],
                [Settings2, "Vehicle condition", "Whether it rolls, steers, shifts, has keys, or has access issues."],
              ].map(([Icon, title, body]) => {
                const I = Icon as typeof MapPin;
                return <li key={String(title)} className="flex gap-4 border-l-4 border-primary bg-muted p-5"><I className="mt-1 h-5 w-5 shrink-0 text-primary" aria-hidden /><div><h3 className="font-display text-xl font-bold uppercase">{String(title)}</h3><p className="mt-1 text-muted-foreground">{String(body)}</p></div></li>;
              })}
            </ul>
          </div>
          <aside className="self-start border border-border bg-card p-6 shadow-sm">
            <h2 className="font-display text-3xl font-extrabold uppercase">Contact JC's Towing</h2>
            <p className="mt-3 text-muted-foreground">Based in {b.city}, {b.state}. Call to discuss your towing request and location.</p>
            <Button asChild variant="hero" size="xl" className="mt-6 w-full"><a href={`tel:${b.phone_e164}`}><Phone /> Call {b.phone}</a></Button>
            <Button asChild variant="inverse" size="xl" className="mt-3 w-full"><Link to="/contact"><ClipboardList /> Request Service</Link></Button>
            <p className="mt-4 text-xs text-muted-foreground">Website requests do not guarantee dispatch, availability, ETA, or price.</p>
          </aside>
        </div>
      </Section>

      <Section tone="muted">
        <SectionTitle>Common questions</SectionTitle>
        <SafeFaq />
      </Section>
    </>
  );
}
