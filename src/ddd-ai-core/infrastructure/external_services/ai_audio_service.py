import os

from google.cloud.texttospeech import (
    AudioConfig,
    AudioEncoding,
    SynthesisInput,
    SynthesizeSpeechResponse,
    TextToSpeechClient,
    VoiceSelectionParams,
)


class AiAudioService(AiAudioInterface):

    def __init__(self):
        self.client: TextToSpeechClient = TextToSpeechClient()
        self.model_id: str = os.getenv("AI_TTS_MODEL_ID", "Paul")

    def generate_audio_data(self, domain1: domain1, domain2: domain2) -> bytes:
        """プロンプト設定を使用して高品質な音声ファイルを生成

        Args:
            domain1: プロンプト設定（domain1ドメインモデル）
            domain2: 読み上げるスクリプト(domain2ドメインモデル)
        Returns:
            audio_data: 生成された音声データ
        """
        # 実行
        response: SynthesizeSpeechResponse = self.client.synthesize_speech(
            input=SynthesisInput(text=domain2.domain2_body, domain1=domain1.domain1_template),
            voice=VoiceSelectionParams(
                name="Puck",
                language_code="ja-jp",
                model_name=self.model_id,
            ),
            audio_config=AudioConfig(audio_encoding=AudioEncoding.MP3),
        )

        return response.audio_content
