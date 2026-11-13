# ApexLiqRadar MCP Server

Real-time multi-chain Aave V3 & DeFi liquidation telemetry, oracle health-factor proximity, and pre-simulated `0x00a718a9` execution calldata across **10 EVM networks** with native **HTTP 402 (`x402` Base USDC)** micropayments.

- **Homepage:** https://apexliqradar.com
- **Agent & LLM Spec:** https://apexliqradar.com
- **x402 Payment Manifest:** https://apexliqradar.com
- **MCP Manifest:** https://apexliqradar.com/.well-known/mcp.json
- **A2A Agent Card:** https://apexliqradar.com

## Quickstart
```json
{
  "mcpServers": {
    "apexliqradar": {
      "command": "uvx",
      "args": ["apexliqradar-mcp"],
      "env": {
        "APEXLIQRADAR_X402_PAYMENT": ""
      }
    }
  }
}
```
Streamable HTTP Endpoint: `https://apexliqradar.com`
