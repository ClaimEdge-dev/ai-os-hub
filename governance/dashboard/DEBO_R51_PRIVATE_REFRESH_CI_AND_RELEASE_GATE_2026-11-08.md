# DEBO R51 | Private refresh CI and deployment gate
2026-11-08 America/Chicago. Mission DEBO-MASTER-031.
R50 server prototype committed at c72c2a285bf8921176925d003836d160ba047981; eight test cases at a92e289e0e633ac6e1cf3f44bc6a1e2820aaedc4.
R51 added .github/workflows/debo-r50-private-endpoint-ci.yml at c90b94c66a33efd85ed620addad9aee404ca05d7. It runs R50 endpoint tests and existing snapshot tests on nonproduction branch changes.
Evidence status: CI WORKFLOW COMMITTED, not yet read back as PASS. Existing R49 HTML is a static snapshot, not a live server-connected dashboard. No Neon credentials have been issued or stored, no private hosting configured, no public deployment performed.
Security design gate: loopback-only prototype is not reachable by remote iPhone; never embed API bearer token or database DSN in browser HTML. For device access, require authenticated private hosting or a user-controlled VPN/reverse proxy with real identity enforcement, TLS, read-only scoped Neon role, and owner-approved deployment. Do not make the service public without these.
Next: confirm CI pass, select approved private host and secure device identity, configure credentials through provider secret storage, verify end-to-end auth + task counts, then mark live only after remote readback.
Checkpoint R51-CI-WORKFLOW-COMMITTED-PRIVATE-HOST-UNCONFIGURED-NOT-LIVE.
