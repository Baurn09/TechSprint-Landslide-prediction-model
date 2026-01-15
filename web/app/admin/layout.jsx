export default function AdminLayout({ children }) {
  return (
    <div className="min-h-screen bg-[#0f172a] text-white">
      <header className="px-6 py-4 border-b border-slate-700">
        <h1 className="text-xl font-bold">
          Landslide Monitoring – Admin Console
        </h1>
        <p className="text-sm text-slate-400">
          Disaster Management Authority
        </p>
      </header>

      <main className="p-6">{children}</main>
    </div>
  );
}
