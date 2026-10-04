import { createFileRoute, Link } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { ArrowRight, ClipboardList, MapPin, Phone, Truck, CheckCircle2, MessageSquare, Navigation, CarFront, Route as RouteIcon, Settings2, BookOpen } from "lucide-react";
import heroImg from "@/assets/hero-tow.jpg";
import { Button } from "@/components/ui/button";
import { BrandLogo } from "@/components/brand/BrandLogo";
import { Section, SectionTitle } from "@/components/site/Section";
import { ServiceCards } from "@/components/site/ServiceCards";
import { VerifiedTrustStrip } from "@/components/site/VerifiedTrustStrip";
import { SafeFaq } from "@/components/site/SafeFaq";
import { businessQuery } from "@/lib/business";
import { pageMeta } from "@/lib/seo";
import { trackJctEvent } from "@/lib/analytics";

export const Route = createFileRoute("/_site/")({
  head: () => pageMeta("JC's Towing — Lockport, IL | (815) 474-7384", "Contact JC's Towing in Lockport, Illinois about towing. Call (815) 474-7384 or send a service request online."),
  component: Home,
});

const details = [
  { icon: MapPin, label: "Your current location", hint: "Address, intersection, or nearest landmark" },
  { icon: CarFront, label: "Vehicle details", hint: "Year, make, and model if you know them" },
  { icon: RouteIcon, label: "Destination", hint: "Where you need the vehicle to go" },
  { icon: Settings2, label: "Vehicle condition", hint: "Does it roll, steer, and shift?" },
  { icon: Navigation, label: "Scene access", hint: "Parking, clearance, or other access issues" },
];

