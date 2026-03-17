from fastapi import FastAPI, Depends, WebSocketDisconnect, WebSocket
from websocket_manager import websocket_manager
from contextlib import asynccontextmanager
from database import engine, get_db
from sqlalchemy.orm import Session
import asyncio
import schemas
import models
import parser


models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Start part
    loop = asyncio.get_running_loop()
    observer = parser.start_watcher("./data_lake", loop)
    yield

    # Stop part
    observer.stop()
    observer.join()

app = FastAPI(title="BTC Data Lake API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "Server worked"}


@app.get("/api/btc/history", response_model=list[schemas.BTCPriceResponse])
def get_btc_history(limit: int=100, db: Session = Depends(get_db)):
    records = db.query(models.DBBTCPrice)\
                .order_by(models.DBBTCPrice.timestamp.desc())\
                .limit(limit)\
                .all()
    return records

@app.websocket("/api/btc/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect