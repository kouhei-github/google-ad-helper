import Link from "next/link";

export const Latest = (props: {links: {title: string, id: number, ogp_image: string}[], title: string}) => {
  const { links, title } = props
  return (
    <div className={"w-[300px] h-[800px] bg-white rounded-xl overflow-y-scroll px-4 pb-5 sticky top-10"}>
      <h3 className={"font-bold text-xl text-center my-6 border-b-2 border-gray-200"}>{title}</h3>
      <div className={"h-full"}>
        {links.map((url, index) => (
          <Link href={`/article/${url.id}`} key={index} className={"underline py-5 underline-offset-2 text-blue-500 hover:text-blue-700"}>
            <img src={url.ogp_image} alt={"画像"} />
            <p className={"overflow-ellipsis overflow-hidden whitespace-nowrap mb-5"}>{url.title}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
