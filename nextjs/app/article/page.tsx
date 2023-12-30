'use client'
import {useEffect, useState} from "react";
import Link from "next/link";

type response = {
  id: number
  story: string
  description: string
  title: string
  ogp_image: string
  tags: string[]
}


const tags = ["vue", "golang", "javascript", "ai", "python", "docker","laravel","node", "ruby", "swift", "react", "github"]

export default function Home() {
  const [article, setArticle] = useState<response[]>([{
    id: 1, story: "", description: "", title: "", ogp_image: "", tags: [""]
  }])

  const [page, setPage] = useState<number>(1)
  useEffect(() => {
    const fetcher = async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/all?page=${page}`)
      const result = await res.json() as Promise<response[]>
      setArticle(await result)
    }
    fetcher()
  }, [page]);

  const prev = () => {
    if (page == 1) return
    setPage(page-1)
  }

  const next = () => {
    if(article.length === 0) return
    setPage(page+1)
  }

  return (
    <main className={"w-[100%] mx-auto my-12 "}>

      <div className="relative">
        <img className="h-[320px] w-full object-cover" src="/images/background-programming.webp" alt="ビギナー画像"/>
        <div className="absolute top-0 h-[320px] bg-black w-full opacity-60"></div>
        <div className="absolute top-1/2 transform -translate-y-1/2 left-1/2-translate-x-1/2 text-center text-white w-full mx-auto">
          <h2 className="md:text-[32px] text-[18px]">
            <span className="text-[#4DABF7]">"プログラミング"</span>に関する記事
          </h2>
          <div className="md:text-[16px] text-[13px] leading-8 md:w-full w-11/12 mx-auto">
            <p>プログラミングに困ったらこちらの記事はチェックしてみましょう。</p>
            <p>プログラミングサイトとして最大級であるdev.toの記事を日本語でまとめています。</p>
          </div>
          <div className="my-5 md:w-2/3 w-full mx-auto grid md:grid-cols-6 grid-cols-4 gap-3">
            {tags.map((tag, index) => (
              <Link href={`/tags/${tag}/`} className="w-max mx-auto" key={index}>
                <p className="text-center bg-[#228BE6] text-white rounded-full md:text-[12px] text-[9px] px-2 py-1"># {tag}</p>
              </Link>
            ))}
          </div>

        </div>
      </div>
      <h2 className={"text-center md:text-2xl text-[17px] md:my-6 my-2 bg-white py-3"}>記事一覧</h2>
      <section className={"md:grid-cols-3 md:grid md:gap-2.5"}>
        {article.map((data, index) => (
          <div key={index} className={"border my-4 md:my-0  bg-white"}>
            <div key={index} className={"py-2"}>
              <img src={data.ogp_image} alt={"画像"} className={"w-[98%] mx-auto h-[125px] object-cover"}/>
              <div className={"grid grid-cols-2 gap-x-2 gap-y-1"}>
                {data.tags.map((tag, index) => (
                  <Link href={`/tags/${tag}`} key={index} className={"text-sm mx-auto text-left"}>
                    <span className={"text-green-400 mr-1"}>#</span>{tag}
                  </Link>
                ))}
              </div>

              <Link href={`/article/${data.id}`}
                    className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>{data.title}</Link>
            </div>
          </div>
        ))}
      </section>
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
