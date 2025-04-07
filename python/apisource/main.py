import ffmpeg
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import io
import tempfile
from pathlib import Path
import zipfile

app = FastAPI()

# 音声トラックを最大5個まで分離し、ZIPにまとめて返す
@app.post("/extract_audio")
async def extract_audio(file: UploadFile = File(...)):
    # ファイルをメモリ上に保持
    video_content = await file.read()

    # 一時的なファイルに動画データを保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video_file:
        tmp_video_file.write(video_content)
        tmp_video_file.close()

        # 音声ファイルを保存するディレクトリを作成
        audio_dir = Path(tmp_video_file.name + "_audio")
        audio_dir.mkdir(parents=True, exist_ok=True)

        # 音声トラックの情報を取得
        try:
            probe = ffmpeg.probe(tmp_video_file.name, v='error', select_streams='a', show_entries='stream=index')
            audio_tracks = [stream['index'] for stream in probe['streams']]
        except ffmpeg.Error as e:
            return {"error": "動画から音声トラックを取得できませんでした。"}

        # 音声トラックを分離
        audio_files = []
        for i, track_index in enumerate(audio_tracks, start=1):
            audio_output = audio_dir / f"audio_{i}.m4a"
            try:
                print(f"音声トラック {i} を処理中")
                ffmpeg.input(tmp_video_file.name) \
                    .output(str(audio_output), acodec='aac', audio_bitrate='192k', map=f"0:{track_index}") \
                    .run()

                audio_files.append(audio_output)
            except ffmpeg.Error as e:
                print(f"トラック {i} は存在しません。エラー: {e}")

        # 音声ファイルをZIPにまとめる
        zip_filename = str(tmp_video_file.name) + "_audio_files.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for audio_file in audio_files:
                zipf.write(audio_file, audio_file.name)

        # 作成したZIPファイルをクライアントに返す
        with open(zip_filename, "rb") as f:
            zip_content = f.read()
            return StreamingResponse(io.BytesIO(zip_content), media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={zip_filename}"})
