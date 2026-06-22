"""SupportGenie's MCP server: exposes order/inventory/ticket tools.

Backed by mock data for now — swap in a real database later (Phase 8)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("supportgenie-tools")

# --- Mock data (pretend database) ------------------------------------------

ORDERS = {
    "12345": {"status": "shipped", "eta": "2 days", "item": "Wireless Headphones"},
    "67890": {"status": "processing", "eta": "5 days", "item": "Laptop Stand"},
    "11111": {"status": "delivered", "eta": "—", "item": "USB-C Cable"},
}

INVENTORY = {
    "wireless headphones": 42,
    "laptop stand": 0,
    "usb-c cable": 153,
}

_ticket_counter = 1000


# --- Tools -----------------------------------------------------------------

@mcp.tool()
def lookup_order(order_id: str) -> str:
    """Look up the status and details of a customer's order by its ID."""
    order = ORDERS.get(order_id)
    if order is None:
        return f"No order found with ID {order_id}."
    return f"Order {order_id}: {order['item']} — status: {order['status']}, ETA: {order['eta']}."


@mcp.tool()
def check_inventory(product: str) -> str:
    """Check how many units of a product are currently in stock."""
    count = INVENTORY.get(product.lower().strip())
    if count is None:
        return f"Product '{product}' not found in inventory."
    if count == 0:
        return f"'{product}' is currently out of stock."
    return f"'{product}' has {count} units in stock."


@mcp.tool()
def create_ticket(subject: str) -> str:
    """Create a support ticket for an issue that needs human attention."""
    global _ticket_counter
    _ticket_counter += 1
    return f"Ticket #{_ticket_counter} created for: '{subject}'. A human agent will follow up."


if __name__ == "__main__":
    mcp.run(transport="stdio")