from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import ast
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", name="home", response_class=HTMLResponse)
@app.get("/posts", name="posts", response_class=HTMLResponse)
async def home(request: Request):
    posts = await get_posts()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts}
    )

@app.get("/api/posts")
async def get_posts():
    data_path = Path(__file__).with_name("snippets.txt")
    with data_path.open("r", encoding="utf-8") as file:
        return ast.literal_eval(file.read())


@app.get("/api/posts/{post_id}")
async def get_post(post_id: int):
    posts = await get_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return {"error": "post not found!"}