function Home() {
  const { data: b } = useSuspenseQuery(businessQuery);
  return (
    <>
      <section className="relative isolate overflow-hidden bg-ink text-ink-foreground">
        <img src={heroImg} alt="Tow truck with warning lights on a wet road" width={1920} height={1088} fetchPriority="high" className="hero-photo absolute inset-0 -z-20 h-full w-full object-cover object-center" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-ink via-ink/85 to-ink/35" aria-hidden />
        <div className="mx-auto max-w-7xl px-4 py-14 sm:py-20 lg:py-24">
          <BrandLogo size="lg" logoUrl={b.logo_url} showTagline />
          <div className="mt-10 h-1 w-20 bg-primary" aria-hidden />
          <h1 className="mt-5 max-w-3xl font-display text-5xl font-black uppercase leading-[0.96] sm:text-6xl lg:text-7xl">JC's Towing.<br /><span className="text-chrome">A clear next step.</span></h1>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-silver">Based in {b.city}, {b.state}. Need a tow? Tell us where you are and what happened. We'll confirm the details directly.</p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button asChild variant="hero" size="xl" className="min-w-52"><a href={`tel:${b.phone_e164}`} onClick={() => trackJctEvent("call_click", { placement: "home_hero" })}><Phone /> Call {b.phone}</a></Button>
            <Button asChild variant="chrome" size="xl"><Link to="/contact" onClick={() => trackJctEvent("request_service_click", { placement: "home_hero" })}><ClipboardList /> Request Service</Link></Button>
          </div>
        </div>
        <div className="stripe-red h-2" aria-hidden />
      </section>

      <VerifiedTrustStrip b={b} />

      <section className="bg-ink text-ink-foreground">
        <div className="mx-auto max-w-7xl px-4 py-12 md:py-16">
          <div className="flex flex-wrap items-end justify-between gap-5">
            <div><p className="font-display text-sm font-bold uppercase text-primary">When you reach out</p><h2 className="mt-2 font-display text-3xl font-extrabold uppercase md:text-4xl">Have these details ready</h2></div>
            <p className="max-w-sm text-silver">Share what you know. If you're unsure about a detail, we can talk it through.</p>
          </div>
          <ul className="mt-8 grid gap-px bg-sidebar-border sm:grid-cols-2 lg:grid-cols-5">
            {details.map(({ icon: Icon, label, hint }, i) => <li key={label} className="bg-ink p-5"><div className="flex items-center justify-between"><Icon className="h-6 w-6 text-primary" aria-hidden /><span className="font-display text-sm text-silver">0{i + 1}</span></div><h3 className="mt-5 font-display text-xl font-bold uppercase">{label}</h3><p className="mt-2 text-sm text-silver">{hint}</p></li>)}
          </ul>
        </div>
      </section>

      <Section>
        <SectionTitle sub="Only currently listed services appear here. Call to confirm the details of your request.">Services</SectionTitle>
        <ServiceCards b={b} />
        <Button asChild variant="link" className="mt-7 px-0 text-base"><Link to="/services">See services <ArrowRight aria-hidden /></Link></Button>
      </Section>

      <Section tone="muted">
        <SectionTitle>How it works</SectionTitle>
        <ol className="grid gap-6 md:grid-cols-3">
          {[
            { title: "Call or request", body: "Call us directly or send your location and vehicle details through the form.", icon: Phone },
            { title: "Confirm details", body: "We'll discuss your situation and confirm what service, if any, is available.", icon: MessageSquare },
            { title: "Agree on next steps", body: "We'll confirm the next step directly with you. A form submission alone does not arrange dispatch.", icon: CheckCircle2 },
          ].map(({ title, body, icon: Icon }, i) => <li key={title} className="border-t-4 border-primary pt-5"><div className="flex items-center justify-between"><Icon className="h-7 w-7 text-primary" aria-hidden /><span className="font-display text-5xl font-black text-border">0{i + 1}</span></div><h3 className="mt-6 font-display text-2xl font-bold uppercase">{title}</h3><p className="mt-2 max-w-sm text-muted-foreground">{body}</p></li>)}
        </ol>
      </Section>

      <Section>
        <div className="grid gap-10 lg:grid-cols-2 lg:gap-20">
          <div><p className="font-display text-sm font-bold uppercase text-primary">Why JC's Towing</p><h2 className="mt-2 font-display text-4xl font-extrabold uppercase">A direct line when you need it.</h2><p className="mt-5 max-w-xl text-lg text-muted-foreground">Reach JC's Towing at the number below. Tell us what you need and we'll discuss the next step with you directly.</p><Button asChild variant="inverse" size="xl" className="mt-7"><a href={`tel:${b.phone_e164}`} onClick={() => trackJctEvent("call_click", { placement: "home_why" })}><Phone /> Call {b.phone}</a></Button></div>
          <div className="grid gap-4 self-center sm:grid-cols-2">{[{ icon: Phone, title: "Direct contact", text: "Call and speak about your situation." }, { icon: MapPin, title: "Lockport identity", text: `JC's Towing is based in ${b.city}, ${b.state}.` }].map(({icon: Icon, title, text}) => <div key={title} className="border-l-4 border-primary bg-muted p-6"><Icon className="h-7 w-7 text-primary" aria-hidden /><h3 className="mt-5 font-display text-xl font-bold uppercase">{title}</h3><p className="mt-2 text-muted-foreground">{text}</p></div>)}</div>
        </div>
      </Section>

      <Section tone="dark">
        <div className="grid items-center gap-8 md:grid-cols-2">
          <div><p className="flex items-center gap-2 font-display text-sm font-bold uppercase text-primary"><MapPin className="h-4 w-4" /> Service area</p><h2 className="mt-3 font-display text-4xl font-extrabold uppercase">Based in {b.city}, {b.state}</h2><p className="mt-4 text-silver">{b.service_areas.filter((c) => c && c.toLowerCase() !== "lockport").length ? `Also listed: ${b.service_areas.filter((c) => c && c.toLowerCase() !== "lockport").join(" · ")}. ` : ""}Call to confirm we can reach your location.</p></div>
          <div className="md:text-right"><Button asChild variant="chrome" size="xl"><Link to="/service-area">View service area <ArrowRight /></Link></Button></div>
        </div>
      </Section>

      {b.services.commercial && <Section tone="muted"><div className="flex flex-col justify-between gap-6 md:flex-row md:items-center"><div><p className="font-display text-sm font-bold uppercase text-primary">Commercial / fleet</p><h2 className="mt-2 font-display text-3xl font-extrabold uppercase">Let's discuss your business needs.</h2><p className="mt-2 text-muted-foreground">Shops, fleets, and local businesses can get in touch about towing requests.</p></div><Button asChild variant="inverse" size="xl"><Link to="/commercial"><Truck /> Commercial inquiry</Link></Button></div></Section>}

      <Section>
        <div className="grid gap-10 lg:grid-cols-[1fr_1.2fr]">
          <div>
            <p className="font-display text-sm font-bold uppercase text-primary">Questions</p>
            <h2 className="mt-2 font-display text-4xl font-extrabold uppercase">Quick answers before you call.</h2>
            <p className="mt-4 text-muted-foreground">The exact service, availability, ETA, and price are confirmed directly.</p>
          </div>
          <SafeFaq />
        </div>
      </Section>

      <Section tone="muted">
        <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
          <div><p className="font-display text-sm font-bold uppercase text-primary">Resources</p><h2 className="mt-2 font-display text-3xl font-extrabold uppercase">Accident or breakdown?</h2><p className="mt-2 text-muted-foreground">Use the short checklists to gather the details you may need.</p></div>
          <Button asChild variant="inverse" size="xl"><Link to="/resources"><BookOpen /> View checklists</Link></Button>
        </div>
      </Section>

      <Section><div className="flex flex-col justify-between gap-6 md:flex-row md:items-center"><div><p className="font-display text-sm font-bold uppercase text-primary">Feedback</p><h2 className="mt-2 font-display text-3xl font-extrabold uppercase">Your experience matters.</h2><p className="mt-2 text-muted-foreground">No customer reviews are displayed here without verification.</p></div><Button asChild variant="outline" size="xl"><Link to="/reviews">Reviews & feedback <ArrowRight /></Link></Button></div></Section>

      <section className="bg-asphalt text-ink-foreground"><div className="mx-auto max-w-7xl px-4 py-14 md:py-20"><p className="font-display text-sm font-bold uppercase text-primary">Need a tow?</p><h2 className="mt-3 font-display text-4xl font-black uppercase sm:text-5xl">Start with a call.</h2><p className="mt-3 text-silver">For urgent needs, calling is the quickest way to connect.</p><div className="mt-7 flex flex-col gap-3 sm:flex-row"><Button asChild variant="hero" size="xl"><a href={`tel:${b.phone_e164}`} onClick={() => trackJctEvent("call_click", { placement: "home_final" })}><Phone /> Call {b.phone}</a></Button><Button asChild variant="chrome" size="xl"><Link to="/contact" onClick={() => trackJctEvent("request_service_click", { placement: "home_final" })}>Request Service</Link></Button></div></div></section>
    </>
  );
}
