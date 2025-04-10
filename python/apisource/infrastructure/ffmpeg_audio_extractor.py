import ffmpeg
from pathlib import Path

from domain.interfaces.audio_extractor_interface import IAudioExtractor
from core.extract_audio_exception import ExtractAudioException

class FFmpegAudioExtractor(IAudioExtractor):
    def get_audio_tracks(self, video_path: str):
        try:
            probe = ffmpeg.probe(video_path, v='error', select_streams='a', show_entries='stream=index')
            return [stream['index'] for stream in probe['streams']]
        except ffmpeg.Error:
            raise ExtractAudioException("audio_track_retrieval_failed")

    def extract_audio(self, video_path: str, output_path: Path, track_index: int):
        try:
            ffmpeg.input(video_path) \
                .output(str(output_path), acodec='aac', audio_bitrate='192k', map=f"0:{track_index}") \
                .run()
        except ffmpeg.Error as e:
            raise ExtractAudioException("audio_extraction_failed", track_index=track_index, error=e)
