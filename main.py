from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import ast
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", name="home", include_in_schema=False, response_class=HTMLResponse)
@app.get("/posts", name="posts", include_in_schema=False, response_class=HTMLResponse)
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
async def api_get_post(post_id: int):
    """Return a single post as JSON. Keeps API routes consistent under /api."""
    posts = await get_posts()
    for post in posts:
        if post.get("id") == post_id:
            return JSONResponse(status_code=status.HTTP_200_OK, content=post)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/posts/{post_id}", name="post_detail", include_in_schema=False, response_class=HTMLResponse)
async def get_post(post_id: int, request: Request):
    posts = await get_posts()
    for post in posts:
        if post["id"] == post_id:
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post}
            )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):

    detail = exc.detail if exc.detail else "An unexpected error occurred"

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": detail},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {"status_code": exc.status_code, "detail": detail},
        status_code=exc.status_code
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {"status_code": status.HTTP_422_UNPROCESSABLE_ENTITY, "detail": "Invalid request data"},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )