import httpx
from   fastmcp import FastMCP
from   fastmcp.server.openapi import RouteMap, MCPType
import json
import sys
from   dotenv import load_dotenv
import logging
import os

# load .env file for credentials and IP address
load_dotenv()

# set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Hyperfabric_MCP")

# Define the path to your local spec file.
spec_file_path = r'C:\OPENAPI_MCP\hf_spec_modified.json'

try:
    with open(spec_file_path, 'r') as f:
        openapi_spec = json.load(f)
    
    logger.info("✅ OpenAPI spec loaded successfully!")
    if 'info' in openapi_spec and 'title' in openapi_spec['info']:
        logger.info(f"   Title: {openapi_spec['info']['title']}")
        logger.info(f"   Version: {openapi_spec['info']['version']}")

except FileNotFoundError:
    logger.error(f"ERROR: The file was not found at '{spec_file_path}'")
    sys.exit(1)

except json.JSONDecodeError:
    logger.error(f"ERROR: The file at '{spec_file_path}' is not valid JSON.")
    sys.exit(1)
    
except Exception as e:
    logger.error(f"{e}")
    sys.exit(1)

# Create an HTTP client for your API
token  = os.getenv("HYPERFABRIC_API_TOKEN")
if not token:
    logger.error("ERROR: HYPERFABRIC_API_TOKEN not found in environment variables.")
    sys.exit(1) 

logger.info(f"Using token: {token[:4]}...{token[-4:]}")  # Log only the first and last 4 characters for security

client = httpx.AsyncClient(base_url="https://hyperfabric.cisco.com",
                           headers={"Authorization": "Bearer " + token,
                                    "Content-Type": "application/json",
                                    "Accept": "application/json"})

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="Hyperfabric_MCP_API_Server",
    )

if __name__ == "__main__":
    mcp.run()
