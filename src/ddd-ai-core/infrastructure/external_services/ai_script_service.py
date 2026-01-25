import json
import os
import uuid

from google import genai
from google.genai import types


class AiScriptService(AiScriptInterface):
    def __init__(self):
        # google-genai SDKを使用
        project_id = os.getenv("GCP_PROJECT_ID")
        self.client = genai.Client(vertexai=True, project=project_id, location="us-central1")
        self.model_id = os.getenv("AI_SCRIPT_MODEL_ID", "gemini-2.5-flash")

    def generate_script(self, domain1: domain1, domain2: domain2) -> domain3:
        """
        プロンプト設定を使用してスクリプトを生成
        Google検索ツールを使用するため、JSONモードは使用しない

        Args:
            domain1: domain情報
            domain2: プロンプト設定（domain2ドメインモデル）

        Returns:
            domain3: 生成された生スクリプト
        """
        # プロンプトテンプレートにdomain情報を埋め込む
        filled_domain2: str = (
            domain2.domain2_template.replace("{{title}}", domain1.title)
            .replace("{{domain1.url}}", domain1.url)
            .replace("{{buz_reason}}", domain1.buz_reason)
        )

        # グラウンディング（Google検索）のツール設定
        google_search_tool = types.Tool(google_search=types.GoogleSearch())

        # 実行(検索 + テキスト生成)
        # グラウンディングとJSON出力は共存できないため、生データを出力
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=filled_domain2,
            config=types.GenerateContentConfig(
                tools=[google_search_tool],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
                temperature=domain2.temperature,
                max_output_tokens=domain2.max_output_tokens,
            ),
        )

        generated_text = response.text

        return domain3(
            domain1_id=domain1.domain1_id,
            ingested_at=domain1.ingested_at,
            title=domain1.title,
            script_body=generated_text,
        )

    def parse_script_to_ssml(self, domain3: domain3, domain2: domain2) -> domain4:
        """生データをSSMLへパースする

        Args:
            domain2 (domain2): プロンプト設定（domain2ドメインモデル）
            domain3 (domain3): 生成されたスクリプトデータ

        Returns:
            domain3: JSONにパースされたスクリプトデータ
        """
        # プロンプトテンプレートにスクリプト情報を埋め込む
        filled_domain2: str = domain2.domain2_template.replace("{{domain3.domain3_body}}", domain3.domain3_body)

        # 実行
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=filled_domain2,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {"full_script": {"type": "STRING"}},
                    "required": ["full_script"],
                },
                temperature=domain2.temperature,
                max_output_tokens=domain2.max_output_tokens,
            ),
        )

        try:
            res_json = response.parsed if hasattr(response, "parsed") and response.parsed else json.loads(response.text)
        except Exception as e:
            print(
                f"Parse error occurred. Raw response text: {response.text}, response_reason: {response.candidates[0].finish_reason}"
            )
            raise e

        return domain4(
            ssml_generate_id=str(uuid.uuid4()),
            domain1_id=domain3.domain1_id,
            ingested_at=domain3.ingested_at,
            ssml_generated_text=res_json.get("full_script", domain3.script_body),
            audio_file_name=None,
            audio_file_url=None,
            generated_at=None,
        )
