import './globals.css'
import 'zenn-content-css';
import type { Metadata } from 'next'
import {Header} from "@/app/article/[slug]/components/SidBar/Header";

export const metadata: Metadata = {
  title: 'Create Next App',
  description: 'Generated by create next app',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className={"w-full bg-[#EDF2F7]"}>
        <div className={"w-11/12 md:w-2/3 mx-auto"}>
          <Header />
          {children}
        </div>
      </body>
    </html>
  )
}
