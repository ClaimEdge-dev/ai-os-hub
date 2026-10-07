create extension if not exists pgcrypto;

create type cwa_truth_state as enum (
  'VERIFIED','LIKELY','UNRESOLVED','CONCEPT','PLANNED','SUPERSEDED','BLOCKED','APPROVAL_REQUIRED'
);
create type cwa_work_status as enum (
  'INBOX','RECOVER','VERIFY','READY','BUILDING','QA','APPROVAL','BLOCKED','RELEASE_READY','DONE','ARCHIVE'
);

create table if not exists cwa_work_items (
  id uuid primary key default gen_random_uuid(),
  lane text not null,
  title text not null,
  status cwa_work_status not null default 'INBOX',
  truth_state cwa_truth_state not null default 'UNRESOLVED',
  approval_required boolean not null default false,
  blocker text,
  return_point text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists cwa_task_deltas (
  id uuid primary key default gen_random_uuid(),
  work_item_id uuid references cwa_work_items(id),
  why_needed text not null,
  classification text not null,
  artifact_path text,
  return_point text,
  created_at timestamptz not null default now()
);

create table if not exists cwa_apparel_series (
  id uuid primary key default gen_random_uuid(),
  code text unique not null,
  name text not null,
  truth_state cwa_truth_state not null default 'CONCEPT',
  design_rules text
);

create table if not exists cwa_achievement_marks (
  id uuid primary key default gen_random_uuid(),
  code text unique not null,
  name text not null,
  visual_spec text not null,
  repeatable boolean not null default true
);

create table if not exists cwa_media_rights_private (
  id uuid primary key default gen_random_uuid(),
  athlete_internal_key text unique not null,
  guardian_consent_status text not null default 'UNKNOWN',
  website_allowed boolean,
  social_allowed boolean,
  video_allowed boolean,
  sponsor_ad_allowed boolean,
  notes_private text
);
