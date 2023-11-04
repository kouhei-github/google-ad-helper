# requestsとurlencodeライブラリをインポートしています。これらは、APIリクエストの送信とURLのエンコードに使用されます。
import requests
from urllib.parse import urlencode

# ConvertUrlToMarkdownという名前のクラスを定義しています。このクラスは、URLをマークダウン形式に変換する機能を持っています。
class ConvertUrlToMarkdown:
    """
    マークダウンへの変換

    このクラスは、URLをマークダウン・フォーマットに変換する静的メソッドを提供します。

    メソッドを提供します：
        convert(url: str) -> str：
            URLを受け取り、外部APIを使ってマークダウン形式に変換します。

            パラメータ
                url (str)： 変換されるURL。

            戻り値
                str： マークダウン形式に変換されたURL。
    """

    # convertという名前の静的メソッドを定義しています。このメソッドでは指定したURLを取得し、マークダウン形式に変換します。
    @staticmethod
    def convert(url: str):
        """
        引数
            url (str)： マークダウンに変換したいウェブページのURL。

        戻り値
            str： 変換されたウェブページのマークダウン・テキスト。

        例
            >>> convert('https://example.com')
            'これはマークダウンに変換されたウェブページの例です。
        """

        # リクエストの本体とヘッダーを空の辞書で初期化します。これらは、後でAPIリクエストを行うために使用されます。
        payload = {}
        headers = {}

        # 変換するURLを指定したマークダウンに変換するAPIエンドポイントのURLを設定しています。
        base = "https://urltomarkdown.herokuapp.com/"

        # URLをマークダウンに変換するためのクエリパラメータを設定しています。特に、'url'、'title'、'links'の3つのキーを持つ辞書です。
        query = {
            'url': url,
            'title': "true",
            'links': "true",
        }

        # APIエンドポイントのURLとクエリパラメータを組み合わせて、完全なAPIリクエストURLを作成します。
        url = '%s?%s' % (base, urlencode(query))

        # requestsライブラリを使用してGETリクエストを送信し、その結果を受け取ります。
        response = requests.request("GET", url, headers=headers, data=payload)

        # レスポンスの本文（変換されたマークダウン）を返します。
        return response.text
