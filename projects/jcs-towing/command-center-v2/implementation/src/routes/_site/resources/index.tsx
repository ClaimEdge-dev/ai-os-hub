import { createFileRoute, Link } from "@tanstack/react-router";
import { AlertTriangle, Wrench, ArrowRight } from "lucide-react";
import { PageHero, Section, SectionTitle } from "@/components/site/Section";
import { pageMeta } from "@/lib/seo";

export const Route = createFileRoute("/_site/resources/")({
  head: () => pageMeta("Towing Resources — JC's Towing", "Simple towing and breakdown checklists from JC's Towing in Lockport, Illinois.", "/resources"),
  component: Resources,
});

function Resources() {
  const cards = [
    { to: "/resources/accident-checklist", icon: AlertTriangle, title: "After an accident", body: "A simple checklist for documenting the scene and preparing to request help." },
    { to: "/resources/breakdown-checklist", icon: Wrench, title: "Vehicle breakdown", body: "Basic steps for getting to a safer position and gathering the details needed for a tow request." },
  ] as const;
  return (
    <>
      <PageHero eyebrow="Resources" title="Know what to do next">Short, practical checklists. No filler.</PageHero>
      <Section>
        <SectionTitle>Guides</SectionTitle>
        <div className="grid gap-5 md:grid-cols-2">
          {cards.map(({to,icon:Icon,title,body}) => (
            <Link key={to} to={to} className="service-tile block border border-border border-t-4 border-t-primary bg-card p-6">
              <Icon className="h-7 w-7 text-primary" aria-hidden />
              <h2 className="mt-5 font-display text-2xl font-bold uppercase">{title}</h2>
              <p className="mt-2 text-muted-foreground">{body}</p>
              <span className="mt-5 inline-flex items-center gap-2 font-semibold">Read checklist <ArrowRight className="h-4 w-4" /></span>
            </Link>
          ))}
        </div>
      </Section>
    </>
  );
}
