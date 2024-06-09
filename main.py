from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
from text_extraction import extract_text
from processing import classify_text
from rating import score_achievements, generate_rating

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Achievement(BaseModel):
    criterion: str
    score: int

class ResponseModel(BaseModel):
    achievements: list[Achievement]
    rating: str

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_cv(request: Request, cv: UploadFile = File(...)):
    logging.info("Received file: %s", cv.filename)
    try:
        content = await cv.read()
        logging.info("File read successfully")
        logging.info("File content size: %d bytes", len(content))
    except Exception as e:
        logging.error("Error reading file: %s", e)
        return templates.TemplateResponse("index.html", {"request": request, "result": "Error reading file"})
    
    try:
        text = extract_text(content)
        logging.info("Extracted text: %s", text[:200])
    except Exception as e:
        logging.error("Error extracting text: %s", e)
        return templates.TemplateResponse("index.html", {"request": request, "result": "Error extracting text"})

    try:
        classifications = classify_text(text)
        logging.info("Classifications: %s", classifications)
    except Exception as e:
        logging.error("Error processing text: %s", e)
        return templates.TemplateResponse("index.html", {"request": request, "result": "Error processing text"})

    try:
        scores = score_achievements(classifications)
        rating = generate_rating(scores)
        logging.info("Scores: %s", scores)
        logging.info("Rating: %s", rating)
    except Exception as e:
        logging.error("Error scoring achievements: %s", e)
        return templates.TemplateResponse("index.html", {"request": request, "result": "Error scoring achievements"})

    achievements_list = [{"criterion": key, "score": value} for key, value in scores.items()]
    result = {"achievements": achievements_list, "rating": rating}

    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.get("/status")
async def status():
    logging.info("Status check received") # Check if server is running properly
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
