const API_BASE =
  import.meta.env.VITE_API_BASE;

export interface Report {

  id: number;

  filename: string;

  report_type: string;

  generated_at: string;

  generated_by: string;

  file_path: string;
}

// =====================================================
// GET REPORT HISTORY
// =====================================================

export async function getReports() {

  const response = await fetch(

    `${API_BASE}/api/reports/history`
  );

  if (!response.ok) {

    throw new Error(
      "Failed to fetch reports"
    );
  }

  return response.json();
}

// =====================================================
// GENERATE WEEKLY REPORT
// =====================================================

export async function generateReport() {

  window.open(

    `${API_BASE}/api/reports/weekly`,

    "_blank"
  );
}

// =====================================================
// DOWNLOAD REPORT
// =====================================================

export function downloadReport(
  reportId: number
) {

  window.open(

    `${API_BASE}/api/reports/download/${reportId}`,

    "_blank"
  );
}

// =====================================================
// PREVIEW REPORT
// =====================================================

export function previewReport(
  reportId: number
) {

  return (

    `${API_BASE}/api/reports/preview/${reportId}`
  );
}