import streamlit as st

#postgresql
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

#langchain
from langgraph.checkpoint.postgres import PostgresSaver

#project import
from app.core.config import setting


@st.cache_resource
def get_checkpointer():
  
  #Connections ko pool banaune
  pool = ConnectionPool(
    conninfo=setting.DATABASE_URL,
    min_size=1,
    max_size=5,
    kwargs={
        "autocommit": True,
        "prepare_threshold": 0,
        "row_factory": dict_row,
    },
  )
  
  # Pool ready bhayepachi checkpointer initialize garne
  pool.wait()
  
  checkpointer = PostgresSaver(
    conn=pool
  )
  
  # First setup ma checkpoint tables create/migrate garne
  checkpointer.setup()
  
  return checkpointer


checkpointer = get_checkpointer()

