import Link from "next/link";

export const Latest = (props: {links: {title: string, id: number}[], title: string}) => {
  const { links, title } = props
  return (
    <div className={"w-[300px] h-[405px] bg-white rounded-xl overflow-y-scroll px-4 pb-5 sticky top-10"}>
      <h3 className={"font-bold text-xl text-center my-6 border-b-2 border-gray-200"}>{title}</h3>
      <div className={"space-y-3"}>
        {links.map((url, index) => (
          <div key={index} className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>
            <Link href={`/article/${url.id}`}>{url.title}</Link>
          </div>
        ))}
      </div>
    </div>
  )
}
