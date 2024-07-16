import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
from deep_translator import GoogleTranslator

load_dotenv()  # .env 파일에서 환경변수 로드

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/images/generations"

class ImagePrompt(BaseModel):
    prompt: str

translator = GoogleTranslator(source='ko', target='en')

@app.post("/generate-image")
async def generate_image(prompt_data: ImagePrompt):
    korean_prompt = prompt_data.prompt
    print(f"Received Korean prompt: {korean_prompt}")

    # 한국어를 영어로 번역
    try:
        english_prompt = translator.translate(korean_prompt)
        print(f"Translated English prompt: {english_prompt}")
    except Exception as e:
        print(f"Translation error: {str(e)}")
        english_prompt = korean_prompt  # 번역 실패 시 원본 프롬프트 사용

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    data = {
        "model": "dall-e-3",  # DALL-E 3 모델 지정
        "prompt": english_prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "hd"  # 'standard' 또는 'hd'
    }
    
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        image_url = result['data'][0]['url']
        return {"image_url": image_url}
    except requests.exceptions.RequestException as e:
        print(f"Error response from OpenAI: {str(e)}")
        # OpenAI API 호출 실패 시 더미 URL 반환
        dummy_image_url = f"https://via.placeholder.com/1024x1024.png?text={english_prompt.replace(' ', '+')}"
        return {"image_url": dummy_image_url}

@app.get("/")
async def root():
    return {"message": "Welcome to the DALL-E Image Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
