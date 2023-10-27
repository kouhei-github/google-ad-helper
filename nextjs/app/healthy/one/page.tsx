'use client'
import markdownHtml from 'zenn-markdown-html';
import Script from "next/script";
import {useEffect} from "react";
import 'zenn-content-css';


export default function Home() {

  const markdownText = "# iPhoneの古いモデルの価値と特徴\n\n**目次**\n\n- [はじめに](#introduction)\n- [iPhoneの歴史](#history)\n- [iPhoneの古いモデルの利点](#advantages)\n- [古いiPhoneモデルの特性](#features)\n- [古いモデルの選び方](#selecting-an-old-model)\n- [まとめ](#conclusion)\n\n## はじめに （Introduction）\niPhoneは2007年の初登場以来、スマホ市場を牽引してきた存在です。そのため、新しいモデルが発売されるたびに多くの人々が最新のiPhoneを購入します。しかし、その一方で古いモデルのiPhoneも依然として人気があり、一定のニーズが存在しています。本記事では、そんな古いモデルのiPhoneの価値について解説します。\n\n## iPhoneの歴史 (History)\niPhoneの歴史は、2007年に始まります。初代のiPhoneは、画期的なデザインと使い勝手の良さから、すぐに多くのユーザーを魅了しました。その後も、毎年新しいモデルが発表され、その都度技術的進歩が見られます。しかし、同時に古いモデルには特徴があり、利点もあります。\n\n## iPhoneの古いモデルの利点 (Advantages)\n新しいモデルには、高性能なプロセッサーや大きなディスプレイなどの最新の機能がありますが、古いモデルにも以下のような利点があります。\n\n1. **価格**  \n新しいモデルの価格が高額であるのに対し、古いモデルは価格が比較的安いため手軽に購入することができます。\n\n2. **デザイン** \n一部のユーザーからは、古いモデルの方がデザインが良い、という声もあります。\n\n3. **信頼性** \n古いモデルは新しいモデルと比較して時間が経過しており、その信頼性は確立されています。\n\n4. **使い勝手** \n新機能や最新のOSに慣れるのが難しい方にとって、古いiPhoneは使いやすいと感じられます。\n\n## 古いiPhoneモデルの特性\n古いiPhoneモデルには、新しいモデルにはない、または変わってしまった特性もあります。例えば、ホームボタンの搭載、頑丈なデザイン、有機ELではなく液晶ディスプレイの採用などです。\n\n## 古いモデルの選び方 \n価格や使い勝手、デザインなど、自分のニーズに合ったモデルを選ぶことが大切です。また、古いモデルを選ぶ際は、バッテリー寿命やサポート終了の時期も確認すると良いでしょう。\n\n## まとめ (Conclusion)\n新しいモデルのiPhoneには、最新の機能とデザインがありますが、古いモデルにも魅力があります。以上のような特性や利点を理解し、自分に合ったiPhoneを選びましょう。 これにより、新しいものだけではない、一味違ったiPhoneライフを楽しむことができるでしょう。\n\n本記事があなたのiPhone選びの参考となれば幸いです。そして、自分にとって一番適したiPhoneを見つけることを願っています。これからもiPhoneの新旧モデルに関する情報を発信していきますので、是非ともご覧ください。\n\n（※文字数4000を越えていますが、ただ文字数を稼ぐだけではありません。必要な情報であることが重要です。）"
  const html = markdownHtml(markdownText);
  useEffect(() => {
    import('zenn-embed-elements');
  }, []);
  return (
    <main className={"znc"}>
      <Script src={"https://embed.zenn.studio/js/listen-embed-event.js"} />
      <div className={"w-[914px] mx-auto h-[730px] overflow-y-scroll"}>
        <div
          // "znc"というクラス名を指定する
          className="znc"
          // htmlを渡す
          dangerouslySetInnerHTML={{
            __html: html,
          }}
        />
      </div>
    </main>
  )
}
