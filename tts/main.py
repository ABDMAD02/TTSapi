from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, JSONResponse
import edge_tts
import uuid
import os

app = FastAPI(title="Multilingual Edge TTS API")

OUTPUT_DIR = "audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICE_MAP = {
    "kk": "kk-KZ-AigulNeural",      # Казахский
    "ru": "ru-RU-DmitryNeural",     # Русский
    "en": "en-US-AriaNeural",       # Английский
}


async def synthesize_speech(text: str, voice: str) -> str:
    file_name = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(OUTPUT_DIR, file_name)

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

    return output_path


@app.post("/api/tts")
async def tts_post(
    body: dict = Body(
        ...,
        example={
            "text": "Сәлем, қалайсың?",
            "lang": "kk"  
        }
    )
):
    try:
        text = body.get("text")
        lang = body.get("lang", "ru")

        if not text:
            return JSONResponse(status_code=400, content={"error": "Поле 'text' обязательно"})

        voice = VOICE_MAP.get(lang, VOICE_MAP["ru"])

        file_path = await synthesize_speech(text, voice)
        return FileResponse(file_path, media_type="audio/mpeg", filename=os.path.basename(file_path))

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


