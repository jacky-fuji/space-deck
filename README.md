# 🛰️ Orbital Dashboard

> A real-time rocket launch tracking dashboard — sleek, minimal, and space-themed.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)

## Overview

**Orbital Dashboard** is a web application that visualizes global rocket launch schedules and historical mission data. It features an interactive world map with launch site pins, a bilingual UI (JP/EN), and a comprehensive mission log covering 4,000+ orbital launches dating back to Sputnik 1 (1957).

## Features

- 🗺️ **Interactive Launch Map** — Leaflet-powered world map with 70+ global launch sites and tooltips
- 📋 **Mission Log** — Upcoming & historical launches with pagination ("Load More")
- 📊 **Summary Widgets** — Total launches, upcoming count, success rate
- 🌏 **Bilingual UI** — Full English / Japanese toggle (JP/EN)
- 🕐 **4,100+ Historical Missions** — Sourced from [GCAT (planet4589.org)](https://planet4589.org/space/gcat/) and JAXA
- 🎨 **Dark, minimal design** — SF-instrument aesthetic with subtle animations

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript 5 |
| Styling | Tailwind CSS 4 |
| Map | Leaflet + react-leaflet |
| Icons | lucide-react |
| Data | GCAT TSV + JAXA HTML (static JSON) |

## Getting Started

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

```bash
# Production build
npm run build
npm run start
```

## Data Sources

| Source | Description |
|---|---|
| [GCAT — planet4589.org](https://planet4589.org/space/gcat/) | ~6,800 orbital launch records (TSV) |
| [JAXA Launch Results](https://www.jaxa.jp/projects/result_j.html) | Japanese missions with JP names (1970–present) |

Historical mission data is pre-processed into `src/app/data/missions.json` at build time.

## Project Structure

```
space-deck/
├── src/app/
│   ├── page.tsx            # Main dashboard page & all UI components
│   ├── layout.tsx          # Root layout & metadata
│   ├── globals.css         # Global styles & animations
│   ├── components/
│   │   └── LaunchMap.tsx   # Leaflet map component (dynamic import)
│   └── data/
│       └── missions.json   # Pre-processed launch history (~4,100 records)
├── SPEC.md                 # Functional specification
├── ARCHITECTURE.md         # Technical architecture
└── LICENSE                 # MIT
```

## License

[MIT](./LICENSE) © 2026 Junichi Fujinuma
