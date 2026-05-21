import {
    ComposableMap,
    Geographies,
    Geography,
  } from "react-simple-maps"
  
  import type {
    CountrySummary,
  } from "../../api/who"
  
  interface Props {
    countries: CountrySummary[],
    diseaseMap: Record<string, string[]>
  }
  
  // =====================================================
  // TEMP TYPES
  // =====================================================
  
  interface GeoFeature {
    rsmKey: string
    id: string
    properties?: {
      name?: string
      NAME?: string
      iso_a2?: string
      ISO_A2?: string
    }
  }
  
  // =====================================================
  // LOCAL GEO JSON
  // =====================================================
  
  const GEO_URL = "/maps/countries.json"
  
  // =====================================================
  // COLOR SCALE
  // =====================================================
  
  function getCountryColor(
    count: number
  ) {
  
    if (count >= 10) {
      return "#b91c1c"
    }
  
    if (count >= 5) {
      return "#ea580c"
    }
  
    if (count >= 2) {
      return "#facc15"
    }
  
    if (count >= 1) {
      return "#4ade80"
    }
  
    return "#e5e7eb"
  }
  
  // =====================================================
  // COMPONENT
  // =====================================================

  const COUNTRY_NAME_TO_ISO2: Record<
    string,
    string
  > = {
    "United Kingdom": "GB",
    Russia: "RU",
    "United States of America": "US",
  }
  
  export default function OutbreakMap({
    countries,
    diseaseMap
  }: Props) {
  
    // -------------------------------------------------
    // COUNTRY LOOKUP
    // -------------------------------------------------
  
    const lookup: Record<
      string,
      number
    > = {}
  
    countries.forEach((country) => {
  
      const iso2 =
        country.country_iso2?.toUpperCase()
  
      if (!iso2) return
  
      lookup[iso2] =
        country.outbreak_count
    })
  
    // =====================================================
    // UI
    // =====================================================
  
    return (
  
      <div
        className="
          bg-white rounded-2xl
          shadow-sm border p-5
        "
      >
  
        {/* HEADER */}
  
        <div className="mb-4">
  
          <h2 className="text-xl font-semibold text-[#1e3f42]">
            Global Outbreak Map
          </h2>
  
          <p className="text-sm text-gray-500 mt-1">
            Geo-aware outbreak intelligence
          </p>
  
        </div>
  
        {/* MAP */}
  
        <div className="w-full h-[500px]">
  
          <ComposableMap
            projectionConfig={{
              scale: 140,
            }}
          >
  
            <Geographies geography={GEO_URL}>
  
              {({
                geographies,
              }: {
                geographies: GeoFeature[]
              }) =>
  
                geographies.map(
                  (geo) => {
  
                    // -----------------------------------
                    // ISO2 FROM GEOJSON
                    // -----------------------------------
  
                    const countryName =
                      geo.properties?.NAME ||
                      geo.properties?.name ||
                      "Unknown"

                    const iso2 =
                      COUNTRY_NAME_TO_ISO2[
                        countryName
                      ] || ""
  
                    const count =
                      lookup[iso2] || 0
  
                    return (
  
                      <Geography
                        key={geo.rsmKey}
                        geography={geo}
  
                        fill={getCountryColor(
                          count
                        )}
  
                        stroke="#ffffff"
                        strokeWidth={0.5}
  
                        style={{
  
                          default: {
                            outline:
                              "none",
                          },
  
                          hover: {
                            fill:
                              "#1f9c94",
                            outline:
                              "none",
                            cursor:
                              "pointer",
                          },
  
                          pressed: {
                            outline:
                              "none",
                          },
                        }}
                      >
  
                        <title>
                          {countryName}
                          {"\n"}
                          Outbreaks: {count}
                          {"\n"}
                          {(diseaseMap[iso2] || []).join(", ")}
                        </title>
  
                      </Geography>
                    )
                  }
                )
              }
  
            </Geographies>
  
          </ComposableMap>
  
        </div>
  
        {/* LEGEND */}
  
        <div className="flex gap-4 flex-wrap mt-5 text-xs">
  
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-[#b91c1c] rounded" />
            <span>10+ outbreaks</span>
          </div>
  
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-[#ea580c] rounded" />
            <span>5+ outbreaks</span>
          </div>
  
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-[#facc15] rounded" />
            <span>2+ outbreaks</span>
          </div>
  
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-[#4ade80] rounded" />
            <span>1+ outbreak</span>
          </div>
  
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-[#e5e7eb] rounded border" />
            <span>No data</span>
          </div>
  
        </div>
  
      </div>
    )
  }