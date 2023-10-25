/**
 * 配列で定義されたカスタムの型を抽出したい時に使う
 *
 * 使い方:
 * type content = {
 *     img: string
 *     altName: string
 * }
 *
 * type Job = {
 *     contents: content[]
 *     title:    string
 *     subTitle: string
 * }
 *
 * Filter<Job, "contents">[0]  // content => [0]とすることでcontent[]ではなくcontentが取得できる
 */
export type Filter<T, K extends keyof T> = CustomRequired<T> extends { [P in K]: infer C } ? C : never


/**
 * 特定の方から特定のプロパティのみを抽出
 *
 * 使い方:
 * type Job = {
 *     contents: content[]
 *     title:    string
 *     subTitle: string
 * }
 *
 * PickItUp<Job, "subTitle"> //  {subTitle: string }
 */
export type PickItUp<T, K extends keyof T> = {
    [P in K]: T[P]
}

/**
 * 特定の方から特定のプロパティ以外を抽出
 *
 * 使い方:
 * type Job = {
 *     contents: content[]
 *     title:    string
 *     subTitle: string
 * }
 *
 * CustomOmit<Job, "subTitle"> // {title: string, contents: content[]}
 *
 */
type customOmitKey<T, K> = {
    [P in keyof T]: P extends K ? never : P
}[keyof T]

export type CustomOmit<T, K extends keyof T > = {
    [P in customOmitKey<T, K>]: T[P]
}


/**
 * 特定の方をオプショナルにする(undefined) // 正確に言うとundefinedとは挙動が変わる
 *
 * 使い方:
 * type Job = {
 *     contents: content[]
 *     title:    string
 *     subTitle: string
 * }
 *
 * Optional<Job> // { contents?: content[], title?: string, subTitle?: string }
 */
export type Optional<T> = {
    [K in keyof  T]?: T[K]
}

/**
 * 特定オプショナルの型を必須にする(undefined) // 正確に言うとundefinedとは挙動が変わる
 *
 * 使い方:
 * type Job = {
 *     contents?: content[]
 *     title?:    string
 *     subTitle?: string
 * }
 *
 * Optional<Job> // { contents: content[], title: string, subTitle: string }
 */
export type CustomRequired<T> = {
    [K in keyof T]-?: T[K]
}
