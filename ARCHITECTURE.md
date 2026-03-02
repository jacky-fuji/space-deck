# Orbital Dashboard — Architecture

> Version 1.0 / Last updated: 2026-03-02

---

## 1. Overview

Orbital Dashboard is a **statically rendered Next.js application**. All mission data is pre-processed into a static JSON file at development time, so no backend server or database is required at runtime.

```
Browser ──► Next.js (App Router, Static Export)
              │
              ├── page.tsx  (all UI + state)
              ├── LaunchMap.tsx  (dynamic Leaflet component)
              └── data/missions.json  (4,100+ missions, ~1 MB)
```

---

## 2. Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Framework | **Next.js 16** (App Router) | Static site generation (SSG) |
| Language | **TypeScript 5** | Strict mode |
| Styling | **Tailwind CSS 4** | Utility-first, no CSS modules |
| Map | **Leaflet + react-leaflet 5** | Dynamic import (SSR disabled) |
| Icons | **lucide-react** | Tree-shakeable SVG icons |
| Runtime | **Node.js 20+** | Dev & build only |

---

## 3. Directory Structure

```
space-deck/
├── src/
│   └── app/
│       ├── layout.tsx            # Root layout, metadata (title, OG, fonts)
│       ├── page.tsx              # Main page — all UI components, state, data
│       ├── globals.css           # CSS custom properties, animations
│       ├── components/
│       │   └── LaunchMap.tsx     # Leaflet map (dynamically imported, no SSR)
│       └── data/
│           └── missions.json     # Pre-processed mission dataset (~4,100 records)
├── public/                       # Static assets (favicon, etc.)
├── scripts/                      # (Recommended) Data processing scripts
│   ├── process_gcat.py           # GCAT TSV → JSON extraction
│   └── merge_jaxa.py             # Merge JAXA Japanese names
├── SPEC.md
├── ARCHITECTURE.md
├── README.md
└── LICENSE
```

---

## 4. Data Pipeline

Historical mission data is **not fetched at runtime**. It is pre-processed offline and committed as `missions.json`.

```
GCAT launch.tsv (planet4589.org)
    │
    ▼ process_gcat.py
    │   Filter: Category contains 'O' (orbital) or 'F' (failed orbital)
    │   Parse: date → ISO 8601, site code → siteId slug
    │   Output: 4,100+ Mission objects
    │
    ▼ merge_jaxa.py
    │   Input: JAXA HTML scrape (scratchpad JSON)
    │   Match by date + Japanese rocket/provider patterns
    │   Enrich: missionNameJP, rocketNameJP fields
    │
    ▼ src/app/data/missions.json  (~914 KB)
```

To refresh the dataset:

```bash
curl -L https://planet4589.org/space/gcat/tsv/launch/launch.tsv -o /tmp/launch.tsv
python3 scripts/process_gcat.py
python3 scripts/merge_jaxa.py
```

---

## 5. Component Architecture

All UI is currently co-located in `page.tsx` as a single-file component for simplicity. The recommended decomposition for scaling is:

```
page.tsx   (OrbitalDashboard — root state owner)
├── Navbar
├── SummaryWidgets
│   ├── TotalLaunchesWidget
│   ├── UpcomingWidget
│   └── SuccessRateWidget
├── MissionLog
│   ├── TabBar
│   ├── MissionTable   (md+)
│   ├── MissionCards   (< md)
│   └── LoadMoreButton
└── LaunchMap   (dynamic, Leaflet)
```

### Key State

| State | Type | Location | Purpose |
|---|---|---|---|
| `lang` | `"en" \| "ja"` | `OrbitalDashboard` | UI language |
| `activeTab` | `"upcoming" \| "past"` | `OrbitalDashboard` | Mission log tab |
| `visibleCount` | `number` | `OrbitalDashboard` | Pagination cursor |

### Key Memos

| Memo | Deps | Purpose |
|---|---|---|
| `upcoming` | `[]` | Filter + sort upcoming missions once |
| `past` | `[]` | Filter + sort past missions once |
| `paginatedMissions` | `[activeMissions, visibleCount]` | Slice for rendering |
| `mapMissions` | `[lang]` | Map-ready mission list with localized names |

---

## 6. Rendering Strategy

| Page | Strategy | Reason |
|---|---|---|
| `/` | **Static (SSG)** | No runtime data fetch required |
| LaunchMap | **Client-only** | Leaflet uses `window`/`document` APIs |

The app is deployable as a **pure static site** (`next export`) to any CDN (Vercel, Netlify, GitHub Pages, etc.).

---

## 7. Performance Considerations

| Concern | Current Approach | Future Option |
|---|---|---|
| Large mission list (4,100+) | Client-side pagination (50 + 100/click) | Virtual scroll (react-window) |
| missions.json (~1 MB) | Bundled as static import | Split by year, lazy-load chunks |
| Map tile loading | OpenStreetMap CDN | Self-hosted tiles, or Mapbox |
| JP name data | Inline in missions.json | Separate `missions-jp.json`, lazy-loaded |

---

## 8. Planned Architecture Evolution (Phase 2)

Currently, Orbital Dashboard is a Single-Page Application (SPA) driven by a monolithic `page.tsx` pulling from a static `missions.json`.

Phase 2 will decentralize this into a **Multi-Page App Router Architecture**:

### 8.1 Multi-Page Routing Architecture

```
src/app/
├── globals.css
├── layout.tsx                # Shared Navigation & Footer
├── page.tsx                  # Home: Hero Countdown, Maps, Widgets
├── launches/
│   ├── upcoming/page.tsx     # Full Upcoming Log
│   ├── past/page.tsx         # Full Historic Log
│   └── [id]/page.tsx         # Deep-dive: Specific mission parameters
├── providers/
│   └── [slug]/page.tsx       # Deep-dive: Agency/Company profiles & fleets
├── vehicles/
│   └── [slug]/page.tsx       # Deep-dive: Rocket family specs & booster history
├── locations/
│   └── [slug]/page.tsx       # Deep-dive: Spaceport pads & activity
└── astronauts/
    └── page.tsx              # Active ISS/Tiangong crew tracking
```

### 8.2 Data Fetching Strategy (Phase 2)

```
Browser
  └── App Router Pages
        ├── Static SSG (missions.json)    ← Historic Archive (/launches/past, /vehicles)
        └── Client-side SWR / React Query ← Live Data (/launches/upcoming, /astronauts)
              └── Launch Library 2 (LL2) API
```

By decoupling the historical archive (static SSG) from the upcoming schedule (dynamic client fetch), the app can maintain ultra-fast load times while ensuring schedule slips are refected in near real-time.

---

## 9. Environment Variables

Currently none required. Future additions for Phase 2:

| Variable | Purpose |
|---|---|
| `NEXT_PUBLIC_LL2_API_KEY` | Launch Library 2 API key (if rate-limited) |
| `NEXT_PUBLIC_MAPBOX_TOKEN` | Mapbox tile token (if switching from OSM) |
