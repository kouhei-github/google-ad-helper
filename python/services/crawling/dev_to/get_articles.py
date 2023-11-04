# requestsライブラリと標準ライブラリのreモジュールをインポートします。これらは、APIリクエストの送信と正規表現マッチングに使用されます。
import re
import requests
from typing import List

# GetArticlesInDevToという名前のクラスを定義しています。このクラスは、dev.to ウェブサイトから記事を取得し、解析する機能を持っています。
class GetArticlesInDevTo:
    """
    クラス GetArticlesInDevTo

    dev.to ウェブサイトから記事を取得し、解析するためのクラス。

    属性
        url (str)： dev.toの最新記事ページのURL。
        html (str)： 最新記事ページのHTMLコンテンツ。

    メソッド
        __init__(self)：
            GetArticlesInDevToクラスの新しいインスタンスを初期化する。

        get_latest_article(self)：
            最新記事ページのHTMLコンテンツを取得し、'html'属性を更新する。

        get_attribute(self, start: str, end: str) -> List[str]：
            HTMLコンテンツ内の特定の属性の全ての出現回数を取得する。
    """

    # dev.toの最新記事ページのURLをクラス属性として設定します。
    url = "https://dev.to/latest"

    # クラスのインスタンス化時に、ページのHTMLコンテンツを格納するための空のプロパティニを作成します。
    def __init__(self):
        self.html = ""

    # 指定されたURLから最新の記事を取得するメソッドを定義します。 その結果をインスタンス属性のhtmlに格納します。
    def get_latest_article(self):
        """
        指定されたURLから最新の記事を取得する。

        戻り値
            None: 記事が見つからないか、エラーが発生した場合。
            str： 最新記事のHTMLコンテンツ。

        """
        payload = {}
        headers = {}

        # requestsライブラリを使用してGETリクエストを送信し、その結果を受け取ります。
        response = requests.request("GET", self.url, headers=headers, data=payload)

        # レスポンスの本文（HTML）を保存します。
        self.html = response.text


    # 特定の属性をHTMLコンテンツから抽出するためのメソッドを定義します。これは、開始と終了文字列の間の内容をリスト形式で返します。
    def get_attribute(self, start: str, end: str) -> List[str]:
        """
        引数
            start (str)： HTMLの検索開始文字列。
            end (str)： HTML内で検索する終了文字列。

        戻り値
            リスト[str]： HTMLの開始文字列と終了文字列の間にある文字列のリスト。
        """

        # 開始と終了文字列間のすべてのマッチを見つけるための正規表現パターンを定義します。
        pattern = f'{re.escape(start)}(.*?){re.escape(end)}'

        # 上記で定義した正規表現パターンを使ってHTMLコンテンツにあるマッチを全て見つけます。
        matches = re.findall(pattern, self.html)

        # マッチしたすべての文字列をリストとして返します。
        return matches
