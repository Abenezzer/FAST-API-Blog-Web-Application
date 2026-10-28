from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from dummyDB import posts

app = FastAPI()
template = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), "static")



@app.get('/', include_in_schema=False, name="home")
@app.get('/posts', include_in_schema=False, name="posts")
def home(request: Request):
    return template.TemplateResponse(request, "home.html", {"posts":posts})

@app.get('/posts/{post_id}', include_in_schema=FastAPI, name="post_page")
def post_page(request:Request, post_id:int):
    for post in posts:
            if post.get("id") == post_id:
                return template.TemplateResponse(request, "post.html", {"post": post})
    
    return f"post with {post_id} doesn't exist"


# build the api part

@app.get('/api/posts')
def get_posts():
    return posts

@app.get('/api/posts/{post_id}')
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return post

    return f"post with {post_id} doesn't exist"