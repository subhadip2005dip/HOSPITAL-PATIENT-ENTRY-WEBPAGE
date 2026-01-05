from fastapi import FastAPI
from pydantic import BaseModel


app=FastAPI()

@app.get("/")
def read_root():
  return{"hellow":"world"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
 return {"item_id":item_id}


class items(BaseModel):
  name: str
  price: int
  password:str= 'dont show'


class ItemResponse(BaseModel):
     name:str
     price:int


@app.post("/items/", response_model=ItemResponse)

def create_items(items:items):
  print(items)
  return items
          
   
