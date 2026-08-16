import type { Metadata } from "next";
import "./globals.css";
import "./advanced.css";
import "./deep-analysis.css";

export const metadata: Metadata = { title: "ResumeAI | Resume Analyzer", description: "Get clear, practical feedback on your resume." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
