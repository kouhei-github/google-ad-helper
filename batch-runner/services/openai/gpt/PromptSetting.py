

class PromptSetting:
    @staticmethod
    def create_template_prompt(keyword: str) -> str:
        prompt = """
        あなたはマークダウン記法でサイトを記述するプロフェッショナルです。
        """

        prompt += f'{keyword}について記事を書いてください。'

        prompt += """
        その際下記を厳守して記事を書いてください。
        必ず下記を厳守してください。
        ・タイトルの直後に目次を記載すること
        ・文字数は4000文字以上にすること
        ・SEOを意識すること
        ・マークダウン形式で記述すること
        ・読みやすい、見やすい記述にすること
        ・zenn.devのマークダウン記法に合わせた見やすい記事にしてください
        """

        return prompt

    @staticmethod
    def create_markdown_prompt(keyword: str) -> str:
        prompt = """
        英語と日本語の相互の変換が得意です。
        """

        prompt += f'下記英語の記事を日本語に変換してください。'

        prompt += """
        その際下記を厳守して記事を書いてください。
        1. マークダウンのコードブロック内のプログラミン言語を判別して、記載すること。
        (例):
        ```python
        print("test")
        ```
        2. 日本語に翻訳した際、話し言葉でわかりやすい日本語で翻訳してください。

        3. 記事の内容を翻訳するだけで、あなたの言葉を入れないでください。(翻訳するだけに集中してください)
        以上を参考に下記を変換してください。

        """

        prompt += keyword

        return prompt
