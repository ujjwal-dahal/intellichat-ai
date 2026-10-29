import time
from langchain_core.messages import AIMessage

def slow_stream_for_chunks(stream_generator):
  for message_chunk , metadata in stream_generator:
    #tool ko message aauda message_chunk chai ToolMessage and AIMessage both aaucha
    #so AIMessage huda matra pathaune
    if isinstance(message_chunk,AIMessage):
        yield message_chunk.content 
        #write_stream() lai generator chaincha so yield gareko not "return"
        time.sleep(0.07)