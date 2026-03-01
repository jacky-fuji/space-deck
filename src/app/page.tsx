"use client";

import { useState, useMemo, useEffect } from "react";
import dynamic from "next/dynamic";
import {
  Rocket,
  CalendarClock,
  TrendingUp,
  CheckCircle2,
  Clock,
  XCircle,
  MapPin,
  Globe,
  Activity,
  ChevronRight,
  Map,
  Filter,
} from "lucide-react";
import type { LaunchSite, MapMission } from "./components/LaunchMap";
import missionsData from "./data/missions.json";

// Dynamic import — Leaflet requires window
const LaunchMap = dynamic(() => import("./components/LaunchMap"), {
  ssr: false,
  loading: () => <div className="h-[400px] w-full" />,
});

const LaunchHistoryChart = dynamic(
  () => import("./components/LaunchHistoryChart"),
  { ssr: false, loading: () => <div className="h-[380px] w-full" /> }
);

// ─── Types ───────────────────────────────────────────────────────────────────

type MissionStatus =
  | "Scheduled"
  | "Success"
  | "Partial Failure"
  | "Failure"
  | "In Flight"
  | "TBD";

type MissionType =
  | "Crew"
  | "Cargo"
  | "Satellite"
  | "Test Flight"
  | "Technology Demo"
  | "Science"
  | "Commercial";

interface Mission {
  id: string;
  date: string;
  missionName: string;
  missionNameJP?: string;
  missionType: MissionType;
  rocketName: string;
  rocketNameJP?: string;
  provider: string;
  location: string;
  siteId: string;
  status: MissionStatus;
}

const allMissions = missionsData as Mission[];

// ─── Launch Sites ────────────────────────────────────────────────────────────

