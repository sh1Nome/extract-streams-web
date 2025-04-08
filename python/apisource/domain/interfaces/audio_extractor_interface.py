from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class IAudioExtractor(ABC):
    @abstractmethod
    def get_audio_tracks(self, video_path: str) -> List[int]:
        pass

    @abstractmethod
    def extract_audio(self, video_path: str, output_path: Path, track_index: int) -> None:
        pass
