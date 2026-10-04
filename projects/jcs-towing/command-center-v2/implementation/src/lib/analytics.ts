export type JctEventName =
  | "call_click"
  | "request_service_click"
  | "request_form_start"
  | "request_form_error"
  | "request_form_submit"
  | "request_form_success"
  | "get_location_click"
  | "geolocation_granted"
  | "geolocation_denied"
  | "service_selected"
  | "review_click"
  | "directions_click";

export type JctEventPayload = Record<string, string | number | boolean | null | undefined>;

declare global {
  interface Window {
    dataLayer?: Array<Record<string, unknown>>;
  }
}

/**
 * Provider-neutral analytics bridge.
 * It sends nothing off-device by itself.
 * If a future approved analytics provider creates window.dataLayer,
 * events are also pushed there.
 */
export function trackJctEvent(name: JctEventName, payload: JctEventPayload = {}) {
  if (typeof window === "undefined") return;
  const event = {
    event: `jct_${name}`,
    path: window.location.pathname,
    ...payload,
  };

  if (Array.isArray(window.dataLayer)) window.dataLayer.push(event);
  window.dispatchEvent(new CustomEvent("jct:analytics", { detail: event }));
}