const launchSites: LaunchSite[] = [
  { id: "alcantara", name: "アルカンタラ射場", country: "Brazil", lat: -2.3155, lng: -44.3676 },
  { id: "andoya", name: "アンドーヤ宇宙センター", country: "Norway", lat: 69.2943, lng: 16.0207 },
  { id: "woomera", name: "ウーメラ試験場", country: "Australia", lat: -30.9567, lng: 136.5222 },
  { id: "esrange", name: "エスレンジ宇宙センター", country: "Sweden", lat: 67.8939, lng: 21.1069 },
  { id: "kourou", name: "ギアナ宇宙センター", country: "French Guiana", lat: 5.2372, lng: -52.7606 },
  { id: "ksc", name: "ケネディ宇宙センター (KSC)", country: "USA", lat: 28.5728, lng: -80.6490 },
  { id: "cape-canaveral", name: "ケープカナベラル宇宙軍施設 (CCSFS)", country: "USA", lat: 28.4889, lng: -80.5778 },
  { id: "southampton", name: "サウサンプトン地域 (Airborne Launch)", country: "UK", lat: 50.4850, lng: -5.0000 },
  { id: "sriharikota", name: "サティシュ・ダワン宇宙センター", country: "India", lat: 13.7330, lng: 80.2304 },
  { id: "boca-chica", name: "スターベース (ボカチカ)", country: "USA", lat: 25.9972, lng: -97.1558 },
  { id: "kushimoto", name: "スペースポート紀伊", country: "Japan", lat: 33.5591, lng: 135.8458 },
  { id: "semnan", name: "セムナーン宇宙センター", country: "Iran", lat: 35.2346, lng: 53.9209 },
  { id: "sohae", name: "ソヘエ衛星発射場", country: "North Korea", lat: 39.6600, lng: 124.7053 },
  { id: "baikonur", name: "バイコヌール宇宙基地", country: "Kazakhstan", lat: 45.9646, lng: 63.3052 },
  { id: "kodiak", name: "パシフィック・スペースポート・コンプレックス", country: "USA", lat: 57.4358, lng: -152.3378 },
  { id: "palmachim", name: "パルマチン空軍基地", country: "Israel", lat: 31.8848, lng: 34.6802 },
  { id: "plesetsk", name: "プレセツク宇宙基地", country: "Russia", lat: 62.9255, lng: 40.5777 },
  { id: "vostochny", name: "ボストーチヌイ宇宙基地", country: "Russia", lat: 51.8844, lng: 128.3340 },
  { id: "mahia", name: "マヒア半島宇宙港 (Rocket Lab)", country: "New Zealand", lat: -39.2610, lng: 177.8640 },
  { id: "yasny", name: "ヤースヌイ宇宙基地", country: "Russia", lat: 51.0000, lng: 59.8333 },
  { id: "wallops", name: "ワロップス飛行施設", country: "USA", lat: 37.8330, lng: -75.4834 },
  { id: "vandenberg", name: "ヴァンデンバーグ宇宙軍基地", country: "USA", lat: 34.7420, lng: -120.5724 },
  { id: "uchiinoura", name: "内之浦宇宙空間観測所", country: "Japan", lat: 31.2510, lng: 131.0790 },
  { id: "taiyuan", name: "太原衛星発射センター", country: "China", lat: 38.8489, lng: 111.6080 },
  { id: "wenchang", name: "文昌宇宙ロケット発射場", country: "China", lat: 19.6143, lng: 110.9511 },
  { id: "haiyang", name: "海陽東方航天港", country: "China", lat: 36.7113, lng: 121.1963 },
  { id: "tanegashima", name: "種子島宇宙センター", country: "Japan", lat: 30.3995, lng: 130.9722 },
  { id: "naro", name: "羅老宇宙センター", country: "South Korea", lat: 34.4319, lng: 127.5350 },
  { id: "xichang", name: "西昌衛星発射センター", country: "China", lat: 28.2460, lng: 102.0265 },
  { id: "jiuquan", name: "酒泉衛星発射センター", country: "China", lat: 40.9605, lng: 100.2983 },
  { id: "taiki", name: "北海道スペースポート", country: "Japan", lat: 42.5044, lng: 143.4421 },
  { id: "arnhem", name: "アーンエム宇宙センター", country: "Australia", lat: -12.3900, lng: 136.8000 },
  { id: "asx", name: "アトランティック宇宙港", country: "Canada", lat: 46.8981, lng: -55.3479 },
  { id: "bowen", name: "ボーウェン軌道宇宙港", country: "Australia", lat: -19.9582, lng: 148.1136 },
  { id: "canso", name: "キャンソ宇宙港", country: "Canada", lat: 45.3036, lng: -60.9829 },
  { id: "chabahar", name: "チャバハール宇宙センター", country: "Iran", lat: 25.1408, lng: 61.2719 },
  { id: "etlaq", name: "エトラック宇宙港", country: "Oman", lat: 19.6396, lng: 57.6780 },
  { id: "hcsls", name: "海南商業ロケット発射場", country: "China", lat: 19.5968, lng: 110.9308 },
  { id: "rize", name: "リゼ・アルトヴィン空港", country: "Turkey", lat: 41.1692, lng: 40.8289 },
  { id: "svalrak", name: "スヴァルラック・ロケット射場", country: "Norway", lat: 78.9315, lng: 11.8504 },
  { id: "saxavord", name: "サクサボード宇宙港", country: "UK", lat: 60.8190, lng: -0.8440 },
  { id: "sutherland", name: "サザランド・スペースハブ", country: "UK", lat: 58.5130, lng: -4.5120 },
  { id: "spaceport-america", name: "スペースポート・アメリカ", country: "USA", lat: 32.9900, lng: -106.9750 },
  { id: "corn-ranch", name: "コーン・ランチ (Blue Origin)", country: "USA", lat: 31.4220, lng: -104.7570 },
  { id: "mojave", name: "モハベ空港", country: "USA", lat: 35.0590, lng: -118.1510 },
  { id: "santa-maria", name: "サンタマリア射場", country: "Portugal", lat: 36.9850, lng: -25.1260 },
  { id: "el-hierro", name: "エル・イエロ打ち上げセンター", country: "Spain", lat: 27.6410, lng: -17.9910 },
  { id: "grottaglie", name: "タラント・グロッターリエ空港", country: "Italy", lat: 40.5170, lng: 17.4030 },
  { id: "qom", name: "コム (Qom)", country: "Iran", lat: 34.6400, lng: 50.8760 },
  { id: "shahroud", name: "シャールード宇宙センター", country: "Iran", lat: 36.4200, lng: 55.0200 },
  { id: "sonmiani", name: "ソンミアニ試験場", country: "Pakistan", lat: 25.4220, lng: 66.6000 },
  { id: "tilla", name: "ティラ (Tilla) 試験場", country: "Pakistan", lat: 33.3960, lng: 73.2960 },
  { id: "abdul-kalam", name: "アブドゥル・カラム島", country: "India", lat: 20.7580, lng: 87.0850 },
  { id: "nantian", name: "南田 (Nantian) 発射場", country: "Taiwan", lat: 22.2620, lng: 120.8900 },
  { id: "biak", name: "ビアク島スペースポート", country: "Indonesia", lat: -1.0000, lng: 136.0000 },
  { id: "broglio", name: "ブローリオ宇宙センター", country: "Kenya", lat: -2.9400, lng: 40.2130 },
  { id: "sabha", name: "サブハ / タウィワ", country: "Libya", lat: 26.9930, lng: 14.4640 },
  { id: "overberg", name: "オーバーベルグ試験場", country: "South Africa", lat: -34.6020, lng: 20.3020 },
];

// ─── i18n ────────────────────────────────────────────────────────────────────

