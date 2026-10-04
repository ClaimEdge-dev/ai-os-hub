export type Attribution = {
  source_page: string;
  referrer: string;
  utm_source: string;
  utm_medium: string;
  utm_campaign: string;
  utm_content: string;
};

const KEY = "jct_attribution_v1";

export function captureAttribution(): Attribution {
  if (typeof window === "undefined") {
    return { source_page: "", referrer: "", utm_source: "", utm_medium: "", utm_campaign: "", utm_content: "" };
  }

  const qs = new URLSearchParams(window.location.search);
  const current: Attribution = {
    source_page: window.location.pathname,
    referrer: document.referrer || "",
    utm_source: qs.get("utm_source") || "",
    utm_medium: qs.get("utm_medium") || "",
    utm_campaign: qs.get("utm_campaign") || "",
    utm_content: qs.get("utm_content") || "",
  };

  try {
    const previous = JSON.parse(sessionStorage.getItem(KEY) || "{}") as Partial<Attribution>;
    const merged = {
      source_page: previous.source_page || current.source_page,
      referrer: previous.referrer || current.referrer,
      utm_source: previous.utm_source || current.utm_source,
      utm_medium: previous.utm_medium || current.utm_medium,
      utm_campaign: previous.utm_campaign || current.utm_campaign,
      utm_content: previous.utm_content || current.utm_content,
    };
    sessionStorage.setItem(KEY, JSON.stringify(merged));
    return merged;
  } catch {
    return current;
  }
}

export function getAttribution(): Attribution {
  if (typeof window === "undefined") return captureAttribution();
  try {
    return JSON.parse(sessionStorage.getItem(KEY) || "null") || captureAttribution();
  } catch {
    return captureAttribution();
  }
}
