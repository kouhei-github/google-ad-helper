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
        コンストラクタ
        引数
            customer_id (str)： 顧客のID。
            location_ids (List[int])： ロケーションのID。
            language_id (int)： 言語のID。

        """
        super().__init__()
        self.customer_id: str = customer_id
        self.location_rns = self.map_locations_ids_to_resource_names(location_ids)
        self.language_rn = self.googleads_client.get_service("GoogleAdsService").language_constant_path(language_id)


    def get_keyword_volume_request(self, keyword_texts: List[str]) -> Any:
        """
        引数
            keyword_texts (リスト[str])： キーワードテキストのリスト

        戻り値
            Any： キーワードボリュームリクエストの結果

        """
        request = self.googleads_client.get_type("GenerateKeywordIdeasRequest")
        request.customer_id = self.customer_id
        request.language = self.language_rn
        request.geo_target_constants.extend(self.location_rns)
        request.include_adult_keywords = False
        request.keyword_plan_network = self.keyword_plan_network
        request.keyword_seed.keywords.extend(keyword_texts)

        return self.keyword_plan_idea_service.generate_keyword_ideas(request=request)
