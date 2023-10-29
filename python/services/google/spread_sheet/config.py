import os
from typing import List
from googleapiclient.discovery import build
from google.oauth2 import service_account
from services.google.spread_sheet.spread_sheet_error import SpreadSheetScopeSelectError

class GoogleSpreadSheetConfig:
    """
        GoogleSpreadSheetConfig` クラスは Google Spreadsheet サービスを設定するためのもので、 スコープの設定、数値と文字の変換、および以下のメソッドを含む。
        * サービスのスプレッドシートを取得するためのメソッドが含まれます。

        属性
            credential_json (dict)： Googleサービスのアカウント情報を含む辞書。
                - "type"： クレデンシャルのタイプ。
                - "project_id": プロジェクトID： プロジェクトID。
                - "private_key_id": 秘密鍵のID： 秘密鍵のID。
                - "private_key": 秘密鍵： 秘密鍵。
                - "client_email": クライアントメール： クライアントのメールアドレス。
                - "client_id": クライアントID： クライアントのID。
                - "auth_uri": 認証URI： 認証URI。
                - "token_uri": トークンURI： トークンURI。
                - "auth_provider_x509_cert_url": 認証プロバイダーのX.509証明書のURL。
                - "client_x509_cert_url": クライアントのX.509証明書のURL： クライアントのX.509証明書のURL。
                - "universe_domain"： ドメイン。

        メソッド：
            __init__(spread_id: str, scope: str)
                GoogleSpreadSheetConfig` クラスの新しいインスタンスを初期化する。

            _create_spread_sheet_service(スコープ: リスト[str])
                指定したスコープに基づく Google Spreadsheet サービスを作成して返します。

            set_scope(scope: str) -> リスト[str]。
                指定されたスコープの値に基づいて適切なスコープを設定します。

            toAlpha(num: int) -> str
                表計算で使用するために数値を対応するアルファベットに変換します。

            toNumber(alphabet: str) -> int
                アルファベットを対応する数値に変換する。

        """
    credential_json = {
        "type": os.environ["TYPE"],
        "project_id": os.environ["PROJECT_ID"],
        "private_key_id": os.environ["PRIVATE_KEY_ID"],
        "private_key": os.environ["PRIVATE_KEY"],
        "client_email": os.environ["CLIENT_EMAIL"],
        "client_id": os.environ["CLIENT_ID"],
        "auth_uri": os.environ["AUTH_URI"],
        "token_uri": os.environ["TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_CERT_URI"],
        "client_x509_cert_url": os.environ["CLIENT_CERT_URI"],
        "universe_domain": os.environ["DOMAIN"]
    }

    def __init__(self, spread_id: str, scope: str):
        """
        GoogleSpreadSheetConfig オブジェクトを初期化します。

        引数
            spread_id (str)： Google スプレッドシートの ID。
            scope (str)： スプレッドシートのアクセススコープ。

            パラメータ `scope` には有効な Google API スコープを指定します。これは
            スプレッドシートに対するアプリケーションのアクセスレベルを定義します。

            spread_id` パラメータは、Google スプレッドシートの一意な識別子となります。

        属性を指定します：
            sheet： 指定した `scope` を用いて作成された Google スプレッドシートサービスのインスタンス。
            spread_id (str)： Google スプレッドシートの ID。

        エラー：
            SpreadSheetScopeSelectError： 指定した `scope` が無効な場合。

        """
        scope: List[str] = self._set_scope(scope)
        self.sheet = self._create_spread_sheet_service(scope)
        self.spread_id: str = spread_id

    @classmethod
    def _create_spread_sheet_service(cls, scopes: List[str]):
        """
        引数
            scopes (List[str])： サービスアカウントに付与する Google API スコープのリスト。

        戻り値
            googleapiclient.discovery.Resource`： Google Sheets サービスリソース。

        戻り値: `googleapiclient.discovery.Resource`: Google Sheets サービスリソース
            SpreadSheetScopeSelectError： シートスコープの選択に失敗した場合に発生する。
        """
        credentials = service_account.Credentials.from_service_account_info(cls.credential_json)
        credentials.with_scopes(scopes)
        service = build('sheets', 'v4', credentials=credentials)
        return service.spreadsheets()

    @staticmethod
    def _set_scope(scope: str) -> List[str]:
        """
        引数
            scope (str)： Googleスプレッドシートのアクセス範囲。
                         read" あるいは "write" のいずれかを指定する。

        戻り値
            List[str]： 指定したアクセススコープに必要な Google API スコープのリスト。

        レイズ
            SpreadSheetScopeSelectError： 無効なスコープが指定された場合。

        説明
        このメソッドは、Google Spreadsheet のアクセススコープを設定します。単一の引数 'scope' を指定します。 この引数には、アクセス形式を表す文字列を指定します。サポートされる
        * スコープの値は次のとおりです：

        - read"： Google スプレッドシートへの読み込み専用アクセスを表します。
        - write"： Google スプレッドシートへの読み書きアクセスを表します。

        このメソッドは、指定したアクセススコープに必要な Google API スコープの一覧を返します。無効なスコープを指定した場合は、SpreadSheetScopeSelectError が発生します。
        * エラーメッセージが表示されます。
        """
        match scope:
            case "read":
                return ["https://www.googleapis.com/auth/drive.readonly"]
            case "write":
                return ["https://www.googleapis.com/auth/spreadsheets"]
            case _:
                msg = """
                SCOPEは下記の二つで選択してください。
                読み込みのみの場合 -> read

                書き込みと読み込み両方の場合 -> write
                """
                raise SpreadSheetScopeSelectError(msg)

    @staticmethod
    def toAlpha(num: int) -> str:
        """数字からスプレッドシート用のアルファベットに変換

        Args:
            num (int): アルファベットへ変換したい数字

        Returns:
            str: アルファベット
        """
        if num <= 26:
            return chr(64 + num)
        elif num % 26 == 0:
            return GoogleSpreadSheetConfig.toAlpha(num // 26 - 1) + chr(90)
        else:
            return GoogleSpreadSheetConfig.toAlpha(num // 26) + chr(64 + num % 26)

    @staticmethod
    def toNumber(alphabet: str) -> int:
        """アルファベットから数字へ変換

        Args:
            alphabet (str): 数字に変換したいアルファベット

        Returns:
            int: 数字
        """
        num = 0
        for index, item in enumerate(list(alphabet)):
            num += pow(26, len(alphabet) - index - 1) * \
                (ord(item) - ord('A') + 1)
        return num
