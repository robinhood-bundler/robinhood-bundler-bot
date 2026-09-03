import os
from dataclasses import dataclass

# Network and Protocol Constants for Robinhood Chain
ROBINHOOD_RPC_URL = os.getenv("ROBINHOOD_RPC_URL", "https://rpc.robinhood-chain.mainnet.io")
PUMP_FUN_PROGRAM_ID = "PumpFunRobinhood111111111111111111111111"

HOOD_DECIMALS = 18
WHOOD_ADDRESS = "0xWHOODxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

@dataclass
class BotConfig:
    """Configuration data class for global bot performance settings."""
    rpc_latency_threshold_ms: int = 5
    max_daily_loss_limit_hood: float = 10.0
    default_slippage_bps: int = 100  # 1%
    priority_fee_multiplier: float = 1.2
