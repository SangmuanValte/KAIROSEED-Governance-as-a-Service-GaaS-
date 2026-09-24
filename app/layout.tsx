import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata={title:"ASTRA Drone Simulator",description:"SCIИENTIA + ASTRA governed drone simulation dashboard"};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}