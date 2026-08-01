from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("Gemini_API_key")

app = FastAPI()

@app.get('/')
def main():
    return api_key


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
