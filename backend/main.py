from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from transcripts import get_transcript
from agent import run_chain

load_dotenv()

app = FastAPI()

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    video_id: str
    question: str

@app.post("/ask")
async def ask_question(request: AskRequest):
    video_id = request.video_id
    question = request.question

    transcript_text = ""
    tries=0
    while not transcript_text and tries < 10:
        try:
            # Attempt to get the transcript
            transcript_text = get_transcript(video_id)
            if(transcript_text):
                break
        except Exception as e:
            print(f"Attempt {tries + 1}: Failed to retrieve transcript for video {video_id}. Retrying...")
            tries += 1

    if not transcript_text:
        return {"answer": "Transcript not found for this video."}

    answer = run_chain(transcript_text, question)
    return {"answer": answer}
