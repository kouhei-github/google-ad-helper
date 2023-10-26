from .config import GoogleAdvertisementConfig
from typing import List, Any

class GoogleAdvertisementSearchWordFacade(GoogleAdvertisementConfig):
    """
    Class GoogleAdvertisementSearchWordFacade

    このクラスは、Google Ads API を使用してキーワードボリュームを検索する機能を提供します。

    継承元: GoogleAdvertisementConfig

    属性
        customer_id (str)： 顧客 ID。
        location_rns (List[str])： ロケーションリソース名のリスト。
        language_rn (str)： 言語リソース名。

    メソッド：
        __init__(customer_id: str, location_ids: List[int], language_id: int) -> なし：
            GoogleAdvertisementSearchWordFacadeオブジェクトを初期化する。

            パラメータ
                customer_id (str)： 顧客ID。
                location_ids (List[int])： ロケーションIDのリスト。
                language_id (int)： 言語ID。

        get_keyword_volume_request(keyword_texts: List[str]) -> List[Dict[str, str]]：
            キーワードボリュームリクエストを取得します。

            パラメータ
                keyword_texts (List[str])： ボリュームを検索するキーワード。

            戻り値
                Any： キーワードボリュームリクエストの結果
    """
    def __init__(self, customer_id: str, location_ids: List[int], language_id: int):
        """
        このクラスの新しいインスタンスを初期化します。

        引数:
        customer_id (str): 顧客ID。Google Adsの顧客IDです。
        location_ids (List[int]): ロケーションのIDのリスト。これはGoogle Adsの地域ターゲティングのIDです。
        language_id (int): 言語ID。これはGoogle Adsの言語ターゲティングのIDです。
        """
        # スーパークラスのコンストラクタを呼び出します。
        super().__init__()

        # 顧客IDを設定します。
        self.customer_id: str = customer_id

        # ロケーションリソース名のリストを設定します。
        # これは、指定されたロケーションIDのリストをリソース名のリストに変換します。
        self.location_rns = self.map_locations_ids_to_resource_names(location_ids)

        # 言語リソース名を設定します。
        # これは、指定された言語IDをリソース名に変換します。
        self.language_rn = self.googleads_client.get_service("GoogleAdsService").language_constant_path(language_id)

    def get_keyword_volume_request(self, keyword_texts: List[str]) -> Any:
        """
        この関数は、指定されたキーワードテキストのリストに対してキーワードボリュームリクエストを生成し、その結果を返します。

        引数:
        keyword_texts (List[str])： キーワードボリュームデータを取得するためのキーワードテキストのリスト。

        戻り値:
        Any： キーワードボリュームリクエストの結果。
        """
        # GenerateKeywordIdeasRequestの新しいインスタンスを作成します。
        request = self.googleads_client.get_type("GenerateKeywordIdeasRequest")

        # リクエストに顧客IDを設定します。
        request.customer_id = self.customer_id

        # リクエストに言語リソース名を設定します。
        request.language = self.language_rn

        # リクエストにロケーションリソース名のリストを設定します。
        request.geo_target_constants.extend(self.location_rns)

        # 大人向けのキーワードを含めないように設定します。
        request.include_adult_keywords = False

        # リクエストにキーワードプランネットワークを設定します。
        request.keyword_plan_network = self.keyword_plan_network

        # リクエストにキーワードシード（キーワードテキストのリスト）を設定します。
        request.keyword_seed.keywords.extend(keyword_texts)

        # キーワードボリュームリクエストをGoogleAdsServiceに送信し、結果を返します。
        return self.keyword_plan_idea_service.generate_keyword_ideas(request=request)
