import { MetadataRoute } from "next";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_URL ?? '';
  const lastModified = new Date();

  const staticPaths = [
    {
      url: `${baseUrl}`,
      lastModified,
    },
    {
      url: `${baseUrl}/tags`,
      lastModified,
    },
    {
      url: `${baseUrl}/tags`,
      lastModified,
    },
    {
      url: `${baseUrl}/article`,
      lastModified,
    },
  ];

  //　記事一覧を取得する
  const articles = await getArticles();
  const dynamicPaths = articles.map((article) => {
    return {
      url: `${baseUrl}/article/${article.id}`,
      lastModified,
    };
  });

  //　タグ一覧を取得する
  const tags = await getTags()
  const dynamicTagPaths = tags.map((tag) => {
    return {
      url: `${baseUrl}/tags/${tag.name}`,
      lastModified,
    };
  });

  return [...staticPaths, ...dynamicPaths, ...dynamicTagPaths];
}


const getArticles = async () => {
  let articles: {id: number, title: string}[] = []
  let flag = true
  let count= 1
  while (flag) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER_URL}/article/all?page=${count}`)
    const result = await res.json() as {id: number, title: string}[]
    if (result.length === 0) flag = false
    articles = articles.concat(result)
    count++
  }
  return articles
}

const getTags = async () => {
  let tags: {id: number, name: string}[] = []
  let flag = true
  let count= 1

  while (flag) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_SERVER_URL}/tag/all?page=${count}`)
    const result = await res.json() as {id: number, name: string}[]
    if (result.length === 0) flag = false
    tags = tags.concat(result)
    count++
  }
  return tags
}
