"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export interface LaunchSite {
    id: string;
    name: string;
    country: string;
    lat: number;
    lng: number;
}

export interface MapMission {
    missionName: string;
    rocketName: string;
    provider: string;
    date: string;
    status: string;
    siteId: string;
}

interface LaunchMapProps {
    sites: LaunchSite[];
    missions: MapMission[];
    lang: "en" | "ja";
}

// Group missions by site
function groupBySite(missions: MapMission[]) {
    const map = new Map<string, MapMission[]>();
    for (const m of missions) {
        const arr = map.get(m.siteId) || [];
        arr.push(m);
        map.set(m.siteId, arr);
    }
    return map;
}

function statusColor(status: string): string {
    switch (status) {
        case "Success":
            return "#34d399";
        case "Scheduled":
            return "#38bdf8";
        case "TBD":
            return "#fbbf24";
        case "In Flight":
            return "#a78bfa";
        case "Partial Failure":
            return "#f59e0b";
        case "Failure":
            return "#f87171";
        default:
            return "#a3a3a3";
    }
}

export default function LaunchMap({ sites, missions, lang }: LaunchMapProps) {
    const grouped = groupBySite(missions);

    // Fix Leaflet default icon issue in Next.js
    useEffect(() => {
        // eslint-disable-next-line @typescript-eslint/no-require-imports
        const L = require("leaflet");
        delete L.Icon.Default.prototype._getIconUrl;
        L.Icon.Default.mergeOptions({
            iconRetinaUrl: "",
            iconUrl: "",
            shadowUrl: "",
        });
    }, []);

    return (
        <div className="relative h-full w-full overflow-hidden rounded-xl">
            <MapContainer
                center={[20, 0]}
                zoom={2}
                minZoom={2}
                maxZoom={10}
                scrollWheelZoom={true}
                className="h-full w-full"
                style={{ background: "#0d0d0d" }}
                attributionControl={false}
            >
                {/* Dark tile layer — CartoDB Dark Matter (free, no API key) */}
                <TileLayer
                    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>'
                />

                {sites.map((site) => {
                    const siteMissions = grouped.get(site.id) || [];
                    const hasUpcoming = siteMissions.some(
                        (m) =>
                            m.status === "Scheduled" ||
                            m.status === "TBD" ||
                            m.status === "In Flight",
                    );
                    const baseColor = hasUpcoming ? "#38bdf8" : "#34d399";
                    const count = siteMissions.length;

                    return (
                        <CircleMarker
                            key={site.id}
                            center={[site.lat, site.lng]}
                            radius={Math.max(6, Math.min(14, 6 + count * 2))}
                            pathOptions={{
                                color: baseColor,
                                fillColor: baseColor,
                                fillOpacity: 0.25,
                                weight: 1.5,
                                opacity: 0.8,
                            }}
                        >
                            <Tooltip
                                direction="top"
                                offset={[0, -8]}
                                className="orbital-tooltip"
                            >
                                <div
                                    style={{
                                        background: "#1a1a1a",
                                        border: "1px solid rgba(255,255,255,0.1)",
                                        borderRadius: "8px",
                                        padding: "10px 14px",
                                        color: "#ededed",
                                        minWidth: "180px",
                                        fontFamily: "var(--font-geist-sans), sans-serif",
                                    }}
                                >
                                    <div
                                        style={{
                                            fontSize: "11px",
                                            fontWeight: 600,
                                            color: "#ededed",
                                            marginBottom: "2px",
                                        }}
                                    >
                                        {site.name}
                                    </div>
                                    <div
                                        style={{
                                            fontSize: "10px",
                                            color: "#737373",
                                            marginBottom: "8px",
                                        }}
                                    >
                                        {site.country} · {site.lat.toFixed(2)}°,{" "}
                                        {site.lng.toFixed(2)}°
                                    </div>
                                    {siteMissions.length > 0 && (
                                        <div
                                            style={{
                                                borderTop: "1px solid rgba(255,255,255,0.06)",
                                                paddingTop: "6px",
                                            }}
                                        >
                                            {siteMissions.map((m, i) => (
                                                <div
                                                    key={i}
                                                    style={{
                                                        display: "flex",
                                                        alignItems: "center",
                                                        gap: "6px",
                                                        marginBottom: i < siteMissions.length - 1 ? "4px" : 0,
                                                    }}
                                                >
                                                    <span
                                                        style={{
                                                            width: "6px",
                                                            height: "6px",
                                                            borderRadius: "50%",
                                                            background: statusColor(m.status),
                                                            flexShrink: 0,
                                                        }}
                                                    />
                                                    <span style={{ fontSize: "10px", color: "#d4d4d4" }}>
                                                        {m.missionName}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </Tooltip>
                        </CircleMarker>
                    );
                })}
            </MapContainer>

            {/* Legend overlay */}
            <div className="absolute bottom-3 left-3 z-[1000] flex items-center gap-3 rounded-lg border border-white/[0.08] bg-[#0a0a0a]/90 px-3 py-2 backdrop-blur-sm">
                <div className="flex items-center gap-1.5">
                    <span className="inline-block h-2 w-2 rounded-full bg-sky-400" />
                    <span className="text-[10px] text-neutral-500">
                        {lang === "ja" ? "予定あり" : "Upcoming"}
                    </span>
                </div>
                <div className="flex items-center gap-1.5">
                    <span className="inline-block h-2 w-2 rounded-full bg-emerald-400" />
                    <span className="text-[10px] text-neutral-500">
                        {lang === "ja" ? "完了のみ" : "Past Only"}
                    </span>
                </div>
            </div>
        </div>
    );
}
