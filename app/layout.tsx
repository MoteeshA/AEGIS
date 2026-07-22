import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Aegis — Energy Supply Chain Resilience",
  description: "AI-assisted geopolitical risk, disruption simulation, adaptive procurement, and strategic reserve decisions.",
  icons: { icon: "/favicon.svg" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
