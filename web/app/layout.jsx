import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "Landslide Early Warning System",
  description: "Hackathon Prototype",
};

import { Inter, Space_Grotesk } from "next/font/google";
import Image from "next/image";

const inter = Inter({
  subsets: ["latin"],
  weight: "400",        // Bungee only has 400
});



export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-black">
          <header className="shadow bg-[#F2EFEA]  px-8 py-4 flex gap-6">
            <div className="navbar shadow-sm rounded-xl  bg-[#163832] ">
              <div className="flex-1">
                <a className="btn btn-ghost text-xl text-white">M.I.M</a>
              </div>
              <div className="flex gap-12 items-center justify-center">
                <Link href="/" className=" text-white hover:text-blue-600">Home</Link>
                <Link href="/components/map" className="text-white hover:text-black">Map</Link>
                <Link href="/admin" className="text-white hover:text-black">Admin</Link>
                <div className="dropdown dropdown-end">
                  <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
                    
                    <div className="w-10 rounded-full">
                      <Image
                        width={10}
                        height={10}
                        alt="Tailwind CSS Navbar component"
                        src="/land1.jpeg" />
                    </div>
                  </div>
                  <ul
                    tabIndex="-1"
                    className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
                    <li>
                      <a className="justify-between">
                        Profile
                        <span className="badge">New</span>
                      </a>
                    </li>
                    <li><a>Settings</a></li>
                    <li><a>Logout</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </header>

        <main >
          {children}
        </main>

      </body>
    </html>
  );
}
