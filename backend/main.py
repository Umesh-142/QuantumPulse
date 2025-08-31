# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Optional
# import numpy as np
# from quantum_simulator import QuantumSimulator
# import json

# app = FastAPI(title="Quantum Data Generator API", version="1.0.0")

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class RabiParams(BaseModel):
#     omega: float = 1.0  # Drive frequency
#     time_max: float = 10.0
#     time_steps: int = 100
#     noise_rate: float = 0.1
#     shots: int = 1000
#     seed: Optional[int] = None

# class DecayParams(BaseModel):
#     t1: float = 5.0  # T1 decay time
#     t2: float = 3.0  # T2 decay time
#     time_max: float = 15.0
#     time_steps: int = 100
#     noise_rate: float = 0.05
#     shots: int = 1000
#     seed: Optional[int] = None

# class BellParams(BaseModel):
#     noise_rate: float = 0.1
#     shots: int = 10000
#     theta: float = 0.0  # Bell state parameter
#     seed: Optional[int] = None

# simulator = QuantumSimulator()

# @app.get("/")
# async def root():
#     print("http://localhost:8000/")
#     return {"message": "Quantum Data Generator API", "version": "1.0.0"}

# @app.post("/generate/rabi")
# async def generate_rabi(params: RabiParams):
#     try:
#         data = simulator.generate_rabi_data(
#             omega=params.omega,
#             time_max=params.time_max,
#             time_steps=params.time_steps,
#             noise_rate=params.noise_rate,
#             shots=params.shots,
#             seed=params.seed
#         )
#         return {"status": "success", "data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/generate/decay")
# async def generate_decay(params: DecayParams):
#     try:
#         data = simulator.generate_decay_data(
#             t1=params.t1,
#             t2=params.t2,
#             time_max=params.time_max,
#             time_steps=params.time_steps,
#             noise_rate=params.noise_rate,
#             shots=params.shots,
#             seed=params.seed
#         )
#         return {"status": "success", "data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/generate/bell")
# async def generate_bell(params: BellParams):
#     try:
#         data = simulator.generate_bell_data(
#             noise_rate=params.noise_rate,
#             shots=params.shots,
#             theta=params.theta,
#             seed=params.seed
#         )
#         return {"status": "success", "data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from quantum_simulator import QuantumSimulator
import json

app = FastAPI(title="Quantum Data Generator API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RabiParams(BaseModel):
    omega: float = 1.0  # Drive frequency
    time_max: float = 10.0
    time_steps: int = 100
    noise_rate: float = 0.1
    shots: int = 1000
    seed: Optional[int] = None

class DecayParams(BaseModel):
    t1: float = 5.0  # T1 decay time
    t2: float = 3.0  # T2 decay time
    time_max: float = 15.0
    time_steps: int = 100
    noise_rate: float = 0.05
    shots: int = 1000
    seed: Optional[int] = None

class BellParams(BaseModel):
    noise_rate: float = 0.1
    shots: int = 10000
    theta: float = 0.0  # Bell state parameter
    seed: Optional[int] = None

simulator = QuantumSimulator()

@app.get("/")
async def root():
    return {"message": "Quantum Data Generator API", "version": "1.0.0"}

@app.post("/generate/rabi")
async def generate_rabi(params: RabiParams):
    try:
        data = simulator.generate_rabi_data(
            omega=params.omega,
            time_max=params.time_max,
            time_steps=params.time_steps,
            noise_rate=params.noise_rate,
            shots=params.shots,
            seed=params.seed
        )
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/decay")
async def generate_decay(params: DecayParams):
    try:
        data = simulator.generate_decay_data(
            t1=params.t1,
            t2=params.t2,
            time_max=params.time_max,
            time_steps=params.time_steps,
            noise_rate=params.noise_rate,
            shots=params.shots,
            seed=params.seed
        )
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/bell")
async def generate_bell(params: BellParams):
    try:
        data = simulator.generate_bell_data(
            noise_rate=params.noise_rate,
            shots=params.shots,
            theta=params.theta,
            seed=params.seed
        )
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
