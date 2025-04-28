from fastmcp.server import FastMCP
import plivo
import os

# Your Plivo credentials
PLIVO_AUTH_ID = os.environ.get("PLIVO_AUTH_ID","")
PLIVO_AUTH_TOKEN = os.environ.get("PLIVO_AUTH_TOKEN","")

MY_NUMBER = os.environ.get("MY_NUMBER","")

# Create Plivo client
client = plivo.RestClient(auth_id=PLIVO_AUTH_ID, auth_token=PLIVO_AUTH_TOKEN)

# Create MCP server
mcp = FastMCP("PlivoMCP")

@mcp.tool()
def send_sms(to_number: str, text: str) -> dict:
    """Send an SMS using Plivo's SDK."""
    try:
        response = client.messages.create(
            src=MY_NUMBER,
            dst=to_number,
            text=text
        )
        return {
            "message_uuid": response.message_uuid,
            "api_id": response.api_id
        }
    except plivo.exceptions.PlivoRestError as e:
        return {
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()