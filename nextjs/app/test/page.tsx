'use client'
import markdownHtml from 'zenn-markdown-html';
import Script from "next/script";
import {useEffect} from "react";
import 'zenn-content-css';
import {useGetArticle} from "@/utils/api/article_fetch";


export default function Home() {

  const {article, isError, isLoading} = useGetArticle(2)
  useEffect(() => {
    import('zenn-embed-elements');
  }, []);
  if (isError) return <div>load is Failed</div>
  if (isLoading) return <div>Loadin ...</div>
  if (typeof article === "undefined") return <div>load is Failed</div>
  const html = markdownHtml(article.description);
  return (
    <>
      <Script src={"https://embed.zenn.studio/js/listen-embed-event.js"}/>
      <div
        // "znc"というクラス名を指定する
        className="znc"
        // htmlを渡す
        dangerouslySetInnerHTML={{
          __html: html,
        }}
      />
    </>
  )
}
