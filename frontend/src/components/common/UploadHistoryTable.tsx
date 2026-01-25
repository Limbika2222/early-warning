import type { UploadHistoryItem } from "../../api/trends"

interface Props {
  uploads: UploadHistoryItem[]
}

export default function UploadHistoryTable({ uploads }: Props) {
  if (!uploads.length) {
    return (
      <p className="text-sm text-gray-500">
        No uploads yet.
      </p>
    )
  }

  return (
    <table className="w-full border">
      <thead className="bg-gray-100">
        <tr>
          <th className="p-2 border">Keyword</th>
          <th className="p-2 border">Country</th>
          <th className="p-2 border">Rows</th>
          <th className="p-2 border">Uploaded at</th>
        </tr>
      </thead>
      <tbody>
        {uploads.map(u => (
          <tr key={u.id}>
            <td className="p-2 border">{u.keyword}</td>
            <td className="p-2 border">{u.country}</td>
            <td className="p-2 border text-center">
              {u.rows_inserted}
            </td>
            <td className="p-2 border">
              {new Date(u.uploaded_at).toLocaleString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
