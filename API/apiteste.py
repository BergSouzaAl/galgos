import requests
#from bs4 import BeautifulSoup

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import date

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hoje = str(date.today())

@app.get("/corridas")
def retorna_corridas():
    r = requests.get("https://greyhoundbet.racingpost.com/meeting/blocks.sd?r_date="+hoje+"&view=time&blocks=header%2Clist");
    return r.json();

@app.get("/corrida/{race_id}")
def retorna_corrida(race_id: str):
    r = requests.get("https://greyhoundbet.racingpost.com/card/blocks.sd?race_id="+race_id+"&r_date="+hoje+"&tab=card&blocks=card-header%2Ccard-pager%2Ccard-tabs%2Ccard-title%2Ccard");
    return r.json();

@app.get("/galgo/{race_id}/{galgo_id}")
def retorna_galgo(race_id: str, galgo_id: str):
    r = requests.get("https://greyhoundbet.racingpost.com/dog/blocks.sd?race_id="+race_id+"&r_date="+hoje+"&dog_id="+galgo_id+"&blocks=header%2Cdetails")
    return r.json();
