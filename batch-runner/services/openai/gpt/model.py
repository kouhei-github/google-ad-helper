import os
import openai
from services.openai.gpt.PromptSetting import PromptSetting

class GPTModelFacade(PromptSetting):
    """

    クラス GPTModelFacade

    このクラスはGPT-3.5-turbo言語モデルAPIのファサードを提供します。与えられたプロンプトに基づいてレスポンスを生成することができます。

    属性
        api_key (str)： OpenAI APIにアクセスするためのAPIキー。
        prompt_format (str)：プロンプトのフォーマット。

    メソッド
        listen_prompt(prompt: str) -> str：
            与えられたプロンプトに基づいてレスポンスを生成します。

    """
    # 環境変数からOPEN_AI_APIキーを取得
    api_key = os.environ.get("OPEN_AI_API")


    @classmethod
    async def listen_prompt(cls, prompt: str) -> str:
        # OpenAIのキーを設定
        openai.api_key = cls.api_key

        # GPT-3.5-turboモデルを使用して、ChatCompletion APIリクエストを作成します。
        # このリクエストは、指定されたプロンプトに基づく応答を生成します。
        response = openai.ChatCompletion.create(
            model="gpt-4",  # GPTのエンジン名を指定します
            messages=[
                {"role": "user", "content": PromptSetting.create_template_prompt(prompt)},  # ユーザーからのメッセージを指定します
            ],
        )

        # GPT-3.5-turboモデルからの最初の応答を取得し、前後の空白を削除します。
        return response.choices[0]["message"]["content"]

    @classmethod
    async def listen_markdown_prompt(cls, prompt: str) -> str:
        # OpenAIのキーを設定
        openai.api_key = cls.api_key

        # GPT-3.5-turboモデルを使用して、ChatCompletion APIリクエストを作成します。
        # このリクエストは、指定されたプロンプトに基づく応答を生成します。
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # GPTのエンジン名を指定します
            messages=[
                {"role": "user", "content": PromptSetting.create_markdown_prompt(prompt)},  # ユーザーからのメッセージを指定します
            ],
        )

        # GPT-3.5-turboモデルからの最初の応答を取得し、前後の空白を削除します。
        return response.choices[0]["message"]["content"]
