import { Link } from "@tanstack/react-router";
import { Phone } from "lucide-react";

export function BrandedNotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-ink px-4 text-ink-foreground">
      <div className="max-w-xl text-center">
        <p className="font-display text-sm font-bold uppercase tracking-[.3em] text-primary">JC's Towing</p>
        <h1 className="mt-3 font-display text-7xl font-black">404</h1>
        <h2 className="mt-3 font-display text-3xl font-bold uppercase">Wrong page. Clear next step.</h2>
        <p className="mt-4 text-silver">The page moved or does not exist. Go back to the site or call JC's Towing.</p>
        <div className="mt-7 flex flex-col justify-center gap-3 sm:flex-row">
          <a href="tel:+18154747384" className="inline-flex min-h-12 items-center justify-center gap-2 bg-primary px-6 font-display font-bold uppercase text-white"><Phone className="h-5 w-5" /> (815) 474-7384</a>
          <Link to="/" className="inline-flex min-h-12 items-center justify-center border border-silver px-6 font-display font-bold uppercase">Back home</Link>
        </div>
      </div>
    </main>
  );
}
