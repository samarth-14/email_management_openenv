import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from environment import EmailEnvironment

app = FastAPI(title="Email Management OpenEnv")

env_instance: Optional[EmailEnvironment] = None
current_task_type: str = "easy"

class ResetRequest(BaseModel):
    task_type: Optional[str] = "easy"

class ResetResponse(BaseModel):
    observation: Dict[str, Any]
    info: Dict[str, Any] = {}

class StepRequest(BaseModel):
    action: Dict[str, Any]

class StepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any] = {}

@app.get("/")
async def root():
    return {"status": "running", "environment": "Email Management OpenEnv", "version": "1.0.0"}

@app.post("/reset", response_model=ResetResponse)
async def reset(request: ResetRequest = ResetRequest()):
    global env_instance, current_task_type
    try:
        env_instance = EmailEnvironment()
        current_task_type = request.task_type or "easy"
        state = env_instance.reset(task_type=current_task_type)
        return ResetResponse(observation=state, info={"task_type": current_task_type})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.post("/step", response_model=StepResponse)
async def step(request: StepRequest):
    global env_instance
    if env_instance is None:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    try:
        new_state, reward, done = env_instance.step(request.action)
        return StepResponse(observation=new_state, reward=reward, done=done, info={})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")

@app.get("/state")
async def get_state():
    global env_instance
    if env_instance is None:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    return {"state": env_instance.state()}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860, log_level="info")

if __name__ == "__main__":
    main()