from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from model import predict_class
from utils import *

app = FastAPI()

app.mount("/static", StaticFiles(directory='static'), name='static')

template = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    url_path_css = request.url_for('static', path = 'style.css')
    context = {'request': request, 'url_path_css': url_path_css}
    return template.TemplateResponse('index.html', context=context)


@app.post("/")
async def post_init(request: Request):

    response = await request.json()
    result = response['result']
    
    # Training Data
    frame, cat = get_frame('data_init.json')
    
    nb = fit_model(frame)
    
    predict = predict_naive_bayes(
        text=result,
        model=nb
    )
    assert predict.get('index'), "No prediction"

    predict.get('index')
    index = predict.get('index')
    # Speach Result
    word_talk = cat.categories[index]
    # print(cat.categories[index], index)
    talk(word_talk)
    # print(index, {"index":str(index)})

    return {"index":str(index)}
    

    
@app.post("/products")
async def post_products(request: Request):
    response = await request.json()

    result = response['result']
    out = predict_class(result)

    # out = {'quantity': '1', 'container': 'caj.', 'name_product': 'Pilsen Lt. x12 vidrio', 'price': '78.5', 'amount': '78.5'}
    
    return out 