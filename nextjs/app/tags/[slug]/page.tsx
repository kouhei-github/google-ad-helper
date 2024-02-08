import Link from "next/link";
import {Tag} from "@/app/article/[slug]/components/SidBar/Tag";

// export const dynamicParams = false

export async function generateStaticParams() {
  // 一覧を取得する
  const res  = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER_URL}/tag/all`, {next: {revalidate: 60}})
  if (!res.ok) throw new Error("failed to fetch wine")
  const datas: {id: number}[] = await res.json()

  return datas.map((data) => {
    {slug: data.id}
  })
}


async function getArticle(tag: string): Promise<{title: string, id: number, ogp_image: string, tags: string[]}[]> {
  const res  = await fetch(
    `${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/tag/${tag}`,
    {next: {revalidate: 60}}
  )

  if (!res.ok) throw new Error("failed to fetch wine")

  return await res.json() as {title: string, id: number, ogp_image: string, tags: string[]}[]

}


const TagArticlePage = async ({params: { slug }}: {params: {slug: string}}) => {
  const articles = await getArticle(slug)

  let relatedArray: string[] = []
  for (const article of articles) {
    relatedArray = relatedArray.concat(article.tags)
  }

  relatedArray = Array.from(new Set(relatedArray))

  return (
    <main className={"w-[100%] mx-auto my-12 "}>
      <section className="relative">
        <img className="h-[320px] w-full object-cover" src="/images/background-programming.webp" alt="ビギナー画像"/>
        <div className="absolute top-0 h-[320px] bg-black w-full opacity-60"></div>
        <div
          className="absolute top-1/2 transform -translate-y-1/2 left-1/2-translate-x-1/2 text-center text-white w-full mx-auto">
          <h2 className="md:text-[32px] text-[18px]">
            <span className="text-[#4DABF7]">&quot;{slug}&quot;</span>に関わる記事
          </h2>
          <div className="md:text-[16px] text-[13px] leading-8 md:w-full w-11/12 mx-auto">
            <p>{slug}を学んで行きましょう！</p>
            <p>世界各国の良質な記事で最大限にサポートします。</p>
          </div>
        </div>
      </section>

      <h1 className={"w-full text-center py-2 bg-white mt-3 mb-2"}>検索対象の記事</h1>
      <div className={"flex flex-col md:flex-row md:mt-5"}>
        <section className={"h-full border p-3  space-y-3 md:grid md:grid-cols-2 md:gap-3 md:space-y-0 w-full"}>
          {articles.map((article, index) => (
            <div key={index} className={"border my-1 md:my-0  bg-white"}>
              <div key={index} className={"py-2"}>
                <img src={article.ogp_image} alt={"画像"} className={"w-[98%] mx-auto h-[125px] object-cover"}/>
                <div className={"grid grid-cols-2 gap-x-2 gap-y-1"}>
                  {article.tags.map((tag, index) => (
                    <Link href={`/tags/${tag}`} key={index} className={"text-sm mx-auto text-left"}>
                      <span className={"text-green-400 mr-1"}>#</span>{tag}
                    </Link>
                  ))}
                </div>

                <Link href={`/article/${article.id}`} className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>{article.title}</Link>
              </div>
            </div>
          ))}
        </section>

        <section >
          <Tag tags={relatedArray} title={"関連する技術"} />
        </section>
      </div>


    </main>
  )
}
export default TagArticlePage
