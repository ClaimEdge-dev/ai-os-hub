import { createFileRoute } from "@tanstack/react-router";
import { useServerFn } from "@tanstack/react-start";
import { useState, type FormEvent } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Loader2, UserPlus } from "lucide-react";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PageHeader, Loading, ErrorBox, Empty } from "@/components/staff/kit";
import { createStaffUser } from "@/lib/staff.functions";
import { useStaff, hasAny, errMsg, ROLE_LABEL, type Role } from "@/lib/staff";

export const Route = createFileRoute("/_authenticated/staff/settings")({ component: Settings });

type Raw = Record<string, any>;

const SERVICE_LABELS: Record<string, string> = {
  towing: "Towing", roadside: "Roadside assistance", transport: "Vehicle transport", commercial: "Commercial / fleet",
  recovery: "Recovery", heavy_duty: "Heavy duty", semi: "Semi", insurance_towing: "Insurance towing", property_towing: "Private property towing",
};

function Settings() {
  const staff = useStaff();
  const isAdmin = hasAny(staff, ["admin"]);
  if (!isAdmin) return <><PageHeader title="Settings" /><Empty title="Owner / Admin only">Ask the owner to change business settings or staff accounts.</Empty></>;
  return (
    <>
      <PageHeader title="Settings" sub="Business Truth is the only source for claims shown on the public website." />
      <Tabs defaultValue="truth">
        <TabsList><TabsTrigger value="truth">Business Truth</TabsTrigger><TabsTrigger value="crm">CRM rules</TabsTrigger><TabsTrigger value="users">Users & roles</TabsTrigger></TabsList>
        <TabsContent value="truth"><BusinessTruthEditor /></TabsContent>
        <TabsContent value="crm"><CrmEditor /></TabsContent>
        <TabsContent value="users"><Users /></TabsContent>
      </Tabs>
    </>
  );
}

function useSetting(key: string) {
  return useQuery({
    queryKey: ["settings", key],
    queryFn: async () => {
      const { data, error } = await supabase.from("settings").select("value").eq("key", key).maybeSingle();
      if (error) throw error;
      return (data?.value ?? {}) as Raw;
    },
  });
}

function useSaveSetting(key: string) {
  const qc = useQueryClient();
  return async (value: Raw) => {
    const { error } = await supabase.from("settings").update({ value } as any).eq("key", key);
    if (error) { toast.error(errMsg(error)); return false; }
    qc.invalidateQueries({ queryKey: ["settings"] });
    qc.invalidateQueries({ queryKey: ["business-truth"] });
    toast.success("Saved");
    return true;
  };
}

