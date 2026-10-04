import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { Phone } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHero, Section } from "@/components/site/Section";
import { businessQuery } from "@/lib/business";
import { pageMeta } from "@/lib/seo";

export const Route = createFileRoute("/_site/accessibility")({
  head: () => pageMeta("Accessibility — JC's Towing", "Accessibility information and contact pathway for the JC's Towing website.", "/accessibility"),
  component: Accessibility,
});

function Accessibility() {
  const { data: b } = useSuspenseQuery(businessQuery);
  return (
    <>
      <PageHero eyebrow="Accessibility" title="Website accessibility" />
      <Section>
        <div className="max-w-3xl space-y-5 text-lg">
          <p>JC's Towing aims to keep this website usable on phones, tablets, desktops, keyboards, and assistive technologies.</p>
          <p>If you have difficulty using a page or form, call us and describe what you need. We can discuss the request directly.</p>
          <Button asChild variant="hero" size="xl"><a href={`tel:${b.phone_e164}`}><Phone /> Call {b.phone}</a></Button>
        </div>
      </Section>
    </>
  );
}
