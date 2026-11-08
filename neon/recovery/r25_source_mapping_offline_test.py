"""R25 offline source identity, fingerprint, and mapping gates. No database writes."""
import hashlib,json,unittest
ROWS=json.loads("[\n  {\n    \"id\": \"WORK-DEBO-001\",\n    \"project\": \"DEBO\",\n    \"state\": \"CHECKPOINT / EXECUTION CONTINUES IN PROJECT LANES\",\n    \"priority\": \"P0\"\n  },\n  {\n    \"id\": \"WORK-JCT-001\",\n    \"project\": \"JCT\",\n    \"state\": \"NATIVE BACKEND DEPLOYED PRIVATE / DATA SCHEMA VERIFIED / E2E HELD\",\n    \"priority\": \"P0\"\n  },\n  {\n    \"id\": \"WORK-CE-001\",\n    \"project\": \"CE-OS\",\n    \"state\": \"SOURCE RECOVERED / GOVERNANCE & LIVE E2E OPEN\",\n    \"priority\": \"P0\"\n  },\n  {\n    \"id\": \"WORK-DWING-001\",\n    \"project\": \"DWING\",\n    \"state\": \"PRIVATE V13 TESTED / V12 INTEGRATION BLOCKED\",\n    \"priority\": \"P0\"\n  },\n  {\n    \"id\": \"WORK-SETTLE-001\",\n    \"project\": \"SETTLE\",\n    \"state\": \"EXISTING EVIDENCE LEDGER / PRIMARY PROOF & DEDUPE OPEN\",\n    \"priority\": \"P0\"\n  },\n  {\n    \"id\": \"WORK-PLOG-001\",\n    \"project\": \"PLOG\",\n    \"state\": \"SOURCE RECONCILED / PRIMARY LEGAL AUTHORITY UNVERIFIED\",\n    \"priority\": \"P0\"\n  },\n  {\n    \"id\": \"WORK-RRR-001\",\n    \"project\": \"RRR\",\n    \"state\": \"EXISTING BUILD VERIFIED / LIVE PUBLIC INTAKE UNVERIFIED\",\n    \"priority\": \"P1\"\n  },\n  {\n    \"id\": \"WORK-MOL-001\",\n    \"project\": \"MORGANS\",\n    \"state\": \"PRIVATE SOURCE DEMO / CANONICAL SITE-CRM UNVERIFIED\",\n    \"priority\": \"P1\"\n  },\n  {\n    \"id\": \"WORK-BBS-001\",\n    \"project\": \"BBS\",\n    \"state\": \"READY\",\n    \"priority\": \"P1\"\n  },\n  {\n    \"id\": \"WORK-WRESTLE-001\",\n    \"project\": \"WRESTLE\",\n    \"state\": \"STAGED RECOVERY / LIVE DB ACCESS BLOCKED\",\n    \"priority\": \"P1\"\n  },\n  {\n    \"id\": \"WORK-ATHLETE-001\",\n    \"project\": \"ATHLETE\",\n    \"state\": \"PRIVATE PREVIEW SOURCE / PRODUCTION AUTH UNVERIFIED\",\n    \"priority\": \"P1\"\n  },\n  {\n    \"id\": \"WORK-BASEBALL-001\",\n    \"project\": \"BASEBALL\",\n    \"state\": \"WAITING\",\n    \"priority\": \"P2\"\n  },\n  {\n    \"id\": \"WORK-RENTALS-001\",\n    \"project\": \"RENTALS\",\n    \"state\": \"PARKED BY OWNER / RECORDS PRESERVED\",\n    \"priority\": \"P1\"\n  },\n  {\n    \"id\": \"WORK-NEON-001\",\n    \"project\": \"NEON\",\n    \"state\": \"BLOCKED — CONNECTED NEON HAS ZERO VISIBLE PROJECTS\",\n    \"priority\": \"P0\"\n  },\n  {\n    \"id\": \"WORK-TPB-001\",\n    \"project\": \"DEBO-TPB-OS\",\n    \"state\": \"RECOVERY + MEDIA QA OPEN\",\n    \"priority\": \"P1\"\n  }\n]")
def fingerprint(row):
    payload=json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()
def classify(row):
    if row['id']=='WORK-RENTALS-001':return 'HOLD_OWNER'
    return 'QUARANTINE_UNAPPROVED_MAPPING'
def verify(rows):
    ids=[r['id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate source ID')
    for r in rows:
        if not all(r.get(k) for k in ('id','project','state','priority')):raise ValueError('missing source field')
        if r['priority'] not in ('P0','P1','P2','P3'):raise ValueError('invalid priority')
    return {'total':len(rows),'quarantined':sum(classify(r)=='QUARANTINE_UNAPPROVED_MAPPING' for r in rows),'held':sum(classify(r)=='HOLD_OWNER' for r in rows),'fingerprints':len({fingerprint(r) for r in rows})}
class Tests(unittest.TestCase):
 def test_canonical_count(self):self.assertEqual(verify(ROWS),{'total':15,'quarantined':14,'held':1,'fingerprints':15})
 def test_deterministic_hash(self):self.assertEqual(fingerprint(ROWS[0]),fingerprint(dict(reversed(list(ROWS[0].items())))))
 def test_source_change_detected(self):
  changed=dict(ROWS[0]);changed['state']+=' changed';self.assertNotEqual(fingerprint(changed),fingerprint(ROWS[0]))
 def test_duplicate_rejected(self):
  with self.assertRaisesRegex(ValueError,'duplicate'):verify(ROWS+[ROWS[0]])
 def test_missing_rejected(self):
  with self.assertRaisesRegex(ValueError,'missing'):verify([{'id':'x'}])
 def test_invalid_priority_rejected(self):
  with self.assertRaisesRegex(ValueError,'priority'):verify([{**ROWS[0],'priority':'P9'}])
 def test_rentals_hold(self):self.assertEqual(classify(next(r for r in ROWS if r['id']=='WORK-RENTALS-001')),'HOLD_OWNER')
 def test_no_implicit_status_approval(self):self.assertTrue(all(classify(r)!='ACCEPT' for r in ROWS))
if __name__=='__main__':unittest.main()
