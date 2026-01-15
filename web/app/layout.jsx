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
          

        <main >
          {children}
        </main>

      </body>
    </html>
  );
}
