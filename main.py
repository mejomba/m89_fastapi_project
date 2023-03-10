import uvicorn
from fastapi import Request, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database_manager import engine
from models import auth, posts
from routers import post_amin
auth.BASE.metadata.create_all(bind=engine)
posts.BASE.metadata.create_all(bind=engine)

template = Jinja2Templates('templates')

app = FastAPI()
app.mount("/statics", StaticFiles(directory="statics"), name="statics")






@app.get('/about')
def test(request: Request):
    context = {'request': request, 'data': 'any data in python'}
    return template.TemplateResponse('about.html', context=context)


if __name__ == "__main__":
    uvicorn.run(f'{__name__}:app', reload=True)
