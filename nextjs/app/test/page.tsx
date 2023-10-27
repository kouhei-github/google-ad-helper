'use client'
import markdownHtml from 'zenn-markdown-html';
import Script from "next/script";
import {useEffect} from "react";
import 'zenn-content-css';


export default function Home() {

  const markdownText = ``
  const html = markdownHtml(markdownText);
  useEffect(() => {
    import('zenn-embed-elements');
  }, []);
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
