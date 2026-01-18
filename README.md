# Spy Trading Algorithm

Simulated runs show a ~54% increase in returns when using this algorithm over 2500 days against the popular buy and hold strategy. This is meant for retail traders, since liquidity is extra important here.

# How it works
Every interval of days, a set amount of "income" is recieved. The buy and hold strategy immediately purchases the maximum amount of shares whenever possible.

For my strategy (currently called "Buy on Recess", but may change later):
1. If the current price drops by over 1% from yesterdays price, **liquidate** the entire portfolio.
2. If it doesn't drop by more than 1%, use all the cash on hand to buy the stock.
3. Profit. It's really that simple.

If this actually works, I'll be rich!

And just as a side note.  
I was planning to add LEAP call options into the equation (to capitalize on major market downturns, where calls would be rotated into). However I couldn't find any SPY call option historical data that was accessible and free, so unfortunately I couldn't simulate that rotation.  
I'd guestimate (since it's only speculation), that adding 1+ year dated call options into the equation would increase the diff after 2500 days towards 70-100%. Obviously, I'm estimating. I don't know if that's actually the case since I haven't simulated it.

# Sample Simulation
![TradingSimulation](TradingSimulation.png)