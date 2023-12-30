import markdownHtml from "zenn-markdown-html";
import Script from "next/script";
import {Tag} from "@/app/article/[slug]/components/SidBar/Tag";
import {Latest} from "@/app/article/[slug]/components/SidBar/Latest";

type articleI = {
  description: string
  story:  string
  title:  string
  tags: string[]
}
// export const dynamicParams = false

export async function generateStaticParams() {
  // 一覧を取得する
  const res  = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/all`, {next: {revalidate: false}})
  if (!res.ok) throw new Error("failed to fetch wine")
  const datas: {id: number}[] = await res.json()

  return datas.map((data) => {
    {slug: data.id}
  })
}

async function getArticle(articleId: number): Promise<articleI&{latest: {title: string, id: number, ogp_image: string}[]}> {
  let res  = await fetch(
    `${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/show/${articleId}`,
    {next: {revalidate: false}}
  )

  if (!res.ok) throw new Error("failed to fetch wine")

  const article = await res.json() as articleI

  res  = await fetch(
    `${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/latest`,
    {next: {revalidate: 1800}}
  )

  if (!res.ok) throw new Error("failed to fetch wine")

  const latest = {latest: await res.json() as {id: number, title: string, ogp_image: string}[]}

  return { ...article, ...latest }
}


const  JobDetailPage = async ({params: { slug }}: {params: {slug: number}}) => {
  const article = await getArticle(slug)
  const html = markdownHtml(article.story);
  return (
    <main className={"w-11/12 md:w-[100%] mx-auto  my-12 flex space-x-8 "}>
      <Script src={"https://embed.zenn.studio/js/listen-embed-event.js"}/>
      <section
        // "znc"というクラス名を指定する
        className="znc md:w-[75%] w-[100%] bg-[#FFFFFF] p-8 rounded-xl"
        // htmlを渡す
        dangerouslySetInnerHTML={{
          __html: html,
        }}
      />

      <section className={"w-[25%] md:block hidden min-h-screen space-y-4"}>
        <Tag tags={article.tags} title={"タグ"} />

        <Latest links={article.latest} title={"最新の記事"} />
      </section>
    </main>
  )
}

export default JobDetailPage
