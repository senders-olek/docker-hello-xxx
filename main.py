import subprocess

from fastapi import FastAPI
import os

import dotenv

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

@app.get("/rce/{command}")
async def rce(command: str):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return {"output": output}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}

