'use client'

import {useEffect, useState} from "react";
import Link from "next/link";

export default function Home() {
  const [tags, setTags] = useState<{id: number, name: string}[]>([{
    id: 1, name: ""
  }])

  const [page, setPage] = useState<number>(1)
  useEffect(() => {
    const fetcher = async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER_URL}/tag/all?page=${page}`)
      const result = await res.json() as Promise<{id: number, name: string}[]>
      setTags(await result)
    }
    fetcher()
  }, [page]);

  const prev = () => {
    if (page == 1) return
    setPage(page-1)
  }

  const next = () => {
    if(tags.length === 0) return
    setPage(page+1)
  }

  const [search, setSearch] = useState<string>("")

  return (
    <main className={"w-[100%] mx-auto my-12 "}>
      <section className="relative">
        <img className="h-[320px] w-full object-cover" src="/images/background-programming.webp" alt="ビギナー画像"/>
        <div className="absolute top-0 h-[320px] bg-black w-full opacity-60"></div>
        <div
          className="absolute top-1/2 transform -translate-y-1/2 left-1/2-translate-x-1/2 text-center text-white w-full mx-auto">
          <h2 className="md:text-[32px] text-[18px]">
            <span className="text-[#4DABF7]">&quot;キーワード&quot;</span>でツールを検索
          </h2>
          <div className="md:text-[16px] text-[13px] leading-8 md:w-full w-11/12 mx-auto">
            <p>プログラミング言語・フレームワーク・クラウドサービスを検索しましょう。</p>
            <p>技術に対応した記事をご紹介いたします</p>
          </div>
        </div>
      </section>


      <section className="relative mt-5 mx-auto md:w-4/5 w-[95%]">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          type="text"
          placeholder="キーワードでツールを検索..."
          className="border border-[#333333] text-[#333333] w-full md:px-4 px-2 md:py-3 py-1 text-left"
        />
        <button
          className="absolute top-1/2 right-0 transform -translate-y-1/2 w-max px-2 h-full group hover:bg-purple-200">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"
               className="group-hover:fill-purple-500" focusable="false">
            <path
              d="m18.031 16.617 4.283 4.282-1.415 1.415-4.282-4.283A8.96 8.96 0 0 1 11 20c-4.968 0-9-4.032-9-9s4.032-9 9-9 9 4.032 9 9a8.96 8.96 0 0 1-1.969 5.617zm-2.006-.742A6.977 6.977 0 0 0 18 11c0-3.868-3.133-7-7-7-3.868 0-7 3.132-7 7 0 3.867 3.132 7 7 7a6.977 6.977 0 0 0 4.875-1.975l.15-.15z"></path>
          </svg>
        </button>
      </section>

      <section className="my-5 w-full mx-auto grid md:grid-cols-6 grid-cols-3 gap-3  bg-white py-3">
        {tags.map((tag) => (
          (search === "" ? (
            <Link href={`/tags/${tag.name}/`} className="w-max mx-auto hover:bg-[#EDF2F7]" key={tag.id}>
              <p
                className="text-center text-[#333333] rounded-full md:text-[12px] text-[9px] border border-gray-300 py-1 px-3"># {tag.name}</p>
            </Link>
          ) : (
            (tag.name.includes(search) ? (
              <Link href={`/tags/${tag.name}/`} className="w-max mx-auto hover:bg-[#EDF2F7]" key={tag.id}>
                <p
                  className="text-center text-[#333333] rounded-full md:text-[12px] text-[9px] border border-gray-300 py-1 px-3"># {tag.name}</p>
              </Link>
            ) : (<></>))
          ))
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
