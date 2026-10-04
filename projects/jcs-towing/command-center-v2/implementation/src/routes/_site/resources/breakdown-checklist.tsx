import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { Phone } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHero, Section, SectionTitle } from "@/components/site/Section";
import { businessQuery } from "@/lib/business";
import { pageMeta } from "@/lib/seo";

export const Route = createFileRoute("/_site/resources/breakdown-checklist")({
  head: () => pageMeta("Vehicle Breakdown Checklist — JC's Towing", "A practical breakdown checklist from JC's Towing in Lockport, Illinois.", "/resources/breakdown-checklist"),
  component: BreakdownChecklist,
});

function BreakdownChecklist() {
  const { data: b } = useSuspenseQuery(businessQuery);
  const steps = [
    "If possible and safe, get the vehicle out of active traffic and turn on hazard lights.",
    "Stay aware of traffic and avoid standing in a dangerous lane or blind spot.",
    "Note your exact location, nearest intersection, exit, mile marker, or landmark.",
    "Have the vehicle year, make, and model ready if you know them.",
    "Know where you want the vehicle taken, if possible.",
    "Tell the towing company whether the vehicle rolls, steers, shifts, has keys, or has damaged wheels or restricted access.",
  ];
  return (
    <>
      <PageHero eyebrow="Checklist" title="Vehicle breakdown">A few details can make the towing request easier to understand.</PageHero>
      <Section>
        <SectionTitle>Before requesting a tow</SectionTitle>
        <ol className="grid gap-4">
          {steps.map((s,i)=><li key={s} className="flex gap-4 border-l-4 border-primary bg-muted p-5"><span className="font-display text-2xl font-black text-primary">{String(i+1).padStart(2,"0")}</span><p>{s}</p></li>)}
        </ol>
        <Button asChild variant="hero" size="xl" className="mt-8"><a href={`tel:${b.phone_e164}`}><Phone /> Call {b.phone}</a></Button>
      </Section>
    </>
  );
}
