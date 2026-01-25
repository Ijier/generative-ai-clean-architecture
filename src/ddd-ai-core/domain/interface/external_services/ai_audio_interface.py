from abc import ABC, abstractmethod


class AiAudioInterface(ABC):
    """AI音声生成サービスのインターフェース
    高品質オーディオ生成を行うためのメソッドを定義します。
    """

    @abstractmethod
    def generate_audio_data(self, domain1: domain1, domain2: domain2) -> bytes:
        """Generate high-quality audio file from domain1 using AI service.

        Args:
            domain1 (domain1): The domain1 settings (domain1 domain model)
        """
        pass