function Field({ label, name, value, hint, area }: { label: string; name: string; value: string; hint?: string; area?: boolean }) {
  return (
    <div className={area ? "sm:col-span-2" : ""}>
      <Label htmlFor={`bt-${name}`} className="mb-1 block text-xs font-semibold uppercase">{label}</Label>
      {area ? <Textarea id={`bt-${name}`} name={name} defaultValue={value} rows={3} /> : <Input id={`bt-${name}`} name={name} defaultValue={value} className="h-10" />}
      {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
    </div>
  );
}

function BusinessTruthEditor() {
  const q = useSetting("business");
  const save = useSaveSetting("business");
  const [busy, setBusy] = useState(false);
  const [services, setServices] = useState<Record<string, boolean> | null>(null);
  const [showHours, setShowHours] = useState<boolean | null>(null);
  if (q.isLoading) return <Loading />;
  if (q.error) return <ErrorBox error={q.error} />;
  const raw = q.data ?? {};
  const svc: Record<string, boolean> = services ?? { ...Object.fromEntries(Object.keys(SERVICE_LABELS).map((k) => [k, false])), ...(raw.services ?? {}) };
  const hoursOn = showHours ?? !!raw.show_hours;

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const s = (k: string) => String(f.get(k) ?? "").trim();
    // Merge onto the stored record so keys this form doesn't edit are preserved.
    const next: Raw = {
      ...raw,
      name: s("name") || raw.name, phone: s("phone") || raw.phone, phone_e164: s("phone_e164") || raw.phone_e164,
      city: s("city"), state: s("state"), domain: s("domain"), tagline: s("tagline"), hours: s("hours"), show_hours: hoursOn,
      email: s("email"), review_url: s("review_url"), logo_url: s("logo_url"), about: s("about"),
      service_areas: s("service_areas").split(/[,\n]/).map((x) => x.trim()).filter(Boolean),
      services: svc,
    };
    setBusy(true);
    await save(next);
    setBusy(false);
  }

  return (
    <form onSubmit={onSubmit} className="max-w-3xl space-y-6">
      <p className="rounded-md border-l-4 border-primary bg-muted p-3 text-sm">Enter only facts the owner has confirmed. Leave a field blank if unsure — blank fields are hidden on the website.{raw.owner_approval_note ? ` Last note: ${raw.owner_approval_note}` : ""}</p>
      <section className="grid gap-4 sm:grid-cols-2">
        <Field label="Business name" name="name" value={raw.name ?? ""} />
        <Field label="Phone (display)" name="phone" value={raw.phone ?? ""} />
        <Field label="Phone (dialing, +1…)" name="phone_e164" value={raw.phone_e164 ?? ""} />
        <Field label="Email (public, optional)" name="email" value={raw.email ?? ""} />
        <Field label="City" name="city" value={raw.city ?? ""} />
        <Field label="State" name="state" value={raw.state ?? ""} />
        <Field label="Domain reference" name="domain" value={raw.domain ?? ""} hint="Reference only — changing this doesn't connect a domain." />
        <Field label="Tagline (optional)" name="tagline" value={raw.tagline ?? ""} hint="Shown in the footer. Leave blank unless approved." />
        <Field label="Service cities" name="service_areas" value={(raw.service_areas ?? []).join(", ")} hint="Comma-separated. Only list cities you actually serve." area />
        <Field label="Hours" name="hours" value={raw.hours ?? ""} area />
        <div className="flex items-center gap-3 sm:col-span-2"><Switch id="show_hours" checked={hoursOn} onCheckedChange={setShowHours} /><Label htmlFor="show_hours">Show hours on the website</Label></div>
        <Field label="Review page link" name="review_url" value={raw.review_url ?? ""} />
        <Field label="Logo image link (optional)" name="logo_url" value={raw.logo_url ?? ""} />
        <Field label="About text" name="about" value={raw.about ?? ""} area />
      </section>
      <section>
        <h2 className="font-display text-xl font-extrabold uppercase">Public service visibility</h2>
        <p className="text-sm text-muted-foreground">Turn on only services you currently offer. Off means hidden from the website.</p>
        <ul className="mt-3 grid gap-2 sm:grid-cols-2">
          {Object.keys(svc).map((k) => (
            <li key={k} className="flex items-center justify-between rounded-md border p-3">
              <Label htmlFor={`svc-${k}`}>{SERVICE_LABELS[k] ?? k}</Label>
              <Switch id={`svc-${k}`} checked={!!svc[k]} onCheckedChange={(c) => setServices({ ...svc, [k]: c })} />
            </li>
          ))}
        </ul>
      </section>
      <Button type="submit" variant="hero" disabled={busy}>{busy && <Loader2 className="animate-spin" />} Save Business Truth</Button>
    </form>
  );
}

function CrmEditor() {
  const q = useSetting("crm");
  const save = useSaveSetting("crm");
  const [flags, setFlags] = useState<Raw | null>(null);
  if (q.isLoading) return <Loading />;
  if (q.error) return <ErrorBox error={q.error} />;
  const raw = q.data ?? {};
  const f = flags ?? raw;
  return (
    <form className="max-w-3xl space-y-4" onSubmit={async (e) => {
      e.preventDefault();
      const fd = new FormData(e.currentTarget);
      await save({ ...raw, ...f, review_sms_template: String(fd.get("sms") ?? ""), review_email_template: String(fd.get("email") ?? "") });
    }}>
      {[["require_invoice_approval", "Invoices need owner approval"], ["require_lead_dup_check", "Warn about duplicate leads"]].map(([k, l]) => (
        <div key={k} className="flex items-center gap-3"><Switch id={k} checked={!!f[k!]} onCheckedChange={(c) => setFlags({ ...f, [k!]: c })} /><Label htmlFor={k}>{l}</Label></div>
      ))}
      <div><Label htmlFor="sms" className="text-xs font-semibold uppercase">Review text template</Label><Textarea id="sms" name="sms" rows={3} defaultValue={raw.review_sms_template ?? ""} /></div>
      <div><Label htmlFor="email" className="text-xs font-semibold uppercase">Review email template</Label><Textarea id="email" name="email" rows={6} defaultValue={raw.review_email_template ?? ""} /></div>
      <p className="text-xs text-muted-foreground">Use {"{name}"} and {"{review_url}"}. Templates only create drafts — nothing sends automatically.</p>
      <Button type="submit" variant="hero">Save CRM rules</Button>
    </form>
  );
}

