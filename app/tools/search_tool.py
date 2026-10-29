#Since Tavily le Dine Result ma "query" , "follow_up_question" jasta data huncha
#so yo LLM lai dida badi Token khancha so afnai tool banaune short response pathauna

from langchain_tavily import TavilySearch
from langchain.tools import tool


from app.core.config import setting

@tool
def tavily_search_tool(user_query : str) -> dict:
  """Search the web using Tavily to retrieve relevant and up-to-date information based on the user's query."""
  websearch = TavilySearch(
    max_results=1,
    topic="general",
    api_key=setting.TAVILY_API_KEY
  )
  
  tavily_result = websearch.invoke(input={
    "query" : user_query
  })
  
  final_result = tavily_result["results"][0]
  
  extracted_result = {
    "source_url" : final_result.get("url",""),
    "title" : final_result.get("title",""),
    "content" : final_result.get("content","")
  }
  
  return extracted_result
  