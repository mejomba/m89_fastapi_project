import uvicorn
from fastapi import Request, FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import jwt_manager
from database_manager import engine
from routers import auth, posts
import models.auth, models.posts
import jinja_custome_filter

models.auth.BASE.metadata.create_all(bind=engine)
models.posts.BASE.metadata.create_all(bind=engine)

template = Jinja2Templates(directory='templates')

app = FastAPI()
app.mount("/statics", StaticFiles(directory="statics"), name="statics")

app.include_router(posts.router)
app.include_router(auth.router)


@app.get('/about')
def about(request: Request, current_user: models.auth.User = Depends(jwt_manager.get_current_user)):
    context = {'request': request, 'user': current_user}
    return template.TemplateResponse('about.html', context=context)


@app.get('/contact_us')
def contact_us(request: Request, current_user: models.auth.User = Depends(jwt_manager.get_current_user)):
    context = {'request': request, 'user': current_user}
    return template.TemplateResponse('contact_us.html', context=context)


if __name__ == "__main__":
    print(__name__)
    uvicorn.run(f'{__name__}:app', reload=True, port=8001)
