import uvicorn
from fastapi import Request, APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

template = Jinja2Templates('templates')

app = APIRouter()
app.mount("/statics", StaticFiles(directory="statics"), name="statics")


@app.get('/login')
def test(request: Request):
    context = {'request': request, 'data': 'any data in python'}
    return template.TemplateResponse('home.html', context=context)


if __name__ == "__main__":
    uvicorn.run(f'{__name__}:app', reload=True)
