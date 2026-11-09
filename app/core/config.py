import os 
from dotenv import load_dotenv
load_dotenv()



class Setting():
  MODEL_API_KEY = os.getenv("MODEL_API_KEY")
  MODEL_NAME  = os.getenv("MODEL_NAME")
  MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
  DATABASE_URL = os.getenv("DATABASE_URL")
  TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
  EXPENSE_DATABASE_URL = os.getenv("EXPENSE_DATABASE_URL")
  

setting = Setting()