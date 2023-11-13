'use client'
import markdownHtml from 'zenn-markdown-html';
import Script from "next/script";
import {useEffect} from "react";
import 'zenn-content-css';
import {useGetArticle} from "@/utils/api/article_fetch";
import Link from "next/link";
import {useSearchParams} from "next/navigation";


export default function Home() {
  const searchParams = useSearchParams()

  const {article, isError, isLoading} = useGetArticle(searchParams.get("page") === null ? 1 : Number(searchParams.get("page")) )
  useEffect(() => {
    import('zenn-embed-elements');
  }, []);
  if (isError) return <div>load is Failed</div>
  if (isLoading) return <div>Loadin ...</div>
  if (typeof article === "undefined") return <div>load is Failed</div>
  const html = markdownHtml(article.description);
  return (
    <div className={"w-11/12 md:w-[85%] mx-auto my-12 flex space-x-8 "}>
      <Script src={"https://embed.zenn.studio/js/listen-embed-event.js"} />
      <div
        // "znc"というクラス名を指定する
        className="znc md:w-[75%] w-[100%] bg-[#FFFFFF] p-8 rounded-xl"
        // htmlを渡す
        dangerouslySetInnerHTML={{
          __html: html,
        }}
      />
      <div className={"w-[25%] md:block hidden min-h-screen space-y-4"}>
        <div className={"w-[300px] h-[275px] bg-white rounded-xl overflow-y-scroll px-4 pb-5"}>
          <h3 className={"font-bold text-xl text-center my-6 border-b-2 border-gray-200"}>おすすめの記事</h3>
          <div className={"space-y-3"}>
            {[{title: "ruby on rails", link: "#"}, {title: "about Python", link: "#"}].map((url, index) => (
              <div key={index} className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>
                <Link href={url.link}>{url.title}</Link>
              </div>
            ))}
          </div>
        </div>

        <div className={"w-[300px] h-[605px] bg-white rounded-xl overflow-y-scroll px-4 pb-5 sticky top-10"}>
          <h3 className={"font-bold text-xl text-center my-6 border-b-2 border-gray-200"}>新着の記事</h3>
          <div className={"space-y-3"}>
            {[{title: "ruby on rails", link: "#"}, {title: "about Python", link: "#"}].map((url, index) => (
              <div key={index} className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>
                <Link href={url.link}>{url.title}</Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
