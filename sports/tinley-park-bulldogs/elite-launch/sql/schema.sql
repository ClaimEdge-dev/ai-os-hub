-- TPB AthleteOS starter schema. Private youth data: add/test RLS before deployment.
create table if not exists tpb_games (
  id text primary key,
  season int not null,
  game_date date,
  opponent text not null,
  score_for int,
  score_against int,
  film_completeness text not null default 'UNKNOWN',
  created_at timestamptz not null default now()
);

create table if not exists tpb_players (
  id text primary key,
  jersey_number text,
  display_name text not null,
  pronunciation text,
  positions text[] not null default '{}'
);

create table if not exists tpb_video_assets (
  id text primary key,
  game_id text references tpb_games(id),
  filename text not null,
  source_uri text not null,
  sha256 text not null unique,
  duration_seconds numeric,
  fps numeric,
  capture_time timestamptz,
  review_status text not null default 'UNREVIEWED'
);

create table if not exists tpb_plays (
  id text primary key,
  game_id text not null references tpb_games(id),
  source_clip_id text references tpb_video_assets(id),
  active_snap boolean not null default false,
  phase text,
  formation_id text,
  motion_id text,
  fake_id text,
  play_name text,
  play_family text,
  result text,
  verified_yards numeric,
  evidence_label text not null,
  confidence numeric,
  review_status text not null
);

create table if not exists tpb_events (
  id text primary key,
  game_id text not null references tpb_games(id),
  play_id text not null references tpb_plays(id),
  player_id text references tpb_players(id),
  event_type text not null,
  value_json jsonb,
  evidence_label text not null,
  confidence numeric,
  review_status text not null
);

create table if not exists tpb_corrections (
  id text primary key,
  target_type text not null,
  target_id text not null,
  field_name text,
  original_value jsonb,
  corrected_value jsonb,
  reviewer text,
  reason text,
  source_reference text,
  created_at timestamptz not null default now()
);
