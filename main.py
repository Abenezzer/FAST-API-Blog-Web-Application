from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from schemas import PersonCreate, PersonResponse

from dummyDB import posts

app = FastAPI()
template = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), "static")


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return template.TemplateResponse(request, "home.html", {"posts": posts})


@app.get("/posts/{post_id}", include_in_schema=False, name="post_page")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return template.TemplateResponse(request, "post.html", {"post": post})

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {post_id} doesn't exist",
    )


# build the api part


@app.get("/api/posts", response_model=list[PersonResponse])
def get_posts():
    return posts


@app.get("/api/posts/{post_id}", response_model=PersonResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {post_id} doesn't exist",
    )
@app.post('/api/posts/create', response_model=PersonResponse)
def create_post(post: PersonCreate):
    return {
        "id": 1,
        "title":post.title,
        "author": post.author,
        "content": post.content,
        "date": "May 12, 2026"
    }

@app.exception_handler(StarletteHttpException)
def general_exception_handler(request: Request, exception: StarletteHttpException):
    message = (
        exception.detail
        if exception.detail
        else "Error Occurs Please check the request and try agin."
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            content={"detail": message}, status_code=exception.status_code
        )

    return template.TemplateResponse(
        request,
        status_code=exception.status_code,
        name="error.html",
        context={"message": message, "status_code": exception.status_code},
    )


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exception: HTTPException):
    message = (
        exception.detail
        if exception.detail
        else "Error Occurs Please check the request and try agin."
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            content={"detail": message}, status_code=exception.status_code
        )

    return template.TemplateResponse(
        request,
        status_code=exception.status_code,
        name="error.html",
        context={"message": message, "status_code": exception.status_code},
    )


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(
    request: Request, exeption: RequestValidationError
):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            content={"detail": "Invalid Request"},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    return template.TemplateResponse(
        request=request,
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        name="error.html",
        context={
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid Request",
        },
    )
