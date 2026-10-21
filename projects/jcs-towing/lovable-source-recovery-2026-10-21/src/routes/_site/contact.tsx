import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { useServerFn } from "@tanstack/react-start";
import { useEffect, useState, type FormEvent } from "react";
import { CheckCircle2, Phone, Loader2, MapPin, Camera, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { PageHero, Section } from "@/components/site/Section";
import { businessQuery, SERVICE_CATALOG } from "@/lib/business";
import { leadSchema, submitServiceRequest } from "@/lib/business.functions";
import { collectAttribution, rememberLanding } from "@/lib/attribution";
import { photoError, PHOTO_MAX_COUNT, PHOTO_TYPES } from "@/lib/lead-schema";
import { uploadLeadPhotos, type PhotoResult } from "@/lib/lead-photos";
import { supabase } from "@/integrations/supabase/client";
import { pageMeta } from "@/lib/seo";

export const Route = createFileRoute("/_site/contact")({
  head: () => pageMeta("Request Towing Service — JC's Towing, Lockport IL", "Send a towing request to JC's Towing in Lockport, IL. Service details are confirmed directly; call (815) 474-7384 for urgent needs.", "/contact"),
  component: Contact,
});

type Errors = Partial<Record<string, string>>;
type Done = { reference: number; leadId: string; uploadBucket: string; uploadPrefix: string };
type Geo = { lat: number; lng: number; acc: number } | null;

const NO_GUARANTEE = "Submitting this form does not guarantee dispatch, availability, ETA, or price. JC's Towing will confirm service details directly.";
const CONDITIONS = [
  ["rolls", "Does it roll?"], ["steers", "Does it steer?"], ["shifts", "Does it shift into neutral?"], ["keys_available", "Keys available?"],
  ["accident", "Was there an accident?"], ["wheel_damage", "Wheel or tire damage?"], ["clearance_issue", "Low clearance / tight access?"],
] as const;

function Contact() {
  const { data: b } = useSuspenseQuery(businessQuery);
  const submit = useServerFn(submitServiceRequest);
  const [errors, setErrors] = useState<Errors>({});
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState<Done | null>(null);
  const [failure, setFailure] = useState<string | null>(null);
  const [consent, setConsent] = useState(false);
  const [geo, setGeo] = useState<Geo>(null);
  const [geoMsg, setGeoMsg] = useState<string | null>(null);
  const services = SERVICE_CATALOG.filter((s) => b.services[s.key]);

  useEffect(() => { rememberLanding(); }, []);

  function useLocation() {
    if (!("geolocation" in navigator)) { setGeoMsg("Location isn't available on this device. Please type the pickup location."); return; }
    setGeoMsg("Getting your location…");
    navigator.geolocation.getCurrentPosition(
      (p) => { setGeo({ lat: p.coords.latitude, lng: p.coords.longitude, acc: Math.round(p.coords.accuracy) }); setGeoMsg(null); },
      () => setGeoMsg("We couldn't get your location. Please type the pickup location."),
      { enableHighAccuracy: true, timeout: 15000 },
    );
  }

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setFailure(null);
    const f = new FormData(e.currentTarget);
    const s = (k: string) => String(f.get(k) ?? "");
    const o = (k: string) => (s(k) || undefined) as never;
    const raw = {
      name: s("name"), phone: s("phone"), email: s("email"), pickup: s("pickup"), destination: s("destination"),
      vehicle_year: s("vehicle_year"), vehicle_make: s("vehicle_make"), vehicle_model: s("vehicle_model"), vehicle_type: s("vehicle_type"),
      service: s("service"), drivable: o("drivable"), preferred_contact_method: o("preferred_contact_method"),
      ...Object.fromEntries(CONDITIONS.map(([k]) => [k, o(k)])),
      access_notes: s("access_notes"), notes: s("notes"),
      ...(geo ? { geolocation_lat: geo.lat, geolocation_lng: geo.lng, geolocation_accuracy_m: geo.acc } : {}),
      consent,
    };
    const parsed = leadSchema.safeParse(raw);
    if (!parsed.success) {
      const errs: Errors = {};
      for (const i of parsed.error.issues) errs[String(i.path[0])] = i.message;
      setErrors(errs);
      return;
    }
    setErrors({});
    setBusy(true);
    try {
      const res = await submit({ data: { lead: parsed.data, attribution: collectAttribution() } });
      if (res.ok) { setDone(res); window.scrollTo({ top: 0 }); }
      else setFailure(res.error);
    } catch {
      setFailure("We couldn't submit your request. Please call us.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <PageHero eyebrow="Request Service" title="Tell us what you need">
        In a hurry? Calling is fastest: <a className="font-bold text-ink-foreground underline" href={`tel:${b.phone_e164}`}>{b.phone}</a>
      </PageHero>
      <Section>
        {done ? (
          <div role="status" aria-live="polite" className="mx-auto max-w-xl border-2 border-ink bg-card p-6 text-center shadow-[8px_8px_0_0_var(--color-primary)] sm:p-8">
            <CheckCircle2 className="mx-auto h-14 w-14 text-success" aria-hidden />
            <h2 className="mt-4 font-display text-3xl font-extrabold italic uppercase">Request received</h2>
            <p className="mt-2 text-muted-foreground">Reference #{done.reference}. We'll reach out using the contact details you gave us.</p>
            <p className="mt-3 text-sm text-muted-foreground">{NO_GUARANTEE}</p>
            <PhotoUploader done={done} phone={b.phone} phoneE164={b.phone_e164} />
            <p className="mt-6">If it's urgent, call now:</p>
            <Button asChild variant="hero" size="xl" className="mt-3"><a href={`tel:${b.phone_e164}`}><Phone /> {b.phone}</a></Button>
          </div>
        ) : (
          <form onSubmit={onSubmit} noValidate className="mx-auto grid max-w-3xl gap-6 md:grid-cols-2">
            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">01 / Contact</h2>
            <Field id="name" label="Your name" required error={errors.name}><Input id="name" name="name" autoComplete="name" className="h-12" /></Field>
            <Field id="phone" label="Phone" required error={errors.phone}><Input id="phone" name="phone" type="tel" autoComplete="tel" className="h-12" /></Field>
            <Field id="email" label="Email (optional)" error={errors.email}><Input id="email" name="email" type="email" autoComplete="email" className="h-12" /></Field>
            <Choice name="preferred_contact_method" legend="Best way to reach you" options={[["phone", "Call"], ["text", "Text"], ["email", "Email"]]} defaultValue="phone" />

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">02 / Location</h2>
            <Field id="pickup" label="Pickup location — address, intersection, or landmark" required error={errors.pickup} className="md:col-span-2"><Input id="pickup" name="pickup" placeholder="Address, intersection, or landmark" className="h-12" /></Field>
            <div className="md:col-span-2">
              <Button type="button" variant="outline" onClick={useLocation} className="min-h-11"><MapPin /> {geo ? "Update my location" : "Use my location"}</Button>
              <p className="mt-1 text-xs text-muted-foreground" aria-live="polite">
                {geoMsg ?? (geo ? `Location shared (accurate to about ${geo.acc} m). Please still describe the pickup above.` : "Optional. Shares your phone's GPS point with this request only.")}
              </p>
            </div>
            <Field id="destination" label="Destination (optional)" className="md:col-span-2"><Input id="destination" name="destination" className="h-12" /></Field>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">03 / Vehicle</h2>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 md:col-span-2 lg:grid-cols-4">
              <Field id="vehicle_year" label="Year"><Input id="vehicle_year" name="vehicle_year" inputMode="numeric" className="h-12" /></Field>
              <Field id="vehicle_make" label="Make"><Input id="vehicle_make" name="vehicle_make" className="h-12" /></Field>
              <Field id="vehicle_model" label="Model"><Input id="vehicle_model" name="vehicle_model" className="h-12" /></Field>
              <Field id="vehicle_type" label="Type">
                <select id="vehicle_type" name="vehicle_type" className="h-12 w-full rounded-md border border-input bg-background px-3">
                  <option value="">Not sure</option>
                  {["Car", "SUV / Crossover", "Pickup truck", "Van", "Motorcycle", "Other"].map((v) => <option key={v}>{v}</option>)}
                </select>
              </Field>
            </div>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">04 / Need &amp; condition</h2>
            <Field id="service" label="Service needed">
              <select id="service" name="service" className="h-12 w-full rounded-md border border-input bg-background px-3">
                <option value="Other / not sure">Other / not sure</option>
                {services.map((s) => <option key={s.key} value={s.title}>{s.title}</option>)}
              </select>
            </Field>
            <Choice name="drivable" legend="Is the vehicle drivable?" options={TRI} />
            {CONDITIONS.map(([k, l]) => <Choice key={k} name={k} legend={l} options={TRI} />)}

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">05 / Notes</h2>
            <Field id="access_notes" label="Access details (parking garage, gate, height limit…)" className="md:col-span-2"><Textarea id="access_notes" name="access_notes" rows={2} maxLength={1000} /></Field>
            <Field id="notes" label="Anything else we should know?" className="md:col-span-2"><Textarea id="notes" name="notes" rows={3} maxLength={2000} /></Field>
            <p className="text-sm text-muted-foreground md:col-span-2"><Camera className="mr-1 inline h-4 w-4" aria-hidden />You can add up to {PHOTO_MAX_COUNT} photos after you send the request.</p>

            <h2 className="border-b border-border pb-2 font-display text-2xl font-bold uppercase md:col-span-2">06 / Consent</h2>
            <div className="md:col-span-2">
              <label className="flex items-start gap-3">
                <Checkbox checked={consent} onCheckedChange={(v) => setConsent(v === true)} className="mt-1 h-5 w-5" aria-describedby="consent-err" />
                <span className="text-sm">I agree that {b.name} may contact me by phone, text, or email about this request.</span>
              </label>
              {errors.consent && <p id="consent-err" className="mt-1 text-sm text-destructive">{errors.consent}</p>}
            </div>
            {failure && <p role="alert" className="border-l-4 border-destructive bg-destructive/10 p-3 text-sm md:col-span-2">{failure} <a className="font-bold underline" href={`tel:${b.phone_e164}`}>{b.phone}</a></p>}
            <div className="md:col-span-2">
              <p className="mb-4 border-l-4 border-primary bg-muted p-4 text-sm">{NO_GUARANTEE}</p>
              <Button type="submit" variant="hero" size="xl" disabled={busy} className="w-full md:w-auto">
                {busy ? <><Loader2 className="animate-spin" /> Sending…</> : "Send request"}
              </Button>
              <p className="mt-2 text-xs text-muted-foreground">No payment is collected online.</p>
            </div>
          </form>
        )}
      </Section>
    </>
  );
}

const TRI: [string, string][] = [["yes", "Yes"], ["no", "No"], ["unsure", "Not sure"]];

function PhotoUploader({ done, phone, phoneE164 }: { done: Done; phone: string; phoneE164: string }) {
  const [files, setFiles] = useState<File[]>([]);
  const [pickErr, setPickErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [results, setResults] = useState<PhotoResult[]>([]);
  const sent = results.filter((r) => r.ok).length;
  const failed = results.filter((r) => !r.ok);
  const remaining = PHOTO_MAX_COUNT - sent;

  function pick(list: FileList | null) {
    const arr = Array.from(list ?? []);
    const bad = arr.map(photoError).filter(Boolean) as string[];
    const good = arr.filter((f) => !photoError(f)).slice(0, remaining);
    setPickErr(bad.length ? bad.join(". ") : arr.length > remaining ? `Only ${remaining} more photo(s) allowed.` : null);
    setFiles(good);
  }

  async function send() {
    setBusy(true);
    const res = await uploadLeadPhotos(supabase as never, { leadId: done.leadId, bucket: done.uploadBucket, prefix: done.uploadPrefix, files });
    setResults((r) => [...r.filter((x) => x.ok), ...res]);
    setFiles(files.filter((f) => !res.find((r) => r.name === f.name && r.ok)));
    setBusy(false);
  }

  return (
    <div className="mt-6 border-t pt-5 text-left">
      <h3 className="font-display text-lg font-bold uppercase">Add photos (optional)</h3>
      <p className="text-sm text-muted-foreground">Up to {PHOTO_MAX_COUNT} photos, JPG/PNG/WEBP/HEIC, 8 MB each. Photos stay private to JC's Towing staff.</p>
      {remaining > 0 && (
        <>
          <Label htmlFor="photos" className="sr-only">Choose photos</Label>
          <input id="photos" type="file" multiple accept={[...PHOTO_TYPES, ".heic", ".heif"].join(",")} onChange={(e) => pick(e.target.files)} className="mt-3 block w-full text-sm file:mr-3 file:min-h-11 file:rounded-md file:border-0 file:bg-secondary file:px-4 file:font-semibold" />
          {pickErr && <p role="alert" className="mt-2 text-sm text-destructive">{pickErr}</p>}
          <Button type="button" variant="secondary" className="mt-3 min-h-11" disabled={!files.length || busy} onClick={send}>
            {busy ? <><Loader2 className="animate-spin" /> Uploading…</> : failed.length ? `Retry ${files.length} photo(s)` : `Upload ${files.length || ""} photo(s)`}
          </Button>
        </>
      )}
      <div aria-live="polite">
        {sent > 0 && <p className="mt-3 text-sm font-semibold text-success">{sent} photo(s) received.</p>}
        {failed.length > 0 && (
          <p role="alert" className="mt-3 border-l-4 border-warning bg-warning/15 p-3 text-sm">
            <AlertTriangle className="mr-1 inline h-4 w-4" aria-hidden />Your request was received, but photo upload is incomplete ({failed.map((f) => f.error).join("; ")}). Choose the photos again to retry, or mention them when we call: <a className="font-bold underline" href={`tel:${phoneE164}`}>{phone}</a>
          </p>
        )}
      </div>
    </div>
  );
}

function Choice({ name, legend, options, defaultValue }: { name: string; legend: string; options: [string, string][]; defaultValue?: string }) {
  return (
    <fieldset className="space-y-1">
      <legend className="text-sm font-medium">{legend}</legend>
      <div className="flex flex-wrap gap-x-4">
        {options.map(([v, l]) => (
          <label key={v} className="flex min-h-11 items-center gap-2">
            <input type="radio" name={name} value={v} defaultChecked={v === defaultValue} className="h-5 w-5 accent-[var(--color-primary)]" /> {l}
          </label>
        ))}
      </div>
    </fieldset>
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