import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Loading, ErrorBox, DemoBadge } from "@/components/staff/kit";
import { dt, type Lead } from "@/lib/staff";

type L = Lead & Record<string, unknown>;

const INTAKE: [string, string][] = [
  ["preferred_contact_method", "Preferred contact"], ["vehicle_type", "Vehicle type"], ["drivable", "Drivable"],
  ["rolls", "Rolls"], ["steers", "Steers"], ["shifts", "Shifts"], ["keys_available", "Keys"],
  ["accident", "Accident"], ["wheel_damage", "Wheel damage"], ["clearance_issue", "Clearance issue"], ["access_notes", "Access notes"],
];
const ATTR: [string, string][] = [
  ["source_page", "Source page"], ["landing_page", "Landing page"], ["referrer", "Referrer"],
  ["utm_source", "UTM source"], ["utm_medium", "UTM medium"], ["utm_campaign", "UTM campaign"], ["utm_content", "UTM content"],
  ["first_touch_source", "First-touch source"], ["gclid", "gclid"], ["fbclid", "fbclid"], ["msclkid", "msclkid"],
  ["device_type", "Device"], ["session_id", "Session"],
];

function Rows({ lead, defs }: { lead: L; defs: [string, string][] }) {
  return (
    <dl className="grid grid-cols-[minmax(0,10rem)_1fr] gap-x-3 gap-y-1 text-sm">
      {defs.map(([k, l]) => (
        <div key={k} className="contents"><dt className="text-muted-foreground">{l}</dt><dd className="break-words">{(lead[k] as string | null) || "—"}</dd></div>
      ))}
    </dl>
  );
}

export function LeadDetail({ lead, onOpenChange }: { lead: Lead | null; onOpenChange: (o: boolean) => void }) {
  const id = lead?.id;
  const extra = useQuery({
    enabled: !!id,
    queryKey: ["lead-detail", id],
    queryFn: async () => {
      const [ev, files] = await Promise.all([
        supabase.from("lead_events").select("id, event_type, metadata, created_at").eq("lead_id", id!).order("created_at"),
        supabase.from("evidence_files").select("id, file_name, mime_type, file_size_bytes, source, created_at").eq("lead_id", id!).eq("archived", false),
      ]);
      if (ev.error) throw ev.error;
      return { events: ev.data ?? [], files: files.data ?? [], filesErr: files.error };
    },
  });
  const l = lead as L | null;
  return (
    <Dialog open={!!lead} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] max-w-2xl overflow-y-auto">
        {l && (
          <>
            <DialogHeader><DialogTitle>Lead #{l.lead_number}<DemoBadge show={l.is_demo} /></DialogTitle></DialogHeader>
            <p className="text-sm text-muted-foreground">Created {dt(l.created_at)} · updated {dt(l.updated_at)} · {l.source}</p>
            <section><h3 className="mb-2 font-display font-bold uppercase">Intake</h3><Rows lead={l} defs={INTAKE} />
              <p className="mt-2 text-sm">Location pin: {l["geolocation_lat"] != null ? `shared (±${Math.round(Number(l["geolocation_accuracy_m"] ?? 0))} m) — ` : "not shared"}
                {l["geolocation_lat"] != null && <a className="text-primary underline" target="_blank" rel="noreferrer" href={`https://www.google.com/maps?q=${l["geolocation_lat"]},${l["geolocation_lng"]}`}>open map</a>}
              </p>
            </section>
            <section><h3 className="mb-2 font-display font-bold uppercase">Attribution (first-party)</h3><Rows lead={l} defs={ATTR} /></section>
            {extra.isLoading ? <Loading /> : extra.error ? <ErrorBox error={extra.error} /> : (
              <>
                <section><h3 className="mb-2 font-display font-bold uppercase">History</h3>
                  {extra.data!.events.length ? <ol className="space-y-1 text-sm">{extra.data!.events.map((e) => <li key={e.id}><span className="font-mono text-xs text-muted-foreground">{dt(e.created_at)}</span> {e.event_type.replace(/_/g, " ")}</li>)}</ol> : <p className="text-sm text-muted-foreground">No events recorded.</p>}
                </section>
                <section><h3 className="mb-2 font-display font-bold uppercase">Photos / evidence</h3>
                  {extra.data!.filesErr ? <p className="text-sm text-muted-foreground">You don't have access to evidence for this lead.</p> : extra.data!.files.length ? (
                    <ul className="space-y-1 text-sm">{extra.data!.files.map((f) => <li key={f.id}>{f.file_name} · {f.mime_type} · {f.file_size_bytes ? `${Math.round(f.file_size_bytes / 1024)} KB` : "?"} · {f.source}</li>)}</ul>
                  ) : <p className="text-sm text-muted-foreground">No photos attached.</p>}
                  <p className="mt-1 text-xs text-muted-foreground">Files are private; open them from Evidence.</p>
                </section>
              </>
            )}
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}