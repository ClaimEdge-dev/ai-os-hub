import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { Phone } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHero, Section, SectionTitle } from "@/components/site/Section";
import { businessQuery } from "@/lib/business";
import { pageMeta } from "@/lib/seo";

export const Route = createFileRoute("/_site/resources/accident-checklist")({
  head: () => pageMeta("After an Accident Checklist — JC's Towing", "A practical post-accident checklist from JC's Towing in Lockport, Illinois.", "/resources/accident-checklist"),
  component: AccidentChecklist,
});

function AccidentChecklist() {
  const { data: b } = useSuspenseQuery(businessQuery);
  const steps = [
    "If it can be done safely, move out of active traffic and turn on hazard lights.",
    "If anyone may be injured or the scene is unsafe, contact emergency services.",
    "Note your location, nearest intersection, roadway, or visible landmark.",
    "Photograph the vehicles and scene only if doing so is safe and lawful.",
    "Have your vehicle year, make, model, and intended destination ready.",
    "Tell the towing company about wheel damage, blocked access, missing keys, or other conditions that may affect loading.",
  ];
  return (
    <>
      <PageHero eyebrow="Checklist" title="After an accident">Safety comes first. This checklist is general information, not emergency or legal advice.</PageHero>
      <Section>
        <SectionTitle>What to gather</SectionTitle>
        <ol className="grid gap-4">
          {steps.map((s,i)=><li key={s} className="flex gap-4 border-l-4 border-primary bg-muted p-5"><span className="font-display text-2xl font-black text-primary">{String(i+1).padStart(2,"0")}</span><p>{s}</p></li>)}
        </ol>
        <Button asChild variant="hero" size="xl" className="mt-8"><a href={`tel:${b.phone_e164}`}><Phone /> Call {b.phone}</a></Button>
      </Section>
    </>
  );
}
