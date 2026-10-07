-- Rapid Roadside Repair private evidence storage
-- PREPARED / NOT APPLIED
-- No anonymous upload policy is created here.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'rrr-evidence',
  'rrr-evidence',
  false,
  8388608,
  array['image/jpeg','image/png','image/webp']::text[]
)
on conflict (id) do update
set public = false,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists rrr_staff_read_evidence on storage.objects;
create policy rrr_staff_read_evidence
on storage.objects for select
to authenticated
using (bucket_id = 'rrr-evidence');

drop policy if exists rrr_staff_insert_evidence on storage.objects;
create policy rrr_staff_insert_evidence
on storage.objects for insert
to authenticated
with check (bucket_id = 'rrr-evidence');

drop policy if exists rrr_staff_update_evidence on storage.objects;
create policy rrr_staff_update_evidence
on storage.objects for update
to authenticated
using (bucket_id = 'rrr-evidence')
with check (bucket_id = 'rrr-evidence');

drop policy if exists rrr_staff_delete_evidence on storage.objects;
create policy rrr_staff_delete_evidence
on storage.objects for delete
to authenticated
using (bucket_id = 'rrr-evidence');

-- Future public-request photo upload should use a tested signed-upload
-- or security-definer authorization path. Do not grant anon insert here.
