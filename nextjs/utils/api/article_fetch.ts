import useSWR from "swr";

type response = {
  description: string
  story:  string
  title:  string
  tags: string[]
}

type Article = {
  article?: response
  isLoading: boolean
  isError: string
}

const articleFetcher = async (url: string) => {
  const result = await fetch(url)
  return await result.json() as Promise<response>
}

export const useGetArticle = (article_id: number): Article => {
  const { data, error, isLoading} = useSWR(
    `${process.env.NEXT_PUBLIC_API_SERVER_URL}/seo/show/${article_id}`,
    articleFetcher
  )

  return {
    article: data,
    isLoading,
    isError: error
  }
}
