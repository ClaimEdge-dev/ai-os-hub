import { createFileRoute } from "@tanstack/react-router";
import { PageHero, Section } from "@/components/site/Section";
import { pageMeta } from "@/lib/seo";

export const Route = createFileRoute("/_site/privacy")({
  head: () => pageMeta("Privacy — JC's Towing", "Privacy information for the JC's Towing website and service-request form.", "/privacy"),
  component: Privacy,
});

function Privacy() {
  return (
    <>
      <PageHero eyebrow="Privacy" title="Privacy information" />
      <Section>
        <div className="prose max-w-3xl space-y-6">
          <section><h2 className="font-display text-2xl font-bold uppercase">Information you provide</h2><p>When you submit a service request, the site may collect the contact, location, vehicle, service, and note information you choose to provide.</p></section>
          <section><h2 className="font-display text-2xl font-bold uppercase">How it is used</h2><p>Information submitted through the service-request form is used to review and respond to that request and to support related business records.</p></section>
          <section><h2 className="font-display text-2xl font-bold uppercase">Location and photos</h2><p>If optional location sharing or photo upload features are enabled later, they should activate only when you choose to use them. Location permission should not be requested automatically.</p></section>
          <section><h2 className="font-display text-2xl font-bold uppercase">No payment collection</h2><p>The current website service-request form does not collect payment information.</p></section>
          <section><h2 className="font-display text-2xl font-bold uppercase">Questions</h2><p>For questions about information submitted through this website, contact JC's Towing using the phone number shown on the site.</p></section>
        </div>
      </Section>
    </>
  );
}
