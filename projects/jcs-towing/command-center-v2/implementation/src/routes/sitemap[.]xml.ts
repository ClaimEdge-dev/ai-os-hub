import { createFileRoute } from "@tanstack/react-router";

const SAFE_PATHS = [
  "/",
  "/services",
  "/services/towing",
  "/service-area",
  "/reviews",
  "/about",
  "/contact",
  "/resources",
  "/resources/accident-checklist",
  "/resources/breakdown-checklist",
  "/privacy",
  "/accessibility",
];

export const Route = createFileRoute("/sitemap.xml")({
  server: {
    handlers: {
      GET: async ({ request }) => {
        const origin = new URL(request.url).origin;
        const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${SAFE_PATHS.map((p) => `  <url><loc>${origin}${p}</loc></url>`).join("\n")}\n</urlset>`;
        return new Response(body, { headers: { "content-type": "application/xml" } });
      },
    },
  },
});
