import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { useServerFn } from "@tanstack/react-start";
import { useRef, useState, type FormEvent } from "react";
import { CheckCircle2, Phone, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { PageHero, Section } from "@/components/site/Section";
import { GetMyLocationButton } from "@/components/site/GetMyLocationButton";
import { businessQuery, SERVICE_CATALOG } from "@/lib/business";
import { leadSchema, submitServiceRequest } from "@/lib/business.functions";
import { pageMeta } from "@/lib/seo";
import { trackJctEvent } from "@/lib/analytics";

export const Route = createFileRoute("/_site/contact")({
  head: () => pageMeta("Request Towing Service — JC's Towing, Lockport IL", "Send a towing request to JC's Towing in Lockport, IL. Service details are confirmed directly; call (815) 474-7384 for urgent needs.", "/contact"),
  component: Contact,
});

type Errors = Partial<Record<string, string>>;

function Contact() {
  const { data: b } = useSuspenseQuery(businessQuery);
  const submit = useServerFn(submitServiceRequest);
  const pickupRef = useRef<HTMLInputElement>(null);
  const [errors, setErrors] = useState<Errors>({});
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState<number | null>(null);
  const [failure, setFailure] = useState<string | null>(null);
  const [consent, setConsent] = useState(false);
  const services = SERVICE_CATALOG.filter((s) => b.services[s.key]);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setFailure(null);
    trackJctEvent("request_form_submit");
    const f = new FormData(e.currentTarget);
    const raw = {
      name: String(f.get("name") ?? ""),
      phone: String(f.get("phone") ?? ""),
      email: String(f.get("email") ?? ""),
      pickup: String(f.get("pickup") ?? ""),
      destination: String(f.get("destination") ?? ""),
      vehicle_year: String(f.get("vehicle_year") ?? ""),
      vehicle_make: String(f.get("vehicle_make") ?? ""),
      vehicle_model: String(f.get("vehicle_model") ?? ""),
      service: String(f.get("service") ?? ""),
      drivable: (String(f.get("drivable") ?? "") || undefined) as "yes" | "no" | "unsure" | undefined,
      notes: String(f.get("notes") ?? ""),
      consent,
    };
    const parsed = leadSchema.safeParse(raw);
    if (!parsed.success) {
      const errs: Errors = {};
      for (const i of parsed.error.issues) errs[String(i.path[0])] = i.message;
      setErrors(errs);
      trackJctEvent("request_form_error", { error_count: parsed.error.issues.length });
      return;
    }
    setErrors({});
    setBusy(true);
    try {
      const res = await submit({ data: parsed.data });
      if (res.ok) {
        setDone(res.reference);
        trackJctEvent("request_form_success");
      } else {
        setFailure(res.error);
        trackJctEvent("request_form_error", { server: true });
      }
    } catch {
      setFailure("We couldn't submit your request. Please call us.");
      trackJctEvent("request_form_error", { exception: true });
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <PageHero eyebrow="Request Service" title="Tell us what you need">
        In a hurry? Calling is fastest: <a className="font-bold text-ink-foreground underline" href={`tel:${b.phone_e164}`} onClick={() => trackJctEvent("call_click", { placement: "request_hero" })}>{b.phone}</a>
      </PageHero>
      <Section>
        {done !== null ? (
          <div role="status" aria-live="polite" className="mx-auto max-w-xl border-2 border-ink bg-card p-8 text-center shadow-[8px_8px_0_0_var(--color-primary)]">
            <CheckCircle2 className="mx-auto h-14 w-14 text-success" aria-hidden />
            <h2 className="mt-4 font-display text-3xl font-extrabold italic uppercase">Request received</h2>
            <p className="mt-2 text-muted-foreground">Reference #{done}. We'll reach out using the phone number you gave us.</p>
            <p className="mt-3 text-sm text-muted-foreground">Your request does not guarantee dispatch, availability, ETA, or price. JC's Towing will confirm service details directly.</p>
            <p className="mt-4">If it's urgent, call now:</p>
            <Button asChild variant="hero" size="xl" className="mt-3"><a href={`tel:${b.phone_e164}`} onClick={() => trackJctEvent("call_click", { placement: "request_success" })}><Phone /> {b.phone}</a></Button>
          </div>
        ) : (
          <form onSubmit={onSubmit} onFocus={() => trackJctEvent("request_form_start")} noValidate className="mx-auto grid max-w-3xl gap-6 md:grid-cols-2">
            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">01 / Contact</h2>
            <Field id="name" label="Your name" required error={errors.name}><Input id="name" name="name" autoComplete="name" className="h-12" /></Field>
            <Field id="phone" label="Phone" required error={errors.phone}><Input id="phone" name="phone" type="tel" autoComplete="tel" className="h-12" /></Field>
            <Field id="email" label="Email (optional)" error={errors.email} className="md:col-span-2"><Input id="email" name="email" type="email" autoComplete="email" className="h-12" /></Field>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">02 / Location</h2>
            <Field id="pickup" label="Pickup location — address, intersection, landmark, or shared coordinates" required error={errors.pickup} className="md:col-span-2">
              <Input ref={pickupRef} id="pickup" name="pickup" placeholder="Address, intersection, or landmark" className="h-12" />
            </Field>
            <div className="md:col-span-2">
              <GetMyLocationButton onLocation={({lat,lng,accuracy}) => {
                if (pickupRef.current) pickupRef.current.value = `${lat.toFixed(6)}, ${lng.toFixed(6)} (±${Math.round(accuracy)}m)`;
              }} />
              <p className="mt-2 text-xs text-muted-foreground">Location is requested only when you tap the button. You can always enter the location manually.</p>
            </div>
            <Field id="destination" label="Destination (optional)" className="md:col-span-2"><Input id="destination" name="destination" className="h-12" /></Field>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">03 / Vehicle</h2>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3 md:col-span-2">
              <Field id="vehicle_year" label="Year"><Input id="vehicle_year" name="vehicle_year" inputMode="numeric" className="h-12" /></Field>
              <Field id="vehicle_make" label="Make"><Input id="vehicle_make" name="vehicle_make" className="h-12" /></Field>
              <Field id="vehicle_model" label="Model"><Input id="vehicle_model" name="vehicle_model" className="h-12" /></Field>
            </div>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">04 / Need</h2>
            <Field id="service" label="Service needed">
              <select id="service" name="service" onChange={(e) => trackJctEvent("service_selected", { service: e.currentTarget.value })} className="h-12 w-full rounded-md border border-input bg-background px-3">
                <option value="Other / not sure">Other / not sure</option>
                {services.map((s) => <option key={s.key} value={s.title}>{s.title}</option>)}
              </select>
            </Field>
            <fieldset className="space-y-2">
              <legend className="text-sm font-medium">Is the vehicle drivable?</legend>
              <div className="flex gap-4">
                {["yes", "no", "unsure"].map((v) => (
                  <label key={v} className="flex min-h-11 items-center gap-2 capitalize">
                    <input type="radio" name="drivable" value={v} className="h-5 w-5 accent-[var(--color-primary)]" /> {v === "unsure" ? "Not sure" : v}
                  </label>
                ))}
              </div>
            </fieldset>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">05 / Notes</h2>
            <Field id="notes" label="Access issues or anything else we should know?" className="md:col-span-2"><Textarea id="notes" name="notes" rows={4} maxLength={2000} /></Field>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">06 / Consent</h2>
            <div className="md:col-span-2">
              <label className="flex items-start gap-3">
                <Checkbox checked={consent} onCheckedChange={(v) => setConsent(v === true)} className="mt-1 h-5 w-5" aria-describedby="consent-err" />
                <span className="text-sm">I agree that {b.name} may contact me by phone, text, or email about this request.</span>
              </label>
              {errors.consent && <p id="consent-err" className="mt-1 text-sm text-destructive">{errors.consent}</p>}
            </div>
            {failure && <p role="alert" className="md:col-span-2 border-l-4 border-destructive bg-destructive/10 p-3 text-sm">{failure} <a className="font-bold underline" href={`tel:${b.phone_e164}`}>{b.phone}</a></p>}
            <div className="md:col-span-2">
              <p className="mb-4 border-l-4 border-primary bg-muted p-4 text-sm">Submitting this form does not guarantee dispatch, availability, ETA, or price. JC's Towing will confirm service details directly.</p>
              <Button type="submit" variant="hero" size="xl" disabled={busy} className="w-full md:w-auto">
                {busy && <Loader2 className="animate-spin" />} Send request
              </Button>
              <p className="mt-2 text-xs text-muted-foreground">No payment is collected online.</p>
            </div>
          </form>
        )}
      </Section>
    </>
  );
}

function Field({ id, label, required, error, className, children }: { id: string; label: string; required?: boolean; error?: string; className?: string; children: React.ReactNode }) {
  return (
    <div className={className}>
      <Label htmlFor={id} className="mb-1.5 block">{label}{required && <span className="text-primary"> *</span>}</Label>
      {children}
      {error && <p className="mt-1 text-sm text-destructive" role="alert">{error}</p>}
    </div>
  );
}
