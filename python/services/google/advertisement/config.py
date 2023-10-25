import os
from google.ads.googleads.client import GoogleAdsClient
from typing import List, Optional

class GoogleAdvertisementConfig:
    """
    GoogleAdvertisementConfig

    Google 広告の設定を表すクラス。

    属性：
        googleads_client (GoogleAdsClient)： GoogleAdsClient のインスタンスを初期化したもの。
        keyword_plan_idea_service (GoogleAdsService)： KeywordPlanIdeaService のインスタンス。
        keyword_plan_network (KeywordPlanNetworkEnum)： キーワードプランのネットワーク。
        keyword_competition_level_enum (KeywordPlanCompetitionLevelEnum): キーワードプランのコンペティションレベル： KeywordPlanCompetitionLevelEnum インスタンス。

    メソッド：
        map_locations_ids_to_resource_names(location_ids: List[int]) -> List[Optional]：
            ロケーションIDのリストをリソース名に変換する。

    """
    def __init__(self):
        credentials = {
            "developer_token": os.environ["GOOGLE_AD_API_DEVELOPER_TOKEN"],
            "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
            "client_id": os.environ["GOOGLE_OAUTH2_KEY"],
            "client_secret": os.environ["GOOGLE_OAUTH2_SECRET"],
            "use_proto_plus": False
        }
        self.googleads_client = GoogleAdsClient.load_from_dict(credentials, version="v15")
        self.keyword_plan_idea_service = self.googleads_client.get_service("KeywordPlanIdeaService")
        self.keyword_plan_network = (
            self.googleads_client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
        )
        self.keyword_competition_level_enum = self.googleads_client.get_type(
            "KeywordPlanCompetitionLevelEnum"
        ).KeywordPlanCompetitionLevel


    def map_locations_ids_to_resource_names(self, location_ids: List[int]) -> List[str]:
        """
        ロケーションIDのリストをリソース名に変換する。
        引数
            client (GoogleAdsClient): 初期化済みの GoogleAdsClient のインスタンス。
            location_ids (List[int]): ロケーション ID 文字列のリスト。

        戻り値
            リソース名の文字列のリスト。
        """
        build_resource_name = self.googleads_client.get_service(
            "GeoTargetConstantService"
        ).geo_target_constant_path
        return [build_resource_name(location_id) for location_id in location_ids]
