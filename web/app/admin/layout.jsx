"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function AdminLayout({ children }) {
  const pathname = usePathname();

  // hide button only on gateway page
  const showGatewayButton = pathname !== "/admin/gateway";

  return (
    <div className="min-h-screen bg-[#0f172a] text-white">
      <header className="px-6 py-4 border-b border-slate-700 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold">
            Landslide Monitoring – Admin Console
          </h1>
          <p className="text-sm text-slate-400">
            Disaster Management Authority
          </p>
        </div>

        {showGatewayButton && (
          <Link
            href="/admin/gateway"
            className="text-white px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-sm font-semibold"
          >
            Grid Gateway
          </Link>
        )}
      </header>

      <main className="p-6">{children}</main>
    </div>
  );
}
