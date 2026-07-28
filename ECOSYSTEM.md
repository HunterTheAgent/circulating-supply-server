# circulating-supply-server — Ecosystem Role

**Plane:** Infra · **Verdict:** KEEP (maintenance)
Master plan: [hunter-docs](https://github.com/huntertheagent/hunter-docs/tree/claude/hunter-ecosystem-plan-mda36e)

## Role
Public circulating-supply API for $DRPXBT (required by CoinGecko/CMC listings).

## Change
Only one planned addition: subtract balances held by the new `token` contracts
(HunterTierLock, HunterStaking) and the burn address from circulating supply,
so locked/staked/burned tokens are reported correctly once those contracts are
live on Base.
