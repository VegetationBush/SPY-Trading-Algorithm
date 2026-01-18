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

# diff = []
# for i in range(len(buyAndHold)):
#     diff.append(buyOnRecess[i] / buyAndHold[i])
# plt.plot(xAxis, diff, label = "Diff")
plt.plot(xAxis, buyAndHold, label = "Buy and Hold")
plt.plot(xAxis, buyOnRecess, label = "Buy on Recess")
plt.plot(xAxis, deposit, label = "Deposit")
plt.plot(xAxis, data, label = "SPY Price")

plt.legend()
plt.show()