const translations = {
  en: {
    totalLaunches: "Total Launches (2026)",
    next30Days: "Next 30 Days",
    successRate: "Success Rate",
    upcoming: "Upcoming",
    past: "Past",
    date: "Date",
    mission: "Mission",
    rocket: "Rocket / Provider",
    location: "Location",
    status: "Status",
    missionLog: "Mission Log",
    systemOnline: "System Online",
    launches: "launches",
    scheduled: "scheduled",
    launchSites: "Launch Sites",
    launchSitesDesc: "Worldwide spaceport locations",
    all: "All",
    filterYear: "Year",
    filterCountry: "Country",
    filterStatus: "Status",
  },
  ja: {
    totalLaunches: "年間打ち上げ数 (2026)",
    next30Days: "直近30日の予定",
    successRate: "成功率",
    upcoming: "今後の予定",
    past: "過去の実績",
    date: "日付",
    mission: "ミッション",
    rocket: "ロケット / 機関",
    location: "打ち上げ場所",
    status: "ステータス",
    missionLog: "ミッションログ",
    systemOnline: "システムオンライン",
    launches: "回",
    scheduled: "件の予定",
    launchSites: "発射場マップ",
    launchSitesDesc: "世界の宇宙港",
    all: "すべて",
    filterYear: "年",
    filterCountry: "国",
    filterStatus: "ステータス",
  },
} as const;

type Lang = keyof typeof translations;

// missionsData is imported from missions.json

// ─── Status Helpers ──────────────────────────────────────────────────────────

function getStatusConfig(status: MissionStatus) {
  switch (status) {
    case "Success":
      return {
        icon: CheckCircle2,
        color: "text-emerald-400",
        bg: "bg-emerald-400/10",
        border: "border-emerald-400/20",
      };
    case "Scheduled":
      return {
        icon: Clock,
        color: "text-sky-400",
        bg: "bg-sky-400/10",
        border: "border-sky-400/20",
      };
    case "TBD":
      return {
        icon: Clock,
        color: "text-amber-400",
        bg: "bg-amber-400/10",
        border: "border-amber-400/20",
      };
    case "In Flight":
      return {
        icon: Rocket,
        color: "text-violet-400",
        bg: "bg-violet-400/10",
        border: "border-violet-400/20",
      };
    case "Partial Failure":
      return {
        icon: XCircle,
        color: "text-amber-500",
        bg: "bg-amber-500/10",
        border: "border-amber-500/20",
      };
    case "Failure":
      return {
        icon: XCircle,
        color: "text-red-400",
        bg: "bg-red-400/10",
        border: "border-red-400/20",
      };
    default:
      return {
        icon: Clock,
        color: "text-neutral-400",
        bg: "bg-neutral-400/10",
        border: "border-neutral-400/20",
      };
  }
}

