# Root-route quick-win patch

Replace the current inline NotFoundComponent in `src/routes/__root.tsx` with:

```tsx
import { BrandedNotFound } from "@/components/site/BrandedNotFound";
```

Then set:

```tsx
notFoundComponent: BrandedNotFound,
```

This keeps the existing error boundary, auth listener, metadata, fonts, scripts and toaster unchanged while giving 404 traffic a branded Call Now recovery path.

Do not replace the rest of `__root.tsx`.
