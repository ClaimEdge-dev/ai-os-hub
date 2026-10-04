import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

const FAQ = [
  {
    q: "What should I have ready when I call?",
    a: "Your current location or nearest landmark, vehicle year/make/model if known, where the vehicle needs to go, and anything unusual about access or the vehicle condition.",
  },
  {
    q: "Does submitting the website form mean a truck is dispatched?",
    a: "No. A website request does not guarantee dispatch, availability, ETA, or price. JC's Towing confirms service details directly.",
  },
  {
    q: "What if I am not sure which service I need?",
    a: "Choose “Other / not sure” on the request form or call directly. Describe what happened and the vehicle condition.",
  },
  {
    q: "How do I know whether my location can be reached?",
    a: "JC's Towing is based in Lockport, Illinois. Call to confirm service at your specific location.",
  },
  {
    q: "Should I include vehicle condition details?",
    a: "Yes. If you know whether the vehicle rolls, steers, shifts, has keys available, or has wheel or access problems, share that information when requesting service.",
  },
] as const;

export function SafeFaq() {
  return (
    <Accordion type="single" collapsible className="w-full">
      {FAQ.map((item, i) => (
        <AccordionItem key={item.q} value={`faq-${i}`}>
          <AccordionTrigger className="text-left font-display text-lg font-bold uppercase">{item.q}</AccordionTrigger>
          <AccordionContent className="text-base leading-relaxed text-muted-foreground">{item.a}</AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
