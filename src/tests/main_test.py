import sys
import os
import logging
from dotenv import load_dotenv

# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append("/Users/eduardfer/Desktop/TFG TELEMÀTICA/eGym-server/src")
sys.path.append("/Users/eduardfer/Desktop/TFG TELEMÀTICA/eGym-server")

load_dotenv(".env.dev")

from fastapi.testclient import TestClient
from main.main import app

client = TestClient(app)
