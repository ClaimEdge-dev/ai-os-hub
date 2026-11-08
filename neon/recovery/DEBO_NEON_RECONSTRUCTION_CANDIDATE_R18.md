# DEBO Neon historical schema reconstruction (NOT DEPLOYED)

Original project `snowy-block-04251510` currently returns HTTP 404. This is a reconstruction candidate, not a live database backup. Production unchanged. Source: `neon/claimedge_schema_result.json`.

The original trigger function refers to `updated_at` absent from the eight table declarations. Candidate below adds `updated_at TIMESTAMPTZ DEFAULT NOW()` to each table. Seed data deliberately excluded until source verification. Test on isolated temporary database only; do not apply to production without owner approval.

```sql
CREATE SCHEMA IF NOT EXISTS claimedge_os;

CREATE TABLE claimedge_os.skills_registry (skill_id TEXT PRIMARY KEY, name TEXT NOT NULL, pillar TEXT NOT NULL, status TEXT NOT NULL CHECK (status IN ('Draft','Testing','Approved','Restricted','Deprecated','Archived')), version TEXT, description TEXT, filepath TEXT, trigger_phrases TEXT[], dependencies TEXT[], last_updated DATE, reviewed_by TEXT, qa_score NUMERIC, updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE claimedge_os.roles (role_id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, domain TEXT NOT NULL, description TEXT, skills_required TEXT[], activation_trigger TEXT, authority_level INTEGER CHECK (authority_level BETWEEN 1 AND 5), active BOOLEAN DEFAULT true, updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE claimedge_os.tasks (task_id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL CHECK (status IN ('Backlog','In Progress','Blocked','Review','Done')), priority TEXT CHECK (priority IN ('P0','P1','P2','P3')), assignee_role TEXT, pillar TEXT, due_date DATE, blocked_reason TEXT, parent_task TEXT REFERENCES claimedge_os.tasks(task_id), updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE claimedge_os.migration_tracker (item_id TEXT PRIMARY KEY, item_name TEXT NOT NULL, item_type TEXT CHECK (item_type IN ('Skill','Document','Database','Automation','Template')), old_location TEXT, new_location TEXT, status TEXT CHECK (status IN ('Not Started','In Progress','Complete','Blocked')), priority TEXT CHECK (priority IN ('Critical','High','Medium','Low')), effort_hours NUMERIC, assigned_to TEXT, notes TEXT, updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE claimedge_os.references (ref_id TEXT PRIMARY KEY, title TEXT NOT NULL, category TEXT CHECK (category IN ('Statute','Case Law','Building Code','Regulation','Carrier Guideline')), jurisdiction TEXT, citation TEXT, url TEXT, relevance TEXT, last_verified DATE, updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE claimedge_os.skill_qa (qa_id SERIAL PRIMARY KEY, skill_name TEXT NOT NULL, test_date DATE, tester TEXT, result TEXT CHECK (result IN ('Pass','Fail','Partial')), issues_found TEXT, severity TEXT CHECK (severity IN ('Critical','Major','Minor','Cosmetic')), fix_required BOOLEAN, retest_date DATE, updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE claimedge_os.risk_matrix (risk_id SERIAL PRIMARY KEY, output_type TEXT NOT NULL, risk_level TEXT CHECK (risk_level IN ('Low','Medium','High')), auto_run BOOLEAN, review_required BOOLEAN, human_signoff BOOLEAN, description TEXT, updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE claimedge_os.memory_lessons (memory_id SERIAL PRIMARY KEY, session_date DATE, topic TEXT, lesson TEXT, category TEXT CHECK (category IN ('Technical','Process','Business','Tooling')), applied BOOLEAN, related_skill TEXT, updated_at TIMESTAMPTZ DEFAULT NOW());

CREATE INDEX idx_skills_pillar ON claimedge_os.skills_registry(pillar);

CREATE INDEX idx_skills_status ON claimedge_os.skills_registry(status);

CREATE INDEX idx_skills_name ON claimedge_os.skills_registry(name);

CREATE INDEX idx_roles_active ON claimedge_os.roles(active);

CREATE INDEX idx_roles_domain ON claimedge_os.roles(domain);

CREATE INDEX idx_tasks_status ON claimedge_os.tasks(status);

CREATE INDEX idx_tasks_priority ON claimedge_os.tasks(priority);

CREATE INDEX idx_tasks_assignee ON claimedge_os.tasks(assignee_role);

CREATE INDEX idx_tasks_pillar ON claimedge_os.tasks(pillar);

CREATE INDEX idx_tasks_due ON claimedge_os.tasks(due_date);

CREATE INDEX idx_migration_status ON claimedge_os.migration_tracker(status);

CREATE INDEX idx_migration_type ON claimedge_os.migration_tracker(item_type);

CREATE INDEX idx_migration_priority ON claimedge_os.migration_tracker(priority);

CREATE INDEX idx_refs_category ON claimedge_os.references(category);

CREATE INDEX idx_refs_jurisdiction ON claimedge_os.references(jurisdiction);

CREATE INDEX idx_qa_skill ON claimedge_os.skill_qa(skill_name);

CREATE INDEX idx_qa_result ON claimedge_os.skill_qa(result);

CREATE INDEX idx_qa_date ON claimedge_os.skill_qa(test_date);

CREATE INDEX idx_risk_level ON claimedge_os.risk_matrix(risk_level);

CREATE INDEX idx_risk_type ON claimedge_os.risk_matrix(output_type);

CREATE INDEX idx_memory_category ON claimedge_os.memory_lessons(category);

CREATE INDEX idx_memory_applied ON claimedge_os.memory_lessons(applied);

CREATE INDEX idx_memory_date ON claimedge_os.memory_lessons(session_date);

CREATE OR REPLACE FUNCTION claimedge_os.set_updated_at() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_skills_updated_at BEFORE UPDATE ON claimedge_os.skills_registry FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();

CREATE TRIGGER trg_roles_updated_at BEFORE UPDATE ON claimedge_os.roles FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();

CREATE TRIGGER trg_tasks_updated_at BEFORE UPDATE ON claimedge_os.tasks FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();

CREATE TRIGGER trg_migration_updated_at BEFORE UPDATE ON claimedge_os.migration_tracker FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();

CREATE TRIGGER trg_refs_updated_at BEFORE UPDATE ON claimedge_os.references FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();

CREATE TRIGGER trg_qa_updated_at BEFORE UPDATE ON claimedge_os.skill_qa FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();

CREATE TRIGGER trg_risk_updated_at BEFORE UPDATE ON claimedge_os.risk_matrix FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();

CREATE TRIGGER trg_memory_updated_at BEFORE UPDATE ON claimedge_os.memory_lessons FOR EACH ROW EXECUTE FUNCTION claimedge_os.set_updated_at();
```

Acceptance: 8 tables; 24 indexes; 8 triggers; all trigger targets have updated_at; inspect SQL in PostgreSQL test database; verify inserts/updates/rollback with synthetic fixtures. No live acceptance performed.

## R18 static acceptance receipt (2026-11-08)

Read-back verified this file against the original historical receipt. Static checks: {"tables":8,"explicit_indexes":23,"triggers":8,"updated_at":8,"create_function":1}. The source's 24-index claim conflicts with its 23 explicit CREATE INDEX statements; PostgreSQL may create additional primary-key indexes, so total indexes must be checked on an actual isolated database. No PostgreSQL execution or rollback test has been performed. Original project ID returned HTTP 404 through the currently connected Neon accounts. No production mutations, no backup restoration, no database creation. Next: recover an actual backup or authorize an isolated PostgreSQL test target, execute schema, inspect catalog, test synthetic insert/update/rollback, and only then decide on replacement.
