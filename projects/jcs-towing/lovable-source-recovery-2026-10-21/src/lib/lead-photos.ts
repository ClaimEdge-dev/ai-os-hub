import { photoError, PHOTO_MAX_COUNT } from "./lead-schema";

export type PhotoResult = { name: string; ok: boolean; error?: string };

type Client = {
  storage: { from: (b: string) => { upload: (path: string, f: Blob, o?: Record<string, unknown>) => Promise<{ error: { message: string } | null }> } };
  rpc: (fn: string, args: Record<string, unknown>) => PromiseLike<{ error: { message: string } | null }>;
};

/**
 * Uploads photos AFTER the lead exists. Never throws: a failed photo must not
 * undo a received request — callers show a retry state instead.
 */
export async function uploadLeadPhotos(client: Client, opts: { leadId: string; bucket: string; prefix: string; files: File[] }): Promise<PhotoResult[]> {
  const out: PhotoResult[] = [];
  for (const f of opts.files.slice(0, PHOTO_MAX_COUNT)) {
    const bad = photoError(f);
    if (bad) { out.push({ name: f.name, ok: false, error: bad }); continue; }
    const safe = f.name.replace(/[^a-zA-Z0-9._-]/g, "_").slice(-80);
    const path = `${opts.prefix}${crypto.randomUUID()}-${safe}`;
    try {
      const up = await client.storage.from(opts.bucket).upload(path, f, { contentType: f.type || undefined, upsert: false });
      if (up.error) { out.push({ name: f.name, ok: false, error: "Upload failed" }); continue; }
      const reg = await client.rpc("register_lead_evidence", {
        p_lead_id: opts.leadId, p_storage_path: path, p_file_name: f.name,
        p_mime_type: f.type || "image/heic", p_file_size_bytes: f.size, p_category: "intake",
      });
      out.push(reg.error ? { name: f.name, ok: false, error: "Saved but not linked" } : { name: f.name, ok: true });
    } catch {
      out.push({ name: f.name, ok: false, error: "Upload failed" });
    }
  }
  return out;
}