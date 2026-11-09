# यो code को मुख्य काम Asynchronous MCP Tools लाई Synchronous LangChain Tools (StructuredTool) मा convert गर्नु हो।

# यसको process:
# 1. MCP Server बाट asynchronous tools fetch गर्छ।
# 2. प्रत्येक MCP tool लाई StructuredTool मा wrap गर्छ।
# 3. asyncio.run() प्रयोग गरेर asynchronous MCP execution लाई synchronous interface बाट चलाउँछ।
# 4. Converted tools लाई LangChain Agent मा प्रयोग गर्न मिल्ने बनाउँछ।



import asyncio
import streamlit as st
from langchain.mcp import MCPAdapter
from langchain_core.tools import StructuredTool

from app.servers.config import CONFIG


# MCP server haru sanga connect garera available tools ko list lyaune async function
async def _list_tools():

    # MCPAdapter use garera CONFIG ma define bhayeka MCP servers sanga connection establish garne
    async with MCPAdapter(CONFIG) as adapter:

        # MCP servers ma available sabai tools ko information return garne
        return await adapter.list_tools()


# MCP ko async tool lai synchronous LangChain tool ma convert garne function
def _make_async_to_sync_tool(t):
    # यसको काम MCP tool लाई LangChain को StructuredTool मा convert गर्नु हो।


    # MCP tool ko original name save garne, pachi yehi name bata tool identify garincha
    tool_name = t.name

    # LangChain le tool call garda execute hune synchronous function
    def run(**kwargs):

        # Actual MCP tool call garna async function define gareko
        async def call():

            # Harek tool call huda fresh MCP connection establish garne
            # Yesle previous connection close bhayera aaune "Connection closed" error avoid garna help garcha
            async with MCPAdapter(CONFIG) as adapter:

                # Fresh connection bata available MCP tools feri fetch garne
                tools = await adapter.list_tools()

                # Pahile save gareko tool_name sanga match hune actual MCP tool find garne
                tool = next(x 
                            for x in tools 
                            if x.name == tool_name
                            )

                # LLM bata aayeko arguments (kwargs) use garera selected MCP tool execute garne
                # ainvoke() async method ho, jasle tool ko result return garcha
                return await tool.ainvoke(kwargs)

        # Async function lai synchronous context bata execute garne
        # LangChain ko synchronous StructuredTool interface sanga compatible banaune
        return asyncio.run(call())

    # Original MCP tool ko information use garera StructuredTool create garne
    return StructuredTool(
        name=tool_name,                 # Tool ko original name preserve garne
        description=t.description or "",  # Tool le k garcha bhanne description rakhne
        args_schema=t.args_schema,     # Tool ko input parameters ko schema preserve garne
        func=run,                     
        # Tool call huda execute hune synchronous function
    )


# Streamlit ma resource cache garne decorator
# App rerun huda harek choti MCP tools fetch garnu pardaina
@st.cache_resource
def get_all_mcp_tools():

    # MCP server bata available sabai tools ko list fetch garne
    # asyncio.run() le async function lai synchronous way ma execute garcha
    mcp_tools = asyncio.run(_list_tools())

    # Fetch bhayeka sabai MCP tools lai synchronous LangChain tools ma convert garne
    # List comprehension le each tool ma _make_sync_tool() apply garcha
    return [_make_async_to_sync_tool(t) 
            
            for t in mcp_tools
            ]