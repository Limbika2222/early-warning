import React from "react"

interface Props {
  startDate: string | null
  endDate: string | null
  onChange: (range: {
    startDate: string | null
    endDate: string | null
  }) => void
}

export default function DateRangeSelector({
  startDate,
  endDate,
  onChange,
}: Props) {
  return (
    <div className="flex flex-wrap items-end gap-4 mb-6">
      {/* Start Date */}
      <div className="flex flex-col">
        <label className="text-sm text-slate-600 mb-1">
          Start date
        </label>
        <input
          type="date"
          value={startDate ?? ""}
          onChange={e =>
            onChange({
              startDate: e.target.value || null,
              endDate,
            })
          }
          className="border rounded px-3 py-2 text-sm"
        />
      </div>

      {/* End Date */}
      <div className="flex flex-col">
        <label className="text-sm text-slate-600 mb-1">
          End date
        </label>
        <input
          type="date"
          value={endDate ?? ""}
          onChange={e =>
            onChange({
              startDate,
              endDate: e.target.value || null,
            })
          }
          className="border rounded px-3 py-2 text-sm"
        />
      </div>

      {/* Clear button */}
      {(startDate || endDate) && (
        <button
          onClick={() =>
            onChange({
              startDate: null,
              endDate: null,
            })
          }
          className="text-sm text-blue-600 hover:underline mb-1"
        >
          Clear range
        </button>
      )}
    </div>
  )
}
