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
        """
        インスタンスを初期化し、GoogleAdsClientと各サービス、列挙型を作成します。

        初期化時には、環境変数からOAuth2認証情報を取得します。
        """
        # 環境変数から認証情報を取得します。
        credentials = {
            "developer_token": os.environ["GOOGLE_AD_API_DEVELOPER_TOKEN"],
            "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
            "client_id": os.environ["GOOGLE_OAUTH2_KEY"],
            "client_secret": os.environ["GOOGLE_OAUTH2_SECRET"],
            "use_proto_plus": False
        }

        # GoogleAdsClientを作成します。
        # Google Ads APIのバージョンはv15です。
        self.googleads_client = GoogleAdsClient.load_from_dict(credentials, version="v15")

        # KeywordPlanIdeaServiceを使えるように設定します。
        self.keyword_plan_idea_service = self.googleads_client.get_service("KeywordPlanIdeaService")

        # 広告ネットワーク設定を行います。デフォルトでは、Google SearchおよびSearch Partnersに設定します。
        self.keyword_plan_network = (
            self.googleads_client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
        )

        # KeywordPlanCompetitionLevelEnumのインスタンスを取得します。
        self.keyword_competition_level_enum = self.googleads_client.get_type(
            "KeywordPlanCompetitionLevelEnum"
        ).KeywordPlanCompetitionLevel


    def map_locations_ids_to_resource_names(self, location_ids: List[int]) -> List[str]:
        """
        この関数は、GoogleAdsClientを使って指定されたロケーションIDのリストをリソース名のリストに変換します。

        Arguments:
        location_ids (List[int])： Google Ads の地域ターゲティングのIDのリスト。

        Returns:
        List[str]: ロケーションIDそれぞれに対応するリソース名のリスト。
        """
        # GeoTargetConstantServiceをセットアップします。
        # これを使用して、地理的なターゲットの常数を取得します。
        build_resource_name = self.googleads_client.get_service(
            "GeoTargetConstantService"
        ).geo_target_constant_path

        # ロケーション ID のリストをリソース名のリストに変換します。
        return [build_resource_name(location_id) for location_id in location_ids]
