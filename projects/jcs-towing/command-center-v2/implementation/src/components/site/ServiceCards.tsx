import { Link } from "@tanstack/react-router";
import { Car, LifeBuoy, Truck, Building2, ArrowRight } from "lucide-react";
import { SERVICE_CATALOG, type BusinessTruth } from "@/lib/business";

const ICONS = { towing: Truck, roadside: LifeBuoy, transport: Car, commercial: Building2 } as const;

export function ServiceCards({ b }: { b: BusinessTruth }) {
  const visible = SERVICE_CATALOG.filter((s) => b.services[s.key]);
  if (!visible.length) return <p className="text-muted-foreground">Call us to discuss what you need.</p>;

  return (
    <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {visible.map((s) => {
        const Icon = ICONS[s.key];
        const inner = (
          <>
            <div className="flex h-12 w-12 -skew-x-6 items-center justify-center bg-ink text-silver">
              <Icon className="h-6 w-6" aria-hidden />
            </div>
            <h3 className="mt-6 font-display text-2xl font-bold uppercase">{s.title}</h3>
            <p className="mt-2 text-muted-foreground">{s.blurb}</p>
            {s.key === "towing" && <span className="mt-5 inline-flex items-center gap-2 font-semibold">Towing details <ArrowRight className="h-4 w-4" /></span>}
          </>
        );

        return (
          <li key={s.key} className="service-tile relative overflow-hidden border border-border border-t-4 border-t-primary bg-card shadow-sm">
            {s.key === "towing"
              ? <Link to="/services/towing" className="block h-full p-6">{inner}</Link>
              : <div className="h-full p-6">{inner}</div>}
          </li>
        );
      })}
    </ul>
  );
}
