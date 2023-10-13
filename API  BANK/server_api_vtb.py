from fastapi import FastAPI
from pydantic import BaseModel
from config import bankomat, offcie

app = FastAPI()


@app.get("/get_atm")
async def process_data():
    return bankomat

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)