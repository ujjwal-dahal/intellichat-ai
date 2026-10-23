import os 
from dotenv import load_dotenv
load_dotenv()



class Setting():
  MODEL_API_KEY = os.getenv("MODEL_API_KEY")
  MODEL_NAME  = os.getenv("MODEL_NAME")
  MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
  

setting = Setting()