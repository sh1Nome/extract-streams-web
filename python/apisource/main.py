import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from urllib.parse import quote

app = FastAPI()

@app.post("/extract-audio")
async def extract_audio(file: UploadFile = File(...)):
    # ファイルをメモリ上で保持
    file_content = await file.read()

    # メモリ上のファイルをそのまま返す
    return StreamingResponse(io.BytesIO(file_content), media_type="video/mp4")
