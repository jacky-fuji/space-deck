"use client";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Cell,
} from "recharts";

// Country color palette — dark-theme friendly, matched with LaunchHistoryChart
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

export interface ChartMission {
    country: string; // pre-resolved country name
}

interface Props {
    missions: ChartMission[];
    lang: "en" | "ja";
}

// Custom tooltip for horizontal bar
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomTooltip({ active, payload, lang }: any) {
    if (!active || !payload?.length) return null;
    const data = payload[0].payload;
    const name = lang === "ja" ? COUNTRY_JP[data.country] ?? data.country : data.country;

    return (
        <div className="rounded-lg border border-white/[0.10] bg-[#0f0f0f]/95 px-4 py-3 shadow-xl backdrop-blur flex items-center gap-3">
            <span
                className="h-3 w-3 rounded-full flex-shrink-0"
                style={{ background: payload[0].fill }}
            />
            <span className="text-sm font-medium text-neutral-300">
                {name}
            </span>
            <span className="ml-auto pl-4 font-mono text-neutral-200">
                {data.count.toLocaleString()} {lang === "ja" ? "回" : "launches"}
            </span>
        </div>
    );
}

export default function TotalLaunchesChart({ missions, lang }: Props) {
    // ── Compute country totals ──────────────────────────────────────────────────
    const countryTotals: Record<string, number> = {};
    for (const m of missions) {
        const c = m.country;
        countryTotals[c] = (countryTotals[c] ?? 0) + 1;
    }

    // Sort descending by count
    const data = Object.entries(countryTotals)
        .map(([country, count]) => ({ country, count }))
        .sort((a, b) => b.count - a.count);

    if (data.length === 0) {
        return null;
    }

    return (
        <div className="overflow-hidden rounded-xl border border-white/[0.06] bg-white/[0.02] h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/[0.06] px-5 py-3 flex-shrink-0">
                <div className="flex items-center gap-2">
                    <div className="h-1.5 w-1.5 rounded-full bg-violet-400" />
                    <span className="text-xs font-medium uppercase tracking-wider text-neutral-400">
                        {lang === "ja" ? "国別累計打ち上げ回数" : "Total Launches by Country"}
                    </span>
                </div>
            </div>

            {/* Chart */}
            <div className="px-5 pb-4 pt-6 flex-grow">
                <ResponsiveContainer width="100%" height={Math.max(300, data.length * 30)}>
                    <BarChart
                        data={data}
                        layout="vertical"
                        margin={{ top: 0, right: 30, left: lang === "ja" ? 20 : 30, bottom: 0 }}
                        barCategoryGap="20%"
                    >
                        <CartesianGrid
                            horizontal={false}
                            stroke="rgba(255,255,255,0.04)"
                        />
                        <XAxis
                            type="number"
                            tick={{ fill: "#6b7280", fontSize: 10 }}
                            tickLine={false}
                            axisLine={false}
                            domain={[0, 'dataMax']}
                        />
                        <YAxis
                            dataKey="country"
                            type="category"
                            tickFormatter={(val) => lang === "ja" ? COUNTRY_JP[val] ?? val : val}
                            tick={{ fill: "#9ca3af", fontSize: 11 }}
                            tickLine={false}
                            axisLine={false}
                            width={80}
                            interval={0} // Force show all country labels
                        />
                        <Tooltip
                            cursor={{ fill: "rgba(255,255,255,0.03)" }}
                            content={<CustomTooltip lang={lang} />}
                        />
                        <Bar
                            dataKey="count"
                            radius={[0, 4, 4, 0]}
                            maxBarSize={20}
                            label={{ position: 'right', fill: '#9ca3af', fontSize: 11, formatter: (val: any) => typeof val === 'number' ? val.toLocaleString() : val }}
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COUNTRY_COLORS[entry.country] || "#475569"} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
