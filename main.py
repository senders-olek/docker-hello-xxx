import subprocess

from fastapi import FastAPI, HTTPException
import os

import dotenv
from pydantic import BaseModel

import base64
from cryptography.fernet import Fernet

dotenv.load_dotenv()

app = FastAPI()


class ObfuscatedSecret:
    def __init__(self, secret):
        key = Fernet.generate_key()
        self.key = key
        f = Fernet(key)
        self.encrypted = f.encrypt(secret.encode())

    def __str__(self):
        return "ObfuscatedSecret"

    def get(self):
        f = Fernet(self.key)
        return f.decrypt(self.encrypted).decode()


SAMPLE_ENV = ObfuscatedSecret(os.getenv('SAMPLE_ENV', None))
del os.environ['SAMPLE_ENV']


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/test-env-injection")
async def test_env_injection():
    return {"message": f"env is {SAMPLE_ENV.get()}"}


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
