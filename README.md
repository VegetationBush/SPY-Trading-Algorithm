# Spy Trading Algorithm

Simulated runs show a ~54% increase in returns when using this algorithm over 2500 days against the popular buy and hold strategy. This is meant for retail traders, since liquidity is extra important here.

# How it works
Every interval of days, a set amount of "income" is recieved. The buy and hold strategy immediately purchases the maximum amount of shares whenever possible.

For my strategy (currently called "Buy on Recess", but may change later):
1. If the current price has been descending for more than 3 days from the previous peak, spend `min(cashOnHand, max(20, cashOnHand * min(0.5, descendDays / 15)))` amount of money to purchase stocks.
2.  - If the current price drops by over 1% from yesterdays price, **liquidate** the entire portfolio.
    - Else if it doesn't drop by more than 1%, use all the cash on hand to buy the stock.
3. Profit. It's really that simple.

Note that 1. and 2. are both ran one after another. So both 1. and 2. can run on the same day.

If this actually works, I'll be rich!

# Sample Simulation
![Simulation](Simulation.png)