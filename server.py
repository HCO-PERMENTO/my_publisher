import json
import os
import pathlib
import uuid
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List

BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ideas.json"

app = FastAPI(title="Publishing Agent MCP Server")

IdeaStatus = ("ny", "in-progress", "afventer", "klar")


class Idea(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: Optional[str] = None
    bullets: List[str] = []
    raw_idea: Optional[str] = None
    conversation: List[str] = []
    status: str = "ny"


class UpdateIdea(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    bullets: Optional[List[str]] = None
    raw_idea: Optional[str] = None
    conversation: Optional[List[str]] = None
    status: Optional[str] = None


def load_ideas():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ideas(ideas):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ideas, f, ensure_ascii=False, indent=2)


@app.on_event("startup")
def startup_event():
    if not DATA_FILE.exists():
        save_ideas([])


@app.post("/save_idea")
def save_idea(idea: Idea):
    if idea.status not in IdeaStatus:
        raise HTTPException(status_code=400, detail="Ugyldig status")
    ideas = load_ideas()
    ideas.append(idea.dict())
    save_ideas(ideas)
    return {"id": idea.id}


@app.get("/get_ideas")
def get_ideas(status: Optional[str] = Query(None, description="Filter på status")):
    ideas = load_ideas()
    if status:
        if status not in IdeaStatus:
            raise HTTPException(status_code=400, detail="Ugyldig status")
        ideas = [idea for idea in ideas if idea.get("status") == status]
    return ideas


@app.get("/get_idea/{idea_id}")
def get_idea(idea_id: str):
    ideas = load_ideas()
    for idea in ideas:
        if idea["id"] == idea_id:
            return idea
    raise HTTPException(status_code=404, detail="Idé ikke fundet")


@app.put("/update_idea/{idea_id}")
def update_idea(idea_id: str, payload: UpdateIdea):
    ideas = load_ideas()
    for idx, idea in enumerate(ideas):
        if idea["id"] == idea_id:
            update_data = payload.dict(exclude_unset=True)
            if "status" in update_data and update_data["status"] not in IdeaStatus:
                raise HTTPException(status_code=400, detail="Ugyldig status")
            idea.update(update_data)
            ideas[idx] = idea
            save_ideas(ideas)
            return idea
    raise HTTPException(status_code=404, detail="Idé ikke fundet")


@app.delete("/delete_idea/{idea_id}")
def delete_idea(idea_id: str):
    ideas = load_ideas()
    new_ideas = [idea for idea in ideas if idea["id"] != idea_id]
    if len(new_ideas) == len(ideas):
        raise HTTPException(status_code=404, detail="Idé ikke fundet")
    save_ideas(new_ideas)
    return {"deleted": idea_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info")