function Users() {
  const create = useServerFn(createStaffUser);
  const qc = useQueryClient();
  const [roles, setRoles] = useState<Role[]>(["dispatcher"]);
  const [busy, setBusy] = useState(false);
  const [temp, setTemp] = useState<string | null>(null);
  const list = useQuery({
    queryKey: ["staff-users"],
    queryFn: async () => {
      const [p, r] = await Promise.all([supabase.from("profiles").select("id, full_name, email, active"), supabase.from("user_roles").select("user_id, role")]);
      if (p.error) throw p.error;
      return (p.data ?? []).map((u) => ({ ...u, roles: (r.data ?? []).filter((x) => x.user_id === u.id).map((x) => x.role as Role) }));
    },
  });

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const f = new FormData(form);
    if (!roles.length) return toast.error("Pick at least one role");
    setBusy(true);
    try {
      const res = await create({ data: { email: String(f.get("email")), full_name: String(f.get("full_name")), phone: String(f.get("phone") || "") || undefined, roles } });
      if (!res.ok) throw new Error(res.error);
      setTemp(res.tempPassword);
      form.reset();
      qc.invalidateQueries({ queryKey: ["staff-users"] });
    } catch (err) { toast.error(errMsg(err)); } finally { setBusy(false); }
  }

  return (
    <div className="grid gap-8 lg:grid-cols-2">
      <section>
        <h2 className="font-display text-xl font-extrabold uppercase">Staff accounts</h2>
        {list.isLoading ? <Loading /> : list.error ? <ErrorBox error={list.error} /> : (
          <ul className="mt-3 divide-y rounded-md border bg-card">
            {list.data!.map((u) => <li key={u.id} className="p-3"><p className="font-semibold">{u.full_name || u.email}</p><p className="text-xs text-muted-foreground">{u.email} · {u.roles.map((r) => ROLE_LABEL[r]).join(", ") || "no role"}</p></li>)}
          </ul>
        )}
      </section>
      <section>
        <h2 className="font-display text-xl font-extrabold uppercase">Add staff login</h2>
        <form onSubmit={onSubmit} className="mt-3 space-y-3">
          <div><Label htmlFor="u-name">Full name</Label><Input id="u-name" name="full_name" required className="h-10" /></div>
          <div><Label htmlFor="u-email">Email</Label><Input id="u-email" name="email" type="email" required className="h-10" /></div>
          <div><Label htmlFor="u-phone">Phone (optional)</Label><Input id="u-phone" name="phone" type="tel" className="h-10" /></div>
          <fieldset><legend className="text-sm font-medium">Roles</legend>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {(Object.keys(ROLE_LABEL) as Role[]).map((r) => (
                <label key={r} className="flex items-center gap-2 text-sm"><input type="checkbox" checked={roles.includes(r)} onChange={(e) => setRoles(e.target.checked ? [...roles, r] : roles.filter((x) => x !== r))} /> {ROLE_LABEL[r]}</label>
              ))}
            </div>
          </fieldset>
          <Button type="submit" variant="hero" disabled={busy}>{busy ? <Loader2 className="animate-spin" /> : <UserPlus />} Create login</Button>
        </form>
        {temp && <p role="status" className="mt-4 rounded-md border-l-4 border-warning bg-warning/15 p-3 text-sm">Temporary password: <code className="font-bold">{temp}</code> — share it privately. They can change it with "Forgot password". No email was sent.</p>}
      </section>
    </div>
  );
}