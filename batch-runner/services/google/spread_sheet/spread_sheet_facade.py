from services.google.spread_sheet.config import GoogleSpreadSheetConfig
from typing import List, Any

class SpreadSheetFacade(GoogleSpreadSheetConfig):
    """
    SpreadSheetFacade` クラスは `GoogleSpreadSheetConfig` のサブクラスである。Google Spreadsheet にデータを書き込んだり、その中の特定のシートからデータを取得したりするためのメソッドを提供します。
    * スプレッドシート内の特定のシートからデータを取得するメソッドを提供します。

    属性
        last_col_num (int)： シート内の最後のカラム番号。
        last_row_alpha (str)： シートの最後の行のアルファベット。

    メソッド
        __init__(spread_id: str, scope: str)
            指定された `spread_id` と `scope` で `SpreadSheetFacade` オブジェクトを初期化する。

            パラメータ
                spread_id (str)： アクセスする Google Spreadsheet の ID。
                scope (str)： アクセスする Google Spreadsheet のスコープ。

        write_sheet(sheet_name: str, values: List[List[str]])
            指定した値をスプレッドシート内の指定したシートに書き込む。

            パラメータ
                sheet_name (str)： データが書き込まれるシートの名前。
                values (List[List[str]])： スプレッドシートに書き込む値。各内部リストは、スプレッドシートの行を表します。

        get_values(sheet_name: str) -> リスト[List[Any]].
            スプレッドシート内の指定したシートの値を取得します。

            パラメータ
                sheet_name (str)： 値を取得するシートの名前。

            戻り値
                List[List[Any]]： シートの行と列を表すリストのリスト。

    """
    def __init__(self, spread_id: str, scope: str):
        """
        引数
            spread_id (str)： アクセスする Google Spreadsheet の ID。
            scope (str)： アクセスする Google Spreadsheet のスコープ。
        """
        super().__init__(spread_id, scope)
        self.last_col_num = None
        self.last_row_alpha = None

    async def write_sheet(self, sheet_name: str, values: List[List[str]], spread_sheet_range=None):
        """
        引数
            sheet_name (str)： データが書き込まれるシートの名前。
            values (List[List[str]])： スプレッドシートに書き込まれる値。各内部リストはスプレッドシートの行を表す。

        """
        if spread_sheet_range is None:
            spread_sheet_range = f'{sheet_name}!A{self.last_col_num}:{self.last_row_alpha}{self.last_col_num + len(values) - 1}'
        self.sheet.values().update(
            spreadsheetId=self.spread_id,
            range=spread_sheet_range,
            valueInputOption="USER_ENTERED",
            body={"values": values}
        ).execute()

    def get_values(self, sheet_name: str) -> List[List[Any]]:
        """
        引数
            sheet_name (str)： 値を取得するシートの名前。

        戻り値
            リスト[List[Any]]： シートの値の行と列を表すリストのリスト

        """
        # Request for all rows in the 'sheet_name' sheet
        result = self.sheet.values().get(
            spreadsheetId=self.spread_id,
            range=sheet_name,
        ).execute()

        # Get list of rows
        rows = result.get('values', [])
        self.last_col_num = len(rows) + 1
        self.last_row_alpha = SpreadSheetFacade.toAlpha(len(rows[0]))
        return rows
