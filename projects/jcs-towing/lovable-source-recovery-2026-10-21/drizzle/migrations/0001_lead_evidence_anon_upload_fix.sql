CREATE OR REPLACE FUNCTION public.lead_accepts_public_upload(p_object_name text)
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.leads l
    WHERE (storage.foldername(p_object_name))[1] = 'lead-intake'
      AND coalesce((storage.foldername(p_object_name))[2],'') ~ '^[0-9a-fA-F-]{36}$'
      AND l.id::text = (storage.foldername(p_object_name))[2]
      AND l.source = 'website'
      AND l.created_at > now() - interval '2 hours'
  )
$$;
REVOKE ALL ON FUNCTION public.lead_accepts_public_upload(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.lead_accepts_public_upload(text) TO anon, authenticated;
DROP POLICY IF EXISTS "lead evidence anon upload" ON storage.objects;
CREATE POLICY "lead evidence anon upload" ON storage.objects FOR INSERT TO anon
  WITH CHECK (bucket_id = 'lead-evidence' AND public.lead_accepts_public_upload(name));