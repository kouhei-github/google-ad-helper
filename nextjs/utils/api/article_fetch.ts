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

export const useGetArticle = (articleId: number): Article => {
  const { data, error, isLoading} = useSWR(
    `${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/show/${articleId}`,
    articleFetcher
  )

  return {
    article: data,
    isLoading,
    isError: error
  }
}