function StatusBadge({ status }: { status: MissionStatus }) {
  const cfg = getStatusConfig(status);
  const Icon = cfg.icon;
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${cfg.color} ${cfg.bg} ${cfg.border}`}
    >
      <Icon className="h-3 w-3" />
      {status}
    </span>
  );
}

function MissionTypeBadge({ type }: { type: MissionType }) {
  const colorMap: Record<MissionType, string> = {
    Crew: "text-violet-300 bg-violet-400/10 border-violet-400/20",
    Cargo: "text-teal-300 bg-teal-400/10 border-teal-400/20",
    Satellite: "text-blue-300 bg-blue-400/10 border-blue-400/20",
    "Test Flight": "text-orange-300 bg-orange-400/10 border-orange-400/20",
    "Technology Demo": "text-pink-300 bg-pink-400/10 border-pink-400/20",
    Science: "text-cyan-300 bg-cyan-400/10 border-cyan-400/20",
    Commercial: "text-neutral-300 bg-neutral-400/10 border-neutral-400/20",
  };
  return (
    <span
      className={`inline-flex rounded border px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-wider ${colorMap[type]}`}
    >
      {type}
    </span>
  );
}

// ─── Site Country Map ────────────────────────────────────────────────────────

const SITE_COUNTRY: Record<string, { flag: string; name: string; nameJP: string }> = {
  // USA
  "ksc": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "cape-canaveral": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "vandenberg": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "wallops": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "kodiak": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "spaceport-america": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "boca-chica": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "taiki": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "kushimoto": { flag: "🇯🇵", name: "Japan", nameJP: "日本" },
  // Russia
  "plesetsk": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "vostochny": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "yasny": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "kapustin-yar": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  // Kazakhstan
  "baikonur": { flag: "🇰🇿", name: "Kazakhstan", nameJP: "カザフスタン" },
  // Japan
  "tanegashima": { flag: "🇯🇵", name: "Japan", nameJP: "日本" },
  "uchiinoura": { flag: "🇯🇵", name: "Japan", nameJP: "日本" },
  // China
  "jiuquan": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "xichang": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "taiyuan": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "wenchang": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  // France (Guiana)
  "kourou": { flag: "🇫🇷", name: "France", nameJP: "フランス" },
  // India
  "sriharikota": { flag: "🇮🇳", name: "India", nameJP: "インド" },
  // South Korea
  "naro": { flag: "🇰🇷", name: "S. Korea", nameJP: "韓国" },
  // North Korea
  "sohae": { flag: "🇰🇵", name: "N. Korea", nameJP: "北朝鮮" },
  // New Zealand
  "mahia": { flag: "🇳🇿", name: "New Zealand", nameJP: "NZ" },
  // Israel
  "palmachim": { flag: "🇮🇱", name: "Israel", nameJP: "イスラエル" },
  // Iran
  "semnan": { flag: "🇮🇷", name: "Iran", nameJP: "イラン" },
  // Brazil
  "alcantara": { flag: "🇧🇷", name: "Brazil", nameJP: "ブラジル" },
  // Norway
  "andoya": { flag: "🇳🇴", name: "Norway", nameJP: "ノルウェー" },
  // Sweden
  "esrange": { flag: "🇸🇪", name: "Sweden", nameJP: "スウェーデン" },
  // Australia
  "woomera": { flag: "🇦🇺", name: "Australia", nameJP: "豪州" },
  // Oman
  "oman": { flag: "🇴🇲", name: "Oman", nameJP: "オマーン" },
};

// Fallback: map raw GCAT site codes to country
const GCAT_COUNTRY: Record<string, { flag: string; name: string; nameJP: string }> = {
  // USA
  "CC": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "KSC": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "V": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "WI": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "AS": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "SA": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  "BOC": { flag: "🇺🇸", name: "USA", nameJP: "米国" },
  // Russia
  "PL": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "VO": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "DOM": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "KY": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "NIIP-53": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "GIK-1": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "PLK": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  "VOSTO": { flag: "🇷🇺", name: "Russia", nameJP: "ロシア" },
  // Kazakhstan
  "B": { flag: "🇰🇿", name: "Kazakhstan", nameJP: "カザフスタン" },
  "NIIP-5": { flag: "🇰🇿", name: "Kazakhstan", nameJP: "カザフスタン" },
  "GIK-5": { flag: "🇰🇿", name: "Kazakhstan", nameJP: "カザフスタン" },
  // Japan
  "T": { flag: "🇯🇵", name: "Japan", nameJP: "日本" },
  "K": { flag: "🇯🇵", name: "Japan", nameJP: "日本" },
  "U": { flag: "🇯🇵", name: "Japan", nameJP: "日本" },
  // China
  "J": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "JQ": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "X": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "XSC": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "TY": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "TSC": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "W": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  "WSC": { flag: "🇨🇳", name: "China", nameJP: "中国" },
  // France / Guiana
  "CSG": { flag: "🇫🇷", name: "France", nameJP: "フランス" },
  "KO": { flag: "🇫🇷", name: "France", nameJP: "フランス" },
  // India
  "SRI": { flag: "🇮🇳", name: "India", nameJP: "インド" },
  // South Korea
  "NARO": { flag: "🇰🇷", name: "S. Korea", nameJP: "韓国" },
  // North Korea
  "SO": { flag: "🇰🇵", name: "N. Korea", nameJP: "北朝鮮" },
  // New Zealand
  "MAH": { flag: "🇳🇿", name: "New Zealand", nameJP: "NZ" },
  // Israel
  "PM": { flag: "🇮🇱", name: "Israel", nameJP: "イスラエル" },
  // Iran
  "SEM": { flag: "🇮🇷", name: "Iran", nameJP: "イラン" },
  // Brazil
  "AL": { flag: "🇧🇷", name: "Brazil", nameJP: "ブラジル" },
  // Norway
  "AND": { flag: "🇳🇴", name: "Norway", nameJP: "ノルウェー" },
  // Sweden
  "ESR": { flag: "🇸🇪", name: "Sweden", nameJP: "スウェーデン" },
  // Australia
  "WOM": { flag: "🇦🇺", name: "Australia", nameJP: "豪州" },
  // Germany / Cold War era test sites
  "HVP": { flag: "🇩🇪", name: "Germany", nameJP: "ドイツ" },
  "WEHR": { flag: "🇩🇪", name: "Germany", nameJP: "ドイツ" },
};

function getSiteCountry(siteId: string, location: string) {
  return (
    SITE_COUNTRY[siteId] ??
    GCAT_COUNTRY[location] ??
    GCAT_COUNTRY[location.split("-")[0]] ??
    { flag: "🌍", name: "Unknown", nameJP: "不明" }
  );
}

// ─── Main Page ───────────────────────────────────────────────────────────────

export default function OrbitalDashboard() {
  const [lang, setLang] = useState<Lang>("en");
  const [activeTab, setActiveTab] = useState<"upcoming" | "past">("upcoming");
  const [visibleCount, setVisibleCount] = useState(50);
  const [dynamicSpX, setDynamicSpX] = useState<Mission[]>([]);

  // Filters
  const [filterYear, setFilterYear] = useState<string>("All");
  const [filterCountry, setFilterCountry] = useState<string>("All");
  const [filterStatus, setFilterStatus] = useState<string>("All");

  const t = translations[lang];

  useEffect(() => {
    fetch("https://api.spacexdata.com/v4/launches/upcoming")
      .then((res) => res.json())
      .then((data) => {
        const rockets: Record<string, string> = {
          "5e9d0d95eda69973a809d1ec": "Falcon 9",
          "5e9d0d95eda69974db09d1ed": "Falcon Heavy",
          "5e9d0d96eda699382d09d1ee": "Starship",
        };
        const pads: Record<string, { siteId: string; location: string }> = {
          "5e9e4501f509094ba4566f84": { siteId: "cape-canaveral", location: "Cape Canaveral" },
          "5e9e4502f509094188566f88": { siteId: "ksc", location: "Kennedy Space Center" },
          "5e9e4502f509092b78566f87": { siteId: "vandenberg", location: "Vandenberg SFB" },
          "5e9e4502f509099ba4566f89": { siteId: "boca-chica", location: "Starbase, Texas" },
        };

        const mapped: Mission[] = data.map((d: any) => ({
          id: `spx-up-${d.id}`,
          date: d.date_utc ? d.date_utc.split("T")[0] : "TBD",
          missionName: d.name,
          missionType: "Commercial" as MissionType,
          rocketName: rockets[d.rocket] || "SpaceX Rocket",
          provider: "SpaceX",
          location: pads[d.launchpad]?.location || "Unknown Pad",
          siteId: pads[d.launchpad]?.siteId || "usa",
          status: d.tbd ? "TBD" : "Scheduled",
        }));
        setDynamicSpX(mapped);
      })
      .catch((err) => console.error("SpaceX API fetch error:", err));
  }, []);

  const upcoming = useMemo(
    () => {
      // Create a set of IDs to prevent duplicates if missions.json also contains them
      const localUpcoming = allMissions.filter((m) => ["Scheduled", "TBD", "In Flight"].includes(m.status));
      const merged = [...localUpcoming, ...dynamicSpX];

      return merged.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    },
    [dynamicSpX]
  );

  const past = useMemo(
    () =>
      allMissions
        .filter((m) =>
          ["Success", "Failure", "Partial Failure"].includes(m.status),
        )
        .sort(
          (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
        ),
    [],
  );

  const activeMissions = activeTab === "upcoming" ? upcoming : past;

  const availableYears = useMemo(() => {
    const years = new Set<string>();
    activeMissions.forEach(m => {
      if (m.date && m.date !== "TBD") years.add(m.date.substring(0, 4));
    });
    return Array.from(years).sort((a, b) => b.localeCompare(a));
  }, [activeMissions]);

  const availableCountries = useMemo(() => {
    const countries = new Set<string>();
    activeMissions.forEach(m => {
      countries.add(getSiteCountry(m.siteId, m.location).name);
    });
    return Array.from(countries).sort();
  }, [activeMissions]);

  const availableStatuses = useMemo(() => {
    const statuses = new Set<string>();
    activeMissions.forEach(m => statuses.add(m.status));
    return Array.from(statuses).sort();
  }, [activeMissions]);

  const filteredMissions = useMemo(() => {
    return activeMissions.filter(m => {
      let match = true;
      if (filterYear !== "All") {
        if (!m.date.startsWith(filterYear)) match = false;
      }
      if (filterCountry !== "All") {
        const c = getSiteCountry(m.siteId, m.location);
        if (c.name !== filterCountry) match = false;
      }
      if (filterStatus !== "All") {
        if (m.status !== filterStatus) match = false;
      }
      return match;
    });
  }, [activeMissions, filterYear, filterCountry, filterStatus]);

  const paginatedMissions = useMemo(
    () => filteredMissions.slice(0, visibleCount),
    [filteredMissions, visibleCount],
  );

  // Reset pagination and filters when tab changes
  const handleTabChange = (tab: "upcoming" | "past") => {
    setActiveTab(tab);
    setVisibleCount(50);
    setFilterYear("All");
    setFilterCountry("All");
    setFilterStatus("All");
  };

  // Map data
  const mapMissions: MapMission[] = useMemo(
    () =>
      [...allMissions, ...dynamicSpX].map((m) => ({
        missionName: lang === "ja" && m.missionNameJP ? m.missionNameJP : m.missionName,
        rocketName: lang === "ja" && m.rocketNameJP ? m.rocketNameJP : m.rocketName,
        provider: m.provider,
        date: m.date,
        status: m.status,
        siteId: m.siteId,
      })),
    [lang, dynamicSpX],
  );

  // Chart data — past missions annotated with country name
  const chartMissions = useMemo(
    () =>
      filteredMissions.map((m) => ({
        date: m.date,
        siteId: m.siteId,
        location: m.location,
        country: getSiteCountry(m.siteId, m.location).name,
      })),
    [filteredMissions],
  );

  // Stats
  const totalLaunches = allMissions.length + dynamicSpX.length;
  const next30 = upcoming.length;
  const successCount = past.filter((m) => m.status === "Success").length;
  const successRate =
    past.length > 0 ? Math.round((successCount / past.length) * 100) : 0;

  const formatDate = (dateStr: string) => {
    const d = new Date(dateStr);
    if (lang === "ja") {
      return d.toLocaleDateString("ja-JP", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    }
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#0a0a0a]">
      {/* Background grid */}
      <div
        className="pointer-events-none fixed inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />

      {/* ── Navbar ─────────────────────────────────────────────────────── */}
      <header className="sticky top-0 z-50 border-b border-white/[0.06] bg-[#0a0a0a]/80 backdrop-blur-xl">
        <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/[0.06] border border-white/[0.08]">
              <Rocket className="h-4 w-4 text-sky-400" />
            </div>
            <span className="text-sm font-semibold tracking-[0.25em] text-neutral-100">
              ORBITAL
            </span>
          </div>

          {/* Right section */}
          <div className="flex items-center gap-4">
            {/* Status indicator */}
            <div className="hidden items-center gap-2 sm:flex">
              <div className="relative flex h-2 w-2">
                <span className="status-pulse absolute inline-flex h-full w-full rounded-full bg-emerald-400" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
              </div>
              <span className="text-[11px] font-medium tracking-wider text-neutral-500">
                {t.systemOnline.toUpperCase()}
              </span>
            </div>

            {/* Divider */}
            <div className="hidden h-4 w-px bg-white/[0.08] sm:block" />

            {/* Language toggle */}
            <button
              onClick={() => setLang(lang === "en" ? "ja" : "en")}
              className="flex items-center gap-1 rounded-md border border-white/[0.08] bg-white/[0.03] px-2.5 py-1 text-[11px] font-medium tracking-wider text-neutral-400 transition-colors hover:border-white/[0.15] hover:text-neutral-200"
            >
              <Globe className="mr-1 h-3 w-3" />
              {lang === "en" ? "JP" : "EN"}
            </button>
          </div>
        </div>
      </header>

      {/* ── Content ────────────────────────────────────────────────────── */}
      <main className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Summary Widgets */}
        <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
          {/* Total Launches */}
          <div className="group relative overflow-hidden rounded-xl border border-white/[0.06] bg-white/[0.02] p-5 transition-colors hover:border-white/[0.12] hover:bg-white/[0.04]">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-[11px] font-medium uppercase tracking-wider text-neutral-500">
                  {t.totalLaunches}
                </p>
                <p className="mt-2 text-3xl font-light tracking-tight text-neutral-100">
                  {totalLaunches}
                  <span className="ml-1.5 text-sm font-normal text-neutral-500">
                    {t.launches}
                  </span>
                </p>
              </div>
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-sky-400/10 text-sky-400">
                <Rocket className="h-4 w-4" />
              </div>
            </div>
            {/* Bottom accent */}
            <div className="absolute bottom-0 left-0 h-[2px] w-full bg-gradient-to-r from-sky-500/50 via-sky-400/20 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
          </div>

          {/* Next 30 Days */}
          <div className="group relative overflow-hidden rounded-xl border border-white/[0.06] bg-white/[0.02] p-5 transition-colors hover:border-white/[0.12] hover:bg-white/[0.04]">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-[11px] font-medium uppercase tracking-wider text-neutral-500">
                  {t.next30Days}
                </p>
                <p className="mt-2 text-3xl font-light tracking-tight text-neutral-100">
                  {next30}
                  <span className="ml-1.5 text-sm font-normal text-neutral-500">
                    {t.scheduled}
                  </span>
                </p>
              </div>
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-400/10 text-violet-400">
                <CalendarClock className="h-4 w-4" />
              </div>
            </div>
            <div className="absolute bottom-0 left-0 h-[2px] w-full bg-gradient-to-r from-violet-500/50 via-violet-400/20 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
          </div>

          {/* Success Rate */}
          <div className="group relative overflow-hidden rounded-xl border border-white/[0.06] bg-white/[0.02] p-5 transition-colors hover:border-white/[0.12] hover:bg-white/[0.04]">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-[11px] font-medium uppercase tracking-wider text-neutral-500">
                  {t.successRate}
                </p>
                <p className="mt-2 text-3xl font-light tracking-tight text-neutral-100">
                  {successRate}
                  <span className="ml-0.5 text-lg font-normal text-neutral-500">
                    %
                  </span>
                </p>
              </div>
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-400/10 text-emerald-400">
                <TrendingUp className="h-4 w-4" />
              </div>
            </div>
            {/* Mini bar chart */}
            <div className="mt-3 flex gap-0.5">
              {past.map((m) => (
                <div
                  key={m.id}
                  className={`h-1 flex-1 rounded-full ${m.status === "Success"
                    ? "bg-emerald-400/60"
                    : m.status === "Partial Failure"
                      ? "bg-amber-400/60"
                      : "bg-red-400/60"
                    }`}
                />
              ))}
            </div>
            <div className="absolute bottom-0 left-0 h-[2px] w-full bg-gradient-to-r from-emerald-500/50 via-emerald-400/20 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
          </div>
        </div>

        {/* ── Launch History Chart (Past only) ──────────────────────── */}
        {activeTab === "past" && (
          <div className="mb-6">
            <LaunchHistoryChart missions={chartMissions} lang={lang} />
          </div>
        )}

        {/* ── Mission Log ──────────────────────────────────────────────── */}
        <div className="overflow-hidden rounded-xl border border-white/[0.06] bg-white/[0.02]">
          {/* Tab header */}
          <div className="flex items-center justify-between border-b border-white/[0.06] px-5 pt-4 pb-0">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-neutral-500" />
              <span className="text-xs font-medium uppercase tracking-wider text-neutral-400">
                {t.missionLog}
              </span>
            </div>
            <div className="flex">
              {(["upcoming", "past"] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => handleTabChange(tab)}
                  className={`relative px-4 pb-3 text-xs font-medium tracking-wider transition-colors ${activeTab === tab
                    ? "text-neutral-100"
                    : "text-neutral-500 hover:text-neutral-300"
                    }`}
                >
                  {tab === "upcoming" ? t.upcoming : t.past}
                  {activeTab === tab && (
                    <span className="tab-active-indicator absolute bottom-0 left-0 right-0 h-[2px] rounded-full bg-sky-400" />
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* ── Filters ─────────────────────────────────────────────────── */}
          <div className="flex flex-wrap items-center gap-4 border-b border-white/[0.06] bg-white/[0.01] px-5 py-3">
            <div className="flex items-center gap-2">
              <Filter className="h-3 w-3 text-neutral-500" />
              <span className="text-[10px] font-medium uppercase tracking-widest text-neutral-500">Filter</span>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <select
                value={filterYear}
                onChange={(e) => { setFilterYear(e.target.value); setVisibleCount(50); }}
                className="appearance-none rounded-md border border-white/[0.08] bg-[#0a0a0a] px-3 py-1.5 text-xs text-neutral-300 outline-none transition-colors hover:border-white/[0.2] focus:border-sky-500/50"
              >
                <option value="All">{t.filterYear}: {t.all}</option>
                {availableYears.map(y => <option key={y} value={y}>{y}</option>)}
              </select>

              <select
                value={filterCountry}
                onChange={(e) => { setFilterCountry(e.target.value); setVisibleCount(50); }}
                className="appearance-none rounded-md border border-white/[0.08] bg-[#0a0a0a] px-3 py-1.5 text-xs text-neutral-300 outline-none transition-colors hover:border-white/[0.2] focus:border-sky-500/50"
              >
                <option value="All">{t.filterCountry}: {t.all}</option>
                {availableCountries.map(c => <option key={c} value={c}>{lang === "ja" ? (Object.values(SITE_COUNTRY).find(sc => sc.name === c)?.nameJP || GCAT_COUNTRY[Object.keys(GCAT_COUNTRY).find(k => GCAT_COUNTRY[k].name === c) || ""]?.nameJP || c) : c}</option>)}
              </select>

              <select
                value={filterStatus}
                onChange={(e) => { setFilterStatus(e.target.value); setVisibleCount(50); }}
                className="appearance-none rounded-md border border-white/[0.08] bg-[#0a0a0a] px-3 py-1.5 text-xs text-neutral-300 outline-none transition-colors hover:border-white/[0.2] focus:border-sky-500/50"
              >
                <option value="All">{t.filterStatus}: {t.all}</option>
                {availableStatuses.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
          </div>

          {/* ── Desktop Table ─────────────────────────────────────────── */}
          <div className="hidden md:block">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/[0.04]">
                  <th className="px-5 py-3 text-left text-[10px] font-medium uppercase tracking-widest text-neutral-600">
                    {t.date}
                  </th>
                  <th className="px-5 py-3 text-left text-[10px] font-medium uppercase tracking-widest text-neutral-600">
                    {t.mission}
                  </th>
                  <th className="px-5 py-3 text-left text-[10px] font-medium uppercase tracking-widest text-neutral-600">
                    {t.rocket}
                  </th>
                  <th className="px-5 py-3 text-left text-[10px] font-medium uppercase tracking-widest text-neutral-600">
                    {lang === "ja" ? "国・地域" : "Country"}
                  </th>
                  <th className="px-5 py-3 text-left text-[10px] font-medium uppercase tracking-widest text-neutral-600">
                    {t.location}
                  </th>
                  <th className="px-5 py-3 text-left text-[10px] font-medium uppercase tracking-widest text-neutral-600">
                    {t.status}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.04]">
                {paginatedMissions.map((m) => (
                  <tr
                    key={m.id}
                    className="group transition-colors hover:bg-white/[0.03]"
                  >
                    <td className="whitespace-nowrap px-5 py-3.5">
                      <span className="font-mono text-xs text-neutral-500">
                        {formatDate(m.date)}
                      </span>
                    </td>
                    <td className="px-5 py-3.5">
                      <div className="flex flex-col gap-1">
                        <span className="text-sm font-medium text-neutral-200 group-hover:text-neutral-50">
                          {lang === "ja" && m.missionNameJP
                            ? m.missionNameJP
                            : m.missionName}
                        </span>
                        <MissionTypeBadge type={m.missionType} />
                      </div>
                    </td>
                    <td className="px-5 py-3.5">
                      <div className="flex flex-col">
                        <span className="text-sm text-neutral-300">
                          {lang === "ja" && m.rocketNameJP
                            ? m.rocketNameJP
                            : m.rocketName}
                        </span>
                        <span className="text-xs text-neutral-500">
                          {m.provider}
                        </span>
                      </div>
                    </td>
                    <td className="whitespace-nowrap px-5 py-3.5">
                      {
                        (() => {
                          const c = getSiteCountry(m.siteId, m.location);
                          return (
                            <span className="flex items-center gap-1.5 text-xs text-neutral-300">
                              <span className="text-base leading-none">{c.flag}</span>
                              <span>{lang === "ja" ? c.nameJP : c.name}</span>
                            </span>
                          );
                        })()
                      }
                    </td>
                    <td className="px-5 py-3.5">
                      <div className="flex items-center gap-1.5">
                        <MapPin className="h-3 w-3 shrink-0 text-neutral-600" />
                        <span className="text-xs text-neutral-400">
                          {m.location}
                        </span>
                      </div>
                    </td>
                    <td className="px-5 py-3.5">
                      <StatusBadge status={m.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ── Mobile Card List ───────────────────────────────────────── */}
          <div className="divide-y divide-white/[0.04] md:hidden">
            {paginatedMissions.map((m) => (
              <div
                key={m.id}
                className="group flex items-start gap-4 px-4 py-4 transition-colors hover:bg-white/[0.03]"
              >
                {/* Date block */}
                <div className="flex w-12 shrink-0 flex-col items-center rounded-lg border border-white/[0.06] bg-white/[0.03] py-1.5">
                  <span className="text-[10px] font-medium uppercase text-neutral-500">
                    {new Date(m.date).toLocaleDateString("en-US", {
                      month: "short",
                    })}
                  </span>
                  <span className="text-lg font-light text-neutral-200">
                    {new Date(m.date).getDate()}
                  </span>
                </div>

                {/* Details */}
                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <h3 className="truncate text-sm font-medium text-neutral-200">
                        {m.missionName}
                      </h3>
                      <p className="mt-0.5 text-xs text-neutral-500">
                        {m.rocketName}{" "}
                        <span className="text-neutral-600">·</span>{" "}
                        {m.provider}
                      </p>
                    </div>
                    <ChevronRight className="mt-0.5 h-4 w-4 shrink-0 text-neutral-700 transition-colors group-hover:text-neutral-400" />
                  </div>
                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    <StatusBadge status={m.status} />
                    <MissionTypeBadge type={m.missionType} />
                  </div>
                  <div className="mt-1.5 flex items-center gap-2">
                    {
                      (() => {
                        const c = getSiteCountry(m.siteId, m.location);
                        return (
                          <span className="flex items-center gap-1 text-[11px] text-neutral-400">
                            <span className="text-sm leading-none">{c.flag}</span>
                            <span>{lang === "ja" ? c.nameJP : c.name}</span>
                          </span>
                        );
                      })()
                    }
                    <span className="text-neutral-700">·</span>
                    <MapPin className="h-3 w-3 text-neutral-600" />
                    <span className="text-[11px] text-neutral-500">
                      {m.location}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Load More Button */}
          {filteredMissions.length > visibleCount && (
            <div className="flex justify-center py-6">
              <button
                onClick={() => setVisibleCount((prev) => prev + 100)}
                className="group flex items-center gap-2 rounded-lg border border-white/[0.08] bg-white/[0.03] px-8 py-2.5 text-[11px] font-medium uppercase tracking-widest text-neutral-400 transition-all hover:border-white/[0.18] hover:bg-white/[0.06] hover:text-neutral-100 active:scale-95"
              >
                {lang === "ja" ? "さらに読み込む" : "Load More"}
                <span className="text-neutral-600 transition-colors group-hover:text-neutral-400">
                  ({filteredMissions.length - visibleCount} {lang === "ja" ? "件" : "remaining"})
                </span>
              </button>
            </div>
          )}

          {filteredMissions.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16 text-neutral-500">
              <Filter className="mb-3 h-8 w-8 opacity-20" />
              <p className="text-sm">{lang === "ja" ? "条件に一致するミッションがありません" : "No missions match your filters"}</p>
              <button
                onClick={() => {
                  setFilterYear("All");
                  setFilterCountry("All");
                  setFilterStatus("All");
                }}
                className="mt-4 text-xs font-medium text-sky-400 hover:text-sky-300"
              >
                {lang === "ja" ? "フィルターをリセット" : "Reset Filters"}
              </button>
            </div>
          )}
        </div>

        {/* ── Launch Sites Map ──────────────────────────────────────── */}
        <div className="mt-8 overflow-hidden rounded-xl border border-white/[0.06] bg-white/[0.02]">
          <div className="flex items-center gap-2 border-b border-white/[0.06] px-5 py-3">
            <Map className="h-4 w-4 text-neutral-500" />
            <span className="text-xs font-medium uppercase tracking-wider text-neutral-400">
              {t.launchSites}
            </span>
            <span className="text-[10px] text-neutral-600">
              — {t.launchSitesDesc}
            </span>
          </div>
          <div className="h-[400px] w-full">
            <LaunchMap
              sites={launchSites}
              missions={mapMissions}
              lang={lang}
            />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-8 flex items-center justify-center">
          <p className="text-[10px] uppercase tracking-widest text-neutral-700">
            Orbital Dashboard · {new Date().getFullYear()} · Mock Data
          </p>
        </footer>
      </main>
    </div>
  );
}
