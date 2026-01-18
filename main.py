'''
Yes this is spaghetti code.
No I don't want to fix it!
It just works.
'''

import matplotlib.pyplot as plt

data = []

with open("spy_historical.txt") as f:
    for line in f:
        # Remove newline, split by comma, take the last item
        last_number = line.strip().split(",")[-1]
        # Convert to float if you want numbers, not strings
        data.append(float(last_number))
data.reverse()

xAxis = [i for i in range(len(data))]

INCOME = 10
INCOME_PERIOD = 30
total = 0
deposit = []
for index, _ in enumerate(data):
    if index % INCOME_PERIOD == 0:
        total += INCOME
    deposit.append(total)

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
descendDays = 0
shares = 0
buyOnRecess = []
for index, price in enumerate(data):
    if index % INCOME_PERIOD == 0:
        cashOnHand += INCOME

    if price > previousHigh:
        previousHigh = price
        descendDays = 0
    else:
        descendDays += 1
        
        if descendDays >= 3:
            spend = min(cashOnHand, max(20, cashOnHand * min(0.5, descendDays / 15)))
            cashOnHand -= spend
            shares += spend / price
        if 1 - price / yesterday > 0.01: # more than 1% drop day to day warrants a sell
            if shares > 0:
                sellAmount = shares * 1
                shares -= sellAmount
                cashOnHand += sellAmount * price
        elif cashOnHand > 0: # if all else doesn't pass, buy instead with a little of the capital
            spend = cashOnHand
            cashOnHand -= spend
            shares += spend / price
    buyOnRecess.append(shares * price + cashOnHand)
    yesterday = price
print(buyOnRecess[-1] / buyAndHold[-1])

fig, ax1 = plt.subplots()

diff = []
for i in range(len(buyAndHold)):
    diff.append(buyOnRecess[i] / buyAndHold[i])

ax1.plot(xAxis, diff, "k", label = "Diff", alpha = 0.2, zorder = 1)

ax1.set_ylabel('Diff (Recess / Hold)')
ax1.yaxis.set_label_position("right")
ax1.legend(loc = "upper left", bbox_to_anchor=(0, 1 - 120/plt.gcf().get_size_inches()[1]/plt.gcf().dpi))

ax2 = ax1.twinx()

ax2.plot(xAxis, buyAndHold, "r", label = "Buy and Hold", zorder = 3)
ax2.plot(xAxis, buyOnRecess, color = "orange", label = "Buy on Recess", zorder = 3)
ax2.plot(xAxis, deposit, "g", label = "Deposit", alpha = 0.2, zorder = 2)
ax2.plot(xAxis, data, "b", label = "SPY Price", alpha = 0.2, zorder = 2)

ax2.set_xlabel("Days")
ax2.set_ylabel('Portfolio Value')
ax1.yaxis.set_label_position("left")
ax2.legend()

plt.title("Investment Strategies Comparison")
plt.show()