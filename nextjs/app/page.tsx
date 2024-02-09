"use client"
import {useEffect, useState} from "react";
import Link from "next/link";
import {Tag} from "@/app/article/[slug]/components/SidBar/Tag";
import { useRouter, useSearchParams} from 'next/navigation'

export default function Home() {

  const [articles, setArticles] = useState<{title: string, id: number, ogp_image: string, tags: string[]}[]>([
    {title: "", id: 1, tags: [], ogp_image: ""}
  ])
  const [relatedArray, setRelatedArray] = useState<string[]>([])

  const router = useRouter()
  const params = useSearchParams()
  const [page, setPage] = useState<number>(Number(params.get("page") ? params.get("page") : 1))


  useEffect(() => {
    const fetcher = async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/latest?page=${page}`)
      const result = await res.json() as Promise<{title: string, id: number, ogp_image: string, tags: string[]}[]>
      setArticles(await result)
      let tags: string[] = []
      for (const article of await result) {
        article.tags.forEach((tag) => {
          if (!tags.includes(tag)) tags.push(tag)
        })
      }
      setRelatedArray(tags)
    }
    fetcher()
    router.push(`/?page=${page}`)
  }, [page]);

  const prev = () => {
    if (page == 1) return
    setPage(page-1)
  }

  const next = () => {
    if(articles.length === 0) return
    setPage(page+1)
  }

  return (
    <main className={"w-[100%] mx-auto my-12 "}>
      <section className="relative">
        <img className="h-[320px] w-full object-cover" src="/images/background-programming.webp" alt="ビギナー画像"/>
        <div className="absolute top-0 h-[320px] bg-black w-full opacity-60"></div>
        <div
          className="absolute top-1/2 transform -translate-y-1/2 left-1/2-translate-x-1/2 text-center text-white w-full mx-auto">
          <h2 className="md:text-[32px] text-[18px]">
            <span className="text-[#4DABF7]">&quot;技術記事&quot;</span>に関わる記事
          </h2>
          <div className="md:text-[16px] text-[13px] leading-8 md:w-full w-11/12 mx-auto">
            <p>プログラミングを学んで行きましょう！</p>
            <p>世界各国の良質な記事で最大限にサポートします。</p>
          </div>
        </div>
      </section>

      <h1 className={"w-full text-center py-2 bg-white mt-3 mb-2 cursor-pointer"}>
        <Link href={"/tags"} className={"underline underline-offset-2 text-blue-500 text-[18px] md:text-[24px]"}>こちらからプログラミング言語で<br className={"md:hidden block"} />記事を検索</Link>

      </h1>
      <div className={"flex flex-col md:flex-row"}>
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

                <Link href={`/article/${article.id}`}
                      className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>{article.title}</Link>
              </div>
            </div>
          ))}
        </section>

        <section>
          <Tag tags={relatedArray} title={"関連する技術"}/>
        </section>
      </div>
      <section className={"flex items-center justify-center space-x-5 bg-white py-2 mt-5"}>
        <div className={"border px-3 py-2 cursor-pointer md:hover:bg-purple-200 md:hover:text-purple-500"}
             onClick={() => prev()}>前へ
        </div>
        <div className={"px-3 py-2"}>{page}</div>
        <div className={"border px-3 py-2 cursor-pointer md:hover:bg-purple-200 md:hover:text-purple-500"}
             onClick={() => next()}>次へ
        </div>
      </section>
    </main>
  )
}
