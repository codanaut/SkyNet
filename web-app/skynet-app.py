from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
import json


from routes import aircraft_by_hex, logged_count, aircraft_by_tail, lookup_aircraft,stats, random_aircraft, test_routes, random_hex
from routes.tools import temp_converter, speed_converter, pressure_converter

app = FastAPI()

app.include_router(aircraft_by_hex.router, prefix="/api/hex", tags=["Aircraft"])
app.include_router(aircraft_by_tail.router, prefix="/api/tailnumber", tags=["Aircraft"])
app.include_router(lookup_aircraft.router, prefix="/api/lookup", tags=["Aircraft"])
app.include_router(logged_count.router, prefix="/api/count", tags=["Stats"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])

app.include_router(random_aircraft.router, prefix="/api/random", tags=["Random Aircraft"])
app.include_router(random_hex.router, prefix="/api/random/hex", tags=["Random Aircraft"])

app.include_router(test_routes.router, prefix="/api/test", tags=["Test Routes"])

# Tools Router to group all tools
tools_router = APIRouter()

tools_router.include_router(temp_converter.router, prefix="/temp")
tools_router.include_router(speed_converter.router, prefix="/speed")
tools_router.include_router(pressure_converter.router, prefix="/pressure")

# Include tools under the /api/tools prefix
app.include_router(tools_router, prefix="/api/tools", tags=["Tools"])


@app.get("/api")
async def root():
    return {"message": "Welcome To SkyNetDB's API","website":"skynetdb.com", "docs":"/docs"}

#Webpages

@app.get('/tools')
async def tools():
    return FileResponse('./webpage/tools.html')

@app.get('/about')
async def about():
    return FileResponse('./webpage/about.html')

@app.get('/testing')
async def about():
    return FileResponse('./webpage/testing.html')
 
app.mount('/',StaticFiles(directory='webpage', html=True), name='static')
# add the mount mount last so that it's not overwriting anything else with being on / 
@app.get('/')
async def index():
    return FileResponse('index.html')
 




# To Run:
# uvicorn app:app --reload --host 0.0.0.0 --port 2222