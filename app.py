
import motor.motor_asyncio
import pydantic
import datetime
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response
from bson import ObjectId
from httpx import request

app = FastAPI()

class data(BaseModel):
   temp: float
   sunset:str
   fanspeed: bool
   brightness: bool

class info():
   temeperature: Optional[float] = None
   fanspeed: Optional[bool]=None
   sunset:Optional[str]=None
   brightness: Optional[bool]=None


origins = [
    "192.168.0.7"
    "https://ecse-sunset-api.onrender.com"
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client=motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Tombraider77:Iamnotarobot17@cluster0.ylqnn6l.mongodb.net/?retryWrites=true&w=majority")

db = client.labs.lab6

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

app.put("/api/temperature",status_code= 204)
async def temp_data(temp_request: Request):
     
   
    temperature_obj = await temp_request.json()
    temp_find = await db["state"].find_one({"temperature": "tempature_obj"})

    
    new_temp= await db["state"].find_one({"temperature":"temperature_obj"})

   return new_temp

@app.get("/api/state")
async def get_state():

    fanspeed = False
    brightness = False

    temps = await db["temp"].find().to_list(999)
 
    curr_temp = temps[-1]
    curr_time_str = datetime.datetime.now().strftime("%H:%M:%S.%f")
    sunset_str = get_time()

    curr_time = datetime.datetime.strptime(curr_time_str,"%H:%M:%S.%f")
    sunset = datetime.datetime.strptime(sunset_str["sunset"].split("T")[1],"%H:%M:%S.%f")

    if curr_temp["temp"] >= 28.0:
       fanspeed = True

    if curr_time >= sunset:
       brightness = True

    return {"Fan": fanspeed, "Light": brightness}

def get_time():
  timedata=request("GET",sunsetURL+"/api/sunset").json()
  return timedata

