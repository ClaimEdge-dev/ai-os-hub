import { MapPin, Phone, ShieldCheck } from "lucide-react";
import type { BusinessTruth } from "@/lib/business";

export function VerifiedTrustStrip({ b }: { b: BusinessTruth }) {
  return (
    <section aria-label="Verified business information" className="border-y border-sidebar-border bg-ink text-ink-foreground">
      <div className="mx-auto grid max-w-7xl gap-px bg-sidebar-border sm:grid-cols-3">
        <a href={`tel:${b.phone_e164}`} className="flex min-h-20 items-center gap-3 bg-ink px-5 py-4 hover:bg-sidebar-accent">
          <Phone className="h-5 w-5 text-primary" aria-hidden />
          <span><strong className="block font-display uppercase">Call JC's Towing</strong><span className="text-sm text-silver">{b.phone}</span></span>
        </a>
        <div className="flex min-h-20 items-center gap-3 bg-ink px-5 py-4">
          <MapPin className="h-5 w-5 text-primary" aria-hidden />
          <span><strong className="block font-display uppercase">Based in</strong><span className="text-sm text-silver">{b.city}, {b.state}</span></span>
        </div>
        <div className="flex min-h-20 items-center gap-3 bg-ink px-5 py-4">
          <ShieldCheck className="h-5 w-5 text-primary" aria-hidden />
          <span><strong className="block font-display uppercase">Clear next step</strong><span className="text-sm text-silver">Service details are confirmed directly.</span></span>
        </div>
      </div>
    </section>
  );
}
