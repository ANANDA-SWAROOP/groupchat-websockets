
from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


app = FastAPI()

class ConnectionManager:
  def __init__(self):
    self.active_connections : list[WebSocket] = []
    
  async def connect(self,websocket:WebSocket):
    await websocket.accept()
    self.active_connections.append(websocket)
    
  def disconnect(self,websocket):
    self.active_connections.remove(websocket)
  
  async def send_personnel_message(self,message:str,websocket:WebSocket):
    await websocket.send_text(message)
  
  async def broadcast(self,message:str):
    for connection in self.active_connections:
      await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
  return {"dude":"fucked up"}

@app.websocket("/ws/{client_id}")
async def websocket(websocket:WebSocket,client_id:int):
    # await websocket.accept()
    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(f"{data}")
    await manager.connect(websocket)
    try:
      while True:
        data = await websocket.receive_text()
        await manager.send_personnel_message(f"YOU: {data}",websocket)
        await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
      manager.disconnect(websocket)
      await manager.broadcast(f"client #{client_id} has left the chat")