import asyncio
import streamlit as st
from langchain_core.tools import StructuredTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.servers.config import CONFIG


# MCP server haru ko config. MultiServerMCPClient le "mcpServers" wrapper chahidaina,
# so seedhai server haru ko dict pathaune
MCP_SERVERS = CONFIG["mcpServers"]


# MCP server haru sanga connect garera available tools ko list lyaune async function
async def _list_tools():

    # MultiServerMCPClient le sabai servers sanga connect garcha
    client = MultiServerMCPClient(MCP_SERVERS)

    # Sabai servers ka tools LangChain tool format ma return garcha
    return await client.get_tools()


# MCP ko async tool lai synchronous LangChain tool ma convert garne function
def _make_sync_tool(t):

    # LangChain le tool call garda execute hune synchronous function
    def run(**kwargs):

        # LLM bata aayeko arguments (kwargs) use garera MCP tool execute garne
        # MultiServerMCPClient ko tool le har call ma afnai fresh session kholcha,
        # so "Connection closed" error aaudaina. Yeta feri adapter kholnu pardaina
        # ainvoke() async ho, tesaile asyncio.run() le sync context ma chalaune
        return asyncio.run(t.ainvoke(kwargs))

    # Original MCP tool ko information use garera StructuredTool create garne
    return StructuredTool(
        name=t.name,                      # Tool ko original name preserve garne
        description=t.description or "",  # Tool le k garcha bhanne description rakhne
        args_schema=t.args_schema,        # Tool ko input parameters ko schema preserve garne
        func=run,                         # Sync call ko lagi (graph.stream / ToolNode)
        coroutine=t.coroutine,            # Async call ko lagi pani kam garos bhanera
        response_format=t.response_format,
    )


# Streamlit ma resource cache garne decorator
# App rerun huda harek choti MCP tools fetch garnu pardaina
@st.cache_resource
def get_all_mcp_tools():

    # MCP server bata available sabai tools ko list fetch garne
    # asyncio.run() le async function lai synchronous way ma execute garcha
    mcp_tools = asyncio.run(_list_tools())

    # Fetch bhayeka sabai MCP tools lai synchronous LangChain tools ma convert garne
    return [_make_sync_tool(t) for t in mcp_tools]