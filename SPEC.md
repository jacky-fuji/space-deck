# Orbital Dashboard — Functional Specification

> Version 1.0 / Last updated: 2026-03-02

---

## 1. Overview

Orbital Dashboard is a read-only, browser-based launch tracking tool. Its primary purpose is to give users a clear, at-a-glance view of upcoming rocket launches and an explorable archive of the complete orbital launch history.

---

## 2. Target Users

| User Type | Description |
|---|---|
| Space enthusiasts | Curious about past & upcoming launches |
| Engineers / Researchers | Quick lookup of historical mission data |
| General public | Accessible, bilingual interface (JP/EN) |

---

## 3. Functional Requirements

### 3.1 Navbar

| ID | Requirement |
|---|---|
| NAV-01 | Display the "ORBITAL" logo with a rocket icon |
| NAV-02 | Show a live system-status indicator (green pulse animation) |
| NAV-03 | Provide a JP ↔ EN language toggle button |
| NAV-04 | Sticky positioning at the top of the viewport |

### 3.2 Summary Widgets

| ID | Requirement |
|---|---|
| SUM-01 | **Total Launches** — display total count of all missions in dataset |
| SUM-02 | **Upcoming** — count of missions with status Scheduled / TBD / In Flight |
| SUM-03 | **Success Rate** — `(success / (success + failure)) × 100` as a percentage |

### 3.3 Mission Log

| ID | Requirement |
|---|---|
| LOG-01 | Two tabs: **Upcoming** (sorted ascending by date) and **Past** (sorted descending) |
| LOG-02 | Display columns: Date, Mission Name, Rocket, Launch Site, Status |
| LOG-03 | Desktop: table layout. Mobile (< md): card layout |
| LOG-04 | Status badges: `Success` (green), `Failure` (red), `Scheduled` (blue), `TBD` (yellow), `In Flight` (amber), `Partial Failure` (orange) |
| LOG-05 | Mission type badges: Crew, Cargo, Satellite, Test Flight, Technology Demo, Science, Commercial |
| LOG-06 | Initial display: **50 records**. Load More button adds 100 at a time |
| LOG-07 | Paginator shows remaining count: e.g. `(4,018 remaining)` |
| LOG-08 | Language switch toggles mission name and rocket name to Japanese where available |
| LOG-09 | Tab switch resets visible count to 50 |

### 3.4 Launch Site Map

| ID | Requirement |
|---|---|
| MAP-01 | World map using Leaflet (OpenStreetMap tiles) |
| MAP-02 | Display pins for all known launch sites (70+) |
| MAP-03 | Clicking a pin shows a tooltip: site name, country, coordinates, active missions count |
| MAP-04 | Map loads dynamically (SSR disabled) to avoid Leaflet `window` errors |
| MAP-05 | Map height: 400px, full width |

### 3.5 Internationalization (i18n)

| ID | Requirement |
|---|---|
| I18N-01 | All UI labels, headings, and status text available in English and Japanese |
| I18N-02 | Mission names use Japanese (`missionNameJP`) when `lang === "ja"` and available |
| I18N-03 | Rocket names use Japanese (`rocketNameJP`) when `lang === "ja"` and available |
| I18N-04 | Dates formatted with `toLocaleDateString` per active locale |

---

## 4. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | Initial page load < 3s on standard broadband |
| Scalability | Mission log must handle 10,000+ records without UI freeze (paginated render) |
| Accessibility | Semantic HTML, sufficient color contrast |
| Responsiveness | Fully usable on mobile (≥ 375px) and desktop |
| Browser Support | Latest Chrome, Firefox, Safari, Edge |

---

## 5. Data

### 5.1 Mission Status Values

| Value | Meaning |
|---|---|
| `Scheduled` | Launch confirmed with a date |
| `TBD` | Date or parameters not yet confirmed |
| `In Flight` | Currently in progress |
| `Success` | Launch completed successfully |
| `Failure` | Launch failed |
| `Partial Failure` | Launch partially successful |

### 5.2 Mission Type Values

`Crew` · `Cargo` · `Satellite` · `Test Flight` · `Technology Demo` · `Science` · `Commercial`

### 5.3 Data Sources

| Dataset | Source | Update Frequency |
|---|---|---|
| Historical missions | [GCAT launch.tsv](https://planet4589.org/space/gcat/tsv/launch/launch.tsv) | Manual re-run of extraction script |
| Japanese mission names | [JAXA 打上げ実績](https://www.jaxa.jp/projects/result_j.html) | Manual |
| Launch sites | GCAT sites.html + user-curated list | Manual |

---

## 6. Phase 2: Functional Roadmap & Architecture

To address the depth of global spaceflight data, the application will shift from a Single-Page Application (SPA) dashboard to a multi-page interconnected database architecture.

### 6.1 Status Legend

- 🟢 **[Implemented]**: Currently live in production.
- 🔵 **[In Progress]**: Development actively underway.
- 🟡 **[Not Implemented]**: Planned for future development sprints.

### 6.2 Proposed Page Architecture (App Router)

| Page Route | Status | Description |
|---|---|---|
| `/` (Home) | 🟢 | High-level summary, next upcoming launch countdown, global map. |
| `/launches/*` | 🟡 | Dedicated tabular logs for Upcoming and Past (migrated from Home). |
| `/launches/[id]` | 🟡 | Deep-dive mission specific page (payload mass, orbit targets, weather GO/NO-GO). |
| `/providers/[slug]`| 🟡 | Agency/Company profiles (SpaceX, NASA) with historic fleet success curves. |
| `/vehicles/[slug]` | 🟡 | Rocket encyclopedia with technical specs and booster-stage reuse history. |
| `/locations/[slug]`| 🟡 | Spaceport details, listing active launch complexes (Pads) and resident providers. |
| `/astronauts` | 🟡 | Human Spaceflight tracking (ISS/Tiangong active crew manifests). |

### 6.3 Future Functional Integrations

| Feature | Status | Requirement Outline |
|---|---|---|
| **LL2 API Webhooks** | 🟡 | Replace static `missions.json` upcoming data with real-time Launch Library 2 (LL2) queries for instant schedule slips/scrubs. |
| **Live Media Embed** | 🟡 | Automatically fetch and embed official YouTube/Twitch streams during the `T-1H` launch window. |
| **Calendar Sync** | 🟡 | Generate `.ics` files and Google Calendar API deep-links for users to export launch schedules. |
| **Advanced Filtering** | 🟡 | Text-based search bar for historic payloads, year-range sliders, and orbital parameter filters (LEO vs GEO). |
| **PWA Support** | 🟡 | Manifest and Service Worker implementation for offline access and native push notifications. |
