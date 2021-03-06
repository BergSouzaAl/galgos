import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import date

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "https://bergalgos.herokuapp.com",
    "https://bergalgos.herokuapp.com:80"
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

@app.get("/corridafull/{race_id}")
def retorna_corridafull(race_id: str):
    r = requests.get("https://greyhoundbet.racingpost.com/card/blocks.sd?race_id="+race_id+"&r_date="+hoje+"&tab=card&blocks=card-header%2Ccard-pager%2Ccard-tabs%2Ccard-title%2Ccard");
    newr = r.json();
    print(newr)
    for galgo in newr['card']['dogs']:
        #print(galgo)
        galgoId = galgo['dogId']
        print(galgoId)
        rg = requests.get("https://greyhoundbet.racingpost.com/dog/blocks.sd?race_id="+race_id+"&r_date="+hoje+"&dog_id="+galgoId+"&blocks=header%2Cdetails")
        #print(rg.json())
        galgo['info'] = (rg.json())
    return newr

@app.get("/corridasfull")
def retorna_corridasfull():
    r = requests.get("https://greyhoundbet.racingpost.com/meeting/blocks.sd?r_date="+hoje+"&view=time&blocks=header%2Clist");
    newr = r.json();
    for pista in newr['list']['items']:
        #print(pista)
        if pista['tvShortName']  != "":
            for corrida in pista['races']:
                #print(corrida)
                c = requests.get("https://greyhoundbet.racingpost.com/card/blocks.sd?race_id="+corrida['raceId']+"&r_date="+hoje+"&tab=card&blocks=card-header%2Ccard-pager%2Ccard-tabs%2Ccard-title%2Ccard");
                newc = c.json();
                for galgo in newc['card']['dogs']:
                    galgoId = galgo['dogId']
                    #print(galgoId)
                    rg = requests.get("https://greyhoundbet.racingpost.com/dog/blocks.sd?race_id="+corrida['raceId']+"&r_date="+hoje+"&dog_id="+galgoId+"&blocks=header%2Cdetails")
                    galgo['info'] = (rg.json())
                corrida['infoC'] = newc
    return newr

    