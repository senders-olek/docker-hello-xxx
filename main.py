import subprocess

from fastapi import FastAPI, HTTPException
import os

import dotenv
from pydantic import BaseModel

dotenv.load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/test-env-injection")
async def test_env_injection():

    return {"message": f"env is {os.getenv('SAMPLE_ENV', None)}"}

class Command(BaseModel):
    command: str

@app.post("/rce")
async def rce(cmd: Command):
    try:
        output = subprocess.check_output(cmd.command, shell=True, text=True)
        print(cmd.command)
        return {"output": output}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

