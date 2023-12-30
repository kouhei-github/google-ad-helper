import Link from "next/link";

export const Tag = (props: {tags: string[], title: string}) => {
  const { tags, title } = props
  return (
    <div className={"w-[300px] h-[275px] bg-white rounded-xl overflow-y-scroll px-4 pb-5"}>
      <h3 className={"font-bold text-xl text-center my-6 border-b-2 border-gray-200"}>{title}</h3>
      <div className={"space-y-3"}>
        {tags.map((tag, index) => (
          <div key={index} className={"underline underline-offset-2 text-blue-500 hover:text-blue-700"}>
            <Link href={`/tags/${tag}`}>
              {tag}に関連する記事
            </Link>
          </div>
        ))}
      </div>
    </div>
)
}
