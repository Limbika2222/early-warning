export default function ChartCard({
  title,
  children,
}: {
  title: string
  children: React.ReactNode
}) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">
        {title}
      </h3>
      {children}
    </div>
  )
}
