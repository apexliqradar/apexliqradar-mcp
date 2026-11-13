"""Thin MCP stdio-to-HTTP bridge for https://apexliqradar.com with x402 payment header passthrough."""

import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

API_URL = os.getenv("APEXLIQRADAR_MCP_URL", "https://apexliqradar.com")
X402_PAYMENT_HEADER = os.getenv("APEXLIQRADAR_X402_PAYMENT", "")

mcp = FastMCP("apexliqradar-mcp")


def _forward_rpc(method: str, params: dict[str, Any]) -> dict[str, Any]:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if X402_PAYMENT_HEADER:
        headers["X-PAYMENT"] = X402_PAYMENT_HEADER

    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    with httpx.Client(timeout=20.0) as client:
        resp = client.post(API_URL, json=payload, headers=headers)
        if resp.status_code == 402:
            return {
                "status": "payment_required",
                "code": 402,
                "message": "HTTP 402 Payment Required via Base USDC (x402). Set APEXLIQRADAR_X402_PAYMENT or see https://apexliqradar.com",
                "x402_headers": dict(resp.headers),
            }
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
def get_live_targets(chain: str = "all", max_hf: float = 1.015, min_bounty_usd: float = 5.0) -> dict[str, Any]:
    """Fetch unmasked Aave V3 borrowers approaching or crossing HF < 1.0000 across EVM chains ($0.01 USDC via x402)."""
    return _forward_rpc(
        "tools/call",
        {
            "name": "get_live_targets",
            "arguments": {"chain": chain, "max_hf": max_hf, "min_bounty_usd": min_bounty_usd},
        },
    )


@mcp.tool()
def get_simulated_calldata(chain: str, borrower: str) -> dict[str, Any]:
    """Return pre-simulated 0x00a718a9 liquidation calldata, flash-loan route, and verified net profit floor ($0.05 USDC via x402)."""
    return _forward_rpc(
        "tools/call",
        {
            "name": "get_simulated_calldata",
            "arguments": {"chain": chain, "borrower": borrower},
        },
    )


@mcp.tool()
def get_chain_health() -> dict[str, Any]:
    """Return live multi-chain telemetry latency, active route counts, and latest verified catch proof hashes ($0.00 free)."""
    return _forward_rpc("tools/call", {"name": "get_chain_health", "arguments": {}})


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
