import Link from 'next/link'

type pageLink = {
  name: string,
  url: string
}

export type FooterLink = {
  title: string
  urls: pageLink[]
}
export default function Footer() {

  const footerLinks: FooterLink[] = [
    {
      title: "チケットヴィレッジについて",
      urls: [{name: "運営会社", url: "https://www.leadi.co.jp"}]
    },
    {
      title: "ヘルプとガイド",
      urls: [{name: "お問い合わせ", url: "/contact"}, {name: "ご利用ガイド", url: "/guide"}]
    },
    {
      title: "プライバシーと利用規約",
      urls: [{name: "プライバシーポリシー", url: "/privacypolicy"}, {name: "利用規約", url: "/terms"}, {name: "特別商取引法に基づく表示", url: "/tokutei"}]
    },
  ];

  return (
    <footer className={"w-full h-[367px]"}>
      <ul className="h-[253px] flex items-start justify-center w-11/12 mx-auto py-[60px] space-x-[60px]">
        {footerLinks.map((footerLink, index) => (
          <li className={"space-y-[15px]"} key={index}>
            <div className="font-[900]">{footerLink.title}</div>
            <ul className="space-y-3">
              {footerLink.urls.map((url, index) => (
                  <li key={index} className={"text-[12px] font-[200] text-[#234]"}><Link href={url.url} target="_blank">{url.name}</Link></li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      <div className="copy-right">
        © Ticket Village 2019
      </div>
    </footer>
  )
}
