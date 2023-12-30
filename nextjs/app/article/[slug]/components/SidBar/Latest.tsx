import Link from "next/link";

export const Latest = (props: {links: {title: string, id: number, ogp_image: string, tags: string[]}[], title: string}) => {
  const { links, title } = props
  return (
    <div className={"w-[98%] md:w-[300px] h-full md:h-[800px] bg-white rounded-xl overflow-y-scroll px-4 pb-5 sticky top-10"}>
      <h3 className={"font-bold text-xl text-center my-6 border-b-2 border-gray-200"}>{title}</h3>
      <div className={"h-full space-y-3"}>
        {links.map((url, index) => (
          <div key={index} className={"border my-1 md:my-0  bg-white"}>
            <div key={index} className={"py-2"}>
              <img src={url.ogp_image} alt={"画像"} className={"w-[98%] mx-auto h-[125px] object-cover"}/>
              <div className={"grid grid-cols-2 gap-x-2 gap-y-1"}>
                {url.tags.map((tag, index) => (
                  <Link href={`/tags/${tag}`} key={index} className={"text-sm mx-auto text-left"}>
                    <span className={"text-green-400 mr-1"}>#</span>{tag}
                  </Link>
                ))}
              </div>

              <Link href={`/article/${url.id}`}
                    className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>{url.title}</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
