#!/usr/bin/env python3
"""R149-001: deterministic, no-I/O connector permission/cost preflight.

All booleans/scopes/tenants must be backed by fresh tool/account readbacks.
This policy gate cannot authenticate or inspect a live vendor permission.
It never logs secrets, makes requests, spends, writes, or contacts anyone.
"""
from collections.abc import Mapping

OPERATIONS = frozenset({"public_read", "private_read", "write", "send", "deploy", "delete", "access_change"})
PRIVATE_OPERATIONS = frozenset({"private_read", "write", "send", "deploy", "delete", "access_change"})
HIGH_IMPACT = frozenset({"send", "deploy", "delete", "access_change"})
SENSITIVE = frozenset({"secret", "client", "minor", "health", "financial", "internal"})

def evaluate_route(request):
    """Return only a sanitized decision, never the original inputs.

    Caller-supplied 'verified' flags must come from actual current permission,
    identity, cost and tenant evidence; they are not evidence on their own.
    """
    if not isinstance(request, Mapping):
        raise TypeError("route request must be a mapping")

    operation = request.get("operation")
    if operation not in OPERATIONS:
        return {"allowed": False, "decision": "BLOCK", "reason_codes": ["INVALID_OPERATION"],
                "tool": str(request.get("tool") or "")[:80], "operation": "UNKNOWN"}
    tool = str(request.get("tool") or "").strip()[:80]
    reasons = []
    if not tool:
        reasons.append("TOOL_ID_MISSING")
    if request.get("action_exposed") is not True or request.get("capability_verified") is not True:
        reasons.append("ACTION_NOT_VERIFIED")

    if operation in PRIVATE_OPERATIONS:
        if request.get("identity_verified") is not True:
            reasons.append("IDENTITY_UNVERIFIED")
        if request.get("authorization_verified") is not True:
            reasons.append("AUTHORIZATION_UNVERIFIED")
        required_scope = str(request.get("required_scope") or "").strip()
        granted_scopes = request.get("granted_scopes")
        if not required_scope or not isinstance(granted_scopes, (tuple, list, set, frozenset)) or required_scope not in granted_scopes:
            reasons.append("SCOPE_NOT_VERIFIED")
        expected_tenant = str(request.get("expected_tenant") or "").strip()
        observed_tenant = str(request.get("observed_tenant") or "").strip()
        if not expected_tenant or not observed_tenant or expected_tenant != observed_tenant:
            reasons.append("TENANT_NOT_VERIFIED")

    metered = request.get("metered") is True
    cost = request.get("estimated_cost_usd")
    # Non-public side effects must include a verified bounded cost estimate,
    # including an explicit numeric zero when the operation is confirmed free.
    cost_needed = (metered or operation in {"write", "send", "deploy",
                                           "delete", "access_change"}
                   or request.get("external_transfer") is True)
    if cost_needed or cost is not None:
        if isinstance(cost, bool) or not isinstance(cost, (int, float)) or cost < 0 or cost != cost or cost == float("inf"):
            reasons.append("COST_NOT_VERIFIED")
        elif cost > 0 and request.get("spend_approved") is not True:
            reasons.append("COST_APPROVAL_REQUIRED")

    if operation in HIGH_IMPACT and request.get("owner_approved") is not True:
        reasons.append("OWNER_APPROVAL_REQUIRED")
    if operation == "send" and request.get("customer_contact_allowed") is not True:
        reasons.append("CUSTOMER_CONTACT_HELD")

    # Caller assertion is not proof: require a boolean transfer intent and
    # an explicit, recognized, nonempty classification for each export.
    transfer_flag = request.get("external_transfer", False)
    if not isinstance(transfer_flag, bool):
        reasons.append("EXTERNAL_TRANSFER_UNVERIFIED")
        external = False
    else:
        external = transfer_flag
    raw_classes = request.get("data_classes")
    allowed_classes = SENSITIVE | frozenset({"public"})
    if raw_classes is None:
        classes = frozenset()
    elif (isinstance(raw_classes, (tuple, list, set, frozenset))
          and all(isinstance(item, str) and item in allowed_classes
                  for item in raw_classes)):
        classes = frozenset(raw_classes)
    else:
        reasons.append("DATA_CLASS_UNVERIFIED")
        classes = frozenset()
    # Do not treat an empty or unknown class list as public information.
    if external:
        if not classes or request.get("data_classes_verified") is not True:
            reasons.append("DATA_CLASS_UNVERIFIED")
        if request.get("destination_verified") is not True:
            reasons.append("DESTINATION_NOT_VERIFIED")
    if "secret" in classes:
        reasons.append("SECRET_TRANSFER_PROHIBITED")
    if external and (classes & SENSITIVE):
        if request.get("data_release_approved") is not True or request.get("destination_verified") is not True:
            reasons.append("SENSITIVE_TRANSFER_NOT_AUTHORIZED")

    if reasons:
        return {"allowed": False, "decision": "BLOCK", "reason_codes": reasons,
                "tool": tool, "operation": operation}
    return {"allowed": True, "decision": "ALLOW_READ_ONLY" if operation in {"public_read", "private_read"}
            else "ALLOW_SCOPED_ACTION", "reason_codes": [], "tool": tool, "operation": operation}
