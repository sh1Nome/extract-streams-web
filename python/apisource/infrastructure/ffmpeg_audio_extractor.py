import ffmpeg
from pathlib import Path

from domain.interfaces.audio_extractor_interface import IAudioExtractor, AudioTrackRetrievalException, AudioExtractionFailedException

class FFmpegAudioExtractor(IAudioExtractor):
    """
    FFmpegを使用して音声トラックを抽出するクラス。

    IAudioExtractorインターフェースを実装します。
    """

    def get_audio_tracks(self, video_path: str):
        """
        ビデオファイルから利用可能な音声トラックを取得します。

        Args:
            video_path (str): 音声トラックを取得するビデオファイルのパス。

        Returns:
            list: 利用可能な音声トラックのインデックスリスト。

        Raises:
            AudioTrackRetrievalException: 音声トラックの取得に失敗した場合。
        """
        try:
            probe = ffmpeg.probe(video_path, v='error', select_streams='a', show_entries='stream=index')
            return [stream['index'] for stream in probe['streams']]
        except ffmpeg.Error:
            raise AudioTrackRetrievalException()

    def extract_audio(self, video_path: str, output_path: Path, track_index: int):
        """
        指定された音声トラックを抽出して保存します。

        Args:
            video_path (str): 音声を抽出するビデオファイルのパス。
            output_path (Path): 抽出した音声を保存するパス。
            track_index (int): 抽出する音声トラックのインデックス。

        Raises:
            AudioExtractionFailedException: 音声抽出に失敗した場合。
        """
        try:
            ffmpeg.input(video_path) \
                .output(str(output_path), acodec='aac', audio_bitrate='192k', map=f"0:{track_index}") \
                .run()
        except ffmpeg.Error as e:
            raise AudioExtractionFailedException()
