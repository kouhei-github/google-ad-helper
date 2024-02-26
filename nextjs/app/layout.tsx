import './globals.css'
import 'zenn-content-css';
import type { Metadata } from 'next'
import {Header} from "@/app/article/[slug]/components/SidBar/Header";
import GoogleAdsense from '@/components/Dashboard/GoogleAdsense'

export const metadata: Metadata = {
  title: '最新のWeb技術記事ならGeekSnipe',
  description: '海外で人気のWeb技術記事を日本語に翻訳して公開！',
  other: {
    "google-adsense-account": "ca-pub-3519272467638604"
  }
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className={"w-full bg-[#EDF2F7]"}>
        <GoogleAdsense pId="3519272467638604" />
        <div className={"w-11/12 md:w-2/3 mx-auto"}>
          <Header />
          {children}
        </div>
      </body>
    </html>
  )
}
