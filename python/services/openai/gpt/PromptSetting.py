

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
