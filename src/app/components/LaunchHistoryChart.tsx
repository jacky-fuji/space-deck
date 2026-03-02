"use client";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";

// Country color palette — dark-theme friendly
const COUNTRY_COLORS: Record<string, string> = {
    USA: "#38bdf8", // sky
    Russia: "#f87171", // red
    China: "#fb923c", // orange
    France: "#a78bfa", // violet
    Japan: "#f472b6", // pink
    India: "#fbbf24", // amber
    Kazakhstan: "#34d399", // emerald
    "New Zealand": "#6ee7b7", // teal-light
    "Marshall Is.": "#94a3b8", // slate
    "N. Korea": "#ef4444", // red-bright
    "S. Korea": "#3b82f6", // blue-bright
    Israel: "#60a5fa", // blue-light
    Iran: "#c084fc", // purple
    Brazil: "#86efac", // green-light
    Australia: "#fdba74", // orange-light
    Germany: "#d1d5db", // gray
    Norway: "#93c5fd", // blue-200
    Sweden: "#fde047", // yellow-300
    Others: "#475569", // slate-muted
};

const TOP_N = 9; // show top N countries + Others

export interface ChartMission {
    date: string;
    siteId: string;
    location: string;
    country: string; // pre-resolved country name
}

interface Props {
    missions: ChartMission[];
    lang: "en" | "ja";
}

const COUNTRY_JP: Record<string, string> = {
    USA: "米国",
    Russia: "ロシア",
    China: "中国",
    France: "フランス",
    Japan: "日本",
    India: "インド",
    Kazakhstan: "カザフスタン",
    "New Zealand": "NZ",
    "Marshall Is.": "マーシャル諸島",
    "N. Korea": "北朝鮮",
    "S. Korea": "韓国",
    Israel: "イスラエル",
    Iran: "イラン",
    Brazil: "ブラジル",
    Australia: "豪州",
    Germany: "ドイツ",
    Norway: "ノルウェー",
    Sweden: "スウェーデン",
    Others: "その他",
    Unknown: "不明",
};

// Custom tooltip
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomTooltip({ active, payload, label, lang }: any) {
    if (!active || !payload?.length) return null;
    const total = payload.reduce(
        (s: number, p: { value: number }) => s + (p.value ?? 0),
        0
    );
    return (
        <div className="rounded-lg border border-white/[0.10] bg-[#0f0f0f]/95 px-4 py-3 shadow-xl backdrop-blur">
            <p className="mb-2 text-xs font-semibold tracking-widest text-neutral-300">
                {label} — {total} {lang === "ja" ? "回" : "launches"}
            </p>
            <div className="flex flex-col gap-1">
                {[...payload].reverse().map(
                    (p: { name: string; value: number; fill: string }) =>
                        p.value > 0 && (
                            <div key={p.name} className="flex items-center gap-2 text-[11px]">
                                <span
                                    className="h-2 w-2 rounded-full flex-shrink-0"
                                    style={{ background: p.fill }}
                                />
                                <span className="text-neutral-400">
                                    {lang === "ja" ? COUNTRY_JP[p.name] ?? p.name : p.name}
                                </span>
                                <span className="ml-auto pl-4 font-mono text-neutral-200">
                                    {p.value}
                                </span>
                            </div>
                        )
                )}
            </div>
        </div>
    );
}

export default function LaunchHistoryChart({ missions, lang }: Props) {
    // ── Compute top countries ──────────────────────────────────────────────────
    const countryTotals: Record<string, number> = {};
    for (const m of missions) {
        const c = m.country;
        countryTotals[c] = (countryTotals[c] ?? 0) + 1;
    }
    const ranked = Object.entries(countryTotals)
        .sort((a, b) => b[1] - a[1])
        .map(([c]) => c);
    const topCountries = ranked.slice(0, TOP_N);
    const hasOthers = ranked.length > TOP_N;

    // ── Build year → country counts ────────────────────────────────────────────
    const byYear: Record<string, Record<string, number>> = {};
    for (const m of missions) {
        const year = m.date.slice(0, 4);
        if (!byYear[year]) byYear[year] = {};
        const country = topCountries.includes(m.country) ? m.country : "Others";
        byYear[year][country] = (byYear[year][country] ?? 0) + 1;
    }

    const years = Object.keys(byYear).sort();
    const data = years.map((year) => ({
        year,
        ...byYear[year],
    }));

    const keys = hasOthers ? [...topCountries, "Others"] : topCountries;

    return (
        <div className="overflow-hidden rounded-xl border border-white/[0.06] bg-white/[0.02]">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/[0.06] px-5 py-3">
                <div className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-sky-400" />
                    <span className="text-xs font-medium uppercase tracking-wider text-neutral-400">
                        {lang === "ja" ? "年別打ち上げ回数（国別積み上げ）" : "Launches per Year by Country"}
                    </span>
                </div>
                <span className="text-[11px] text-neutral-600">
                    {missions.length.toLocaleString()}{" "}
                    {lang === "ja" ? "件 / " : "missions · "}
                    {years.length} {lang === "ja" ? "年分" : "years"}
                </span>
            </div>

            {/* Chart */}
            <div className="px-2 pb-4 pt-4">
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart
                        data={data}
                        margin={{ top: 0, right: 16, left: -8, bottom: 0 }}
                        barCategoryGap="15%"
                    >
                        <CartesianGrid
                            vertical={false}
                            stroke="rgba(255,255,255,0.04)"
                        />
                        <XAxis
                            dataKey="year"
                            tick={{ fill: "#6b7280", fontSize: 10 }}
                            tickLine={false}
                            axisLine={false}
                            interval={9}
                        />
                        <YAxis
                            tick={{ fill: "#6b7280", fontSize: 10 }}
                            tickLine={false}
                            axisLine={false}
                            width={32}
                        />
                        <Tooltip
                            content={(props) => (
                                <CustomTooltip {...props} lang={lang} />
                            )}
                            cursor={{ fill: "rgba(255,255,255,0.03)" }}
                        />
                        <Legend
                            wrapperStyle={{ paddingTop: 16 }}
                            formatter={(value: string) =>
                                <span style={{ color: "#9ca3af", fontSize: 11 }}>
                                    {lang === "ja" ? COUNTRY_JP[value] ?? value : value}
                                </span>
                            }
                        />
                        {keys.map((country) => (
                            <Bar
                                key={country}
                                dataKey={country}
                                stackId="a"
                                fill={COUNTRY_COLORS[country] ?? "#475569"}
                                radius={country === keys[keys.length - 1] ? [2, 2, 0, 0] : [0, 0, 0, 0]}
                                maxBarSize={24}
                            />
                        ))}
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
