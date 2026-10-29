#2. Calculator Tool
from typing import Literal
from langchain.tools import tool


@tool
def calculator_tool(
   action: Literal[
        "addition",
        "subtraction",
        "multiply",
        "divide",
        "remainder",
        "power",
    ],
    a: int,
    b: int,) -> int | float:
  
  """Perform addition, subtraction, multiplication, division, remainder, or power calculations on two integers."""
  
  if action == "addition":
    return a + b
  
  if action == "subtraction":
    return a - b 
  
  if action == "multiply":
    return a * b 
  
  if action == "divide":
    if b == 0:
      raise ValueError("Division by Zero is not Allowed")
    
    return a/b
  
  if action == "remainder" : 
    if b == 0:
      raise ValueError("Division by Zero is not Allowed")
    
    return a%b
  
  if action == "power":
    return a ** b 