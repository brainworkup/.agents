---
name: browse-now
description: Browser automation CLI that controls the user's actual browser with their login sessions. Use it for authenticated websites, dynamic pages, form filling, screenshots, and browser tasks that web_search cannot reach. Prefer it whenever the task requires the user's real browser state, not a generic fetch. Do not use it for simple public page lookups.
---

# browse-now — Browser Automation CLI

You have `browse-now` on your PATH. It controls the user's actual browser with their login sessions.

Use it for authenticated sites, form filling, screenshots, and dynamic browser flows that web_search or simple fetches cannot reach.

Do not use it for simple public pages that web_search can answer faster.

This capability depends on the local browser bridge from the Nowledge Mem app plus the Exchange browser extension. It is local-only and is not exposed through Access Anywhere.

**Core loop**: open → snapshot → interact → snapshot again.
```
browse-now open <url>              # Open page
browse-now snapshot -i             # Get interactive elements (@e1, @e2...)
browse-now click @e5               # Click by ref
browse-now fill @e3 "text"         # Fill input by ref
browse-now get url                 # Verify where you landed
browse-now get page-text           # Read page content
```

Preferred interaction order:
- start with `snapshot -i`
- use refs like `@e5` as the primary interaction surface
- verify navigation with `browse-now get url` or `browse-now get title`
- re-snapshot after navigation or major DOM changes
- if accessibility data is sparse, try `find "query"`, `click -T "text"`, or `screenshot`

Run `browse-now --help` and `browse-now <command> --help` for all options (find, screenshot, scroll, type, press, etc.).
