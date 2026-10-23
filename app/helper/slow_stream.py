import time

def slow_stream_for_chunks(stream_generator):
  for message_chunk , metadata in stream_generator:
    if message_chunk.content:
      yield message_chunk.content 
      #write_stream() lai generator chaincha so yield gareko not "return"
      time.sleep(0.07)