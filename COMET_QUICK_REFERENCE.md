# Comet Browser — Quick Reference Guide

> Verified shortcuts, settings, and power user techniques for Comet (Perplexity's AI browser).

---

## Keyboard Shortcuts (Verified)

| Action | Shortcut |
|---|---|
| New tab | `Ctrl+T` |
| Close tab | `Ctrl+W` |
| Reopen closed tab | `Ctrl+Shift+T` |
| Next tab | `Ctrl+Tab` |
| Previous tab | `Ctrl+Shift+Tab` |
| Address bar | `Ctrl+L` |
| Find on page | `Ctrl+F` |
| Screenshot | `Ctrl+Shift+S` (if configured) |
| Developer tools | `F12` or `Ctrl+Shift+I` |
| Full screen | `F11` |
| Reload | `Ctrl+R` |
| Hard reload | `Ctrl+Shift+R` |

---

## Custom Shortcuts (Recommended Setup)

Configure these in Comet settings (`chrome://extensions/shortcuts` or Settings > Keyboard):

| Shortcut | Action |
|---|---|
| `Ctrl+Shift+1` | Screenshot + save to Drive |
| `Ctrl+Shift+2` | Copy page content |
| `Ctrl+Shift+3` | Save page to designated folder |
| `Ctrl+Shift+4` | Toggle browser tools |
| `Ctrl+Shift+5` | Quick Notion search |

---

## Power User Techniques

### 1. Batch Tab Operations
- Right-click tab bar → "Bookmark all tabs" for research sessions
- Use `Ctrl+Click` to select multiple tabs for batch operations

### 2. Session Management
- Save tab sessions with bookmark folders
- Name folders by date + task (e.g., "2026-07-16 Claims Research")

### 3. Screenshot Workflow
- Full page: `Ctrl+Shift+S` → "Capture full size"
- Element: Right-click → Inspect → Right-click element → Capture node screenshot
- Delayed: Open DevTools → `Ctrl+Shift+P` → "Capture full size screenshot"

### 4. Download Organization
- Set default download: `Settings > Downloads > Location`
- Create dated subfolders: `Drive/Comet-Downloads/2026-07-16/`

### 5. Search Operators (Within Perplexity)
- `site:github.com` — Limit to GitHub
- `filetype:pdf` — Find PDFs only
- `"exact phrase"` — Exact match
- `-exclude` — Exclude term
- `before:2026-01-01` — Date filter

---

## Known Limitations

1. **No extensions** — Comet doesn't support Chrome extensions (as of July 2026)
2. **Single Google account** — Can only be logged into one Google account at a time
3. **No incognito** — Private browsing not available in Comet beta
4. **Limited automation** — No built-in macro recorder (use Make.com or n8n instead)
5. **Captcha handling** — Comet can solve basic captchas but struggles with reCAPTCHA v3
6. **File upload** — Must upload files through Perplexity interface, not via browser
7. **Download limits** — Large file downloads may timeout (>100MB)

---

## Security Warnings

1. **Never save passwords** in Comet browser — use a password manager
2. **Always verify URLs** before entering credentials — phishing risk
3. **Clear cookies/cache** after sensitive sessions (`Ctrl+Shift+Delete`)
4. **Don't download** executables or scripts from untrusted sources
5. **Log out** of financial/sensitive accounts when done

---

## ROI Metrics from Power Users

| Task | Manual Time | With Comet | Time Saved |
|---|---|---|---|
| Drive inventory | 2 hours | 20 min | 83% |
| Notion audit | 1.5 hours | 15 min | 83% |
| Multi-site research | 3 hours | 45 min | 75% |
| Screenshot documentation | 1 hour | 15 min | 75% |
| File organization | 2 hours | 30 min | 75% |

---

## "Flexity" Clarification

**"Flexity" does NOT exist as a browser automation tool.**

- Flexity.io = Employee wellbeing platform (HR analytics)
- No tool named "Flexity" for browser automation exists

**Alternatives for browser automation:**
- **Browser Use** (browser-use.com) — Open source AI browser automation
- **n8n** — Workflow automation with browser triggers
- **Make.com** — Visual automation with HTTP/browser modules
- **Playwright** — Code-based browser automation (requires coding)
- **Comet itself** — Best for hands-free browsing within Perplexity

---

## Settings Checklist

Configure these before starting any audit:

- [ ] Default download location set to Google Drive
- [ ] Screenshot format: PNG (better quality than JPEG)
- [ ] Developer tools docked to right side
- [ ] Zoom level: 100% (for consistent screenshots)
- [ ] PDF viewer: Download instead of open
- [ ] Pop-ups: Allowed for trusted sites (Notion, GitHub)
- [ ] Autofill: Disabled for security
- [ ] Password saving: Disabled
- [ ] Cookie policy: Ask before accepting
