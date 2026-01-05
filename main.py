from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Address(BaseModel):
    city: str
    district: str
    state: str
    pincode: int


class PatientDetails(BaseModel):
    id: str
    name: str
    age: int
    address: Address
    contact: int
    email: str


class Patient(BaseModel):
    id: str
    name: str
    age: int
    address: Address
    contact: int
    email: str



def load_data():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)



@app.get("/")
def hello():
    return {"message": "patient management system"}


@app.get("/about")
def about():
    return {"message": "welcome to abc hospital"}


@app.get("/view")
def view_patient():
    return load_data()


@app.get("/patient/{patient_id}")
def find_patient_id(patient_id: str):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient ID not found")


@app.post("/create")
def patient_entry(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=409, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": "Patient successfully created"}
    )
