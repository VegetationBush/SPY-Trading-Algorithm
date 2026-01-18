'''
Just kidding.
I fixed it.
'''

import matplotlib.pyplot as plt

# loading data
data = []
with open("spy_historical.txt") as f:
    for line in f:
        last_number = line.strip().split(",")[-1]
        data.append(float(last_number))
data.reverse()

xAxis = [i for i in range(len(data))]

# net deposit
INCOME = 10
INCOME_PERIOD = 30
total = 0
netDeposit = []
for index, _ in enumerate(data):
    if index % INCOME_PERIOD == 0:
        total += INCOME
    netDeposit.append(total)

# buy and hold
buyAndHold = []
cashOnHand = 0
shares = 0
for index, price in enumerate(data):
    if index % INCOME_PERIOD == 0:
        cashOnHand += INCOME
    if cashOnHand > 0:
        shares += cashOnHand / price
        cashOnHand = 0
    buyAndHold.append(shares * price)

# buy on recess
cashOnHand = 0
previousHigh = 0
yesterday = 0
shares = 0
buyOnRecess = []
for index, price in enumerate(data):
    if index % INCOME_PERIOD == 0:
        cashOnHand += INCOME

    '''
    1. If the current price drops by over 1% from yesterdays price, **liquidate** the entire portfolio.
    2. If it doesn't drop by more than 1%, use all the cash on hand to buy the stock.
    '''
    if price > previousHigh:
        previousHigh = price
    else:
        if 1 - price / yesterday > 0.01: # more than 1% drop day to day warrants a liquidate
            sellAmount = shares
            shares -= sellAmount
            cashOnHand += sellAmount * price
        elif cashOnHand > 0: # if all else doesn't pass, buy instead with a little of the capital
            spend = cashOnHand
            cashOnHand -= spend
            shares += spend / price
    buyOnRecess.append(shares * price + cashOnHand)
    yesterday = price

print("Final Diff:", buyOnRecess[-1] / buyAndHold[-1])

fig, ax1 = plt.subplots()

# plotting diff
diff = []
for i in range(len(buyAndHold)):
    diff.append(buyOnRecess[i] / buyAndHold[i])

ax1.plot(xAxis, diff, "k", label = "Diff", alpha = 0.2, zorder = 1)

# drawing vertical lines where diff "spikes"
for i in range(5, len(diff)):
    if diff[i] - diff[i-5] > 0.05:
        ax1.axvline(x=i, color='black', alpha=0.04, zorder=0)

ax1.set_ylabel('Diff (Recess / Hold)')
ax1.yaxis.set_label_position("right")
ax1.legend(loc = "upper left", bbox_to_anchor=(0, 1 - 200/plt.gcf().get_size_inches()[1]/plt.gcf().dpi))

# plot strategies
ax2 = ax1.twinx()

ax2.plot(xAxis, buyAndHold, "r", label = "Buy and Hold", zorder = 3)
ax2.plot(xAxis, buyOnRecess, color = "orange", label = "Buy on Recess", zorder = 3)
ax2.plot(xAxis, netDeposit, "g", label = "Net Deposit", alpha = 0.2, zorder = 2)
ax2.plot(xAxis, data, "b", label = "SPY Price", alpha = 0.2, zorder = 2)

ax2.set_xlabel("Days")
ax2.set_ylabel('Portfolio Value')
ax1.yaxis.set_label_position("left")
ax2.legend()

plt.title("Investment Strategies Comparison")
plt.show()