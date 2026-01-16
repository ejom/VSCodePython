import numpy

import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

#x = numpy.random.normal(10, 3, 10)
#y = (numpy.random.normal(190, 20, 10))*x+((numpy.random.normal(9, 2, 10)))*x**3+(numpy.random.normal(92, 90, 10))
#x=[13.87780441, 12.19476746,  7.82055181, 11.34519261, 11.85531986,  9.41976251, 9.9665177,  16.76674335, 12.08264885,  6.56790524]
#y=[21022.68070625, 18466.45001678,  3939.10518872, 17893.67212933, 13860.26331447,  6338.11121511, 10460.31718752, 20670.96252663, 21961.17832686,  3211.97497353]

#x = numpy.random.normal(10, 3, 10)
#y = (numpy.random.normal(190, 20, 10))+((numpy.random.normal(9, 2, 10)))+(numpy.random.normal(92, 90, 10))

x = [50.8214662, 11.51763917,  6.79224813, 11.07808012, 14.33212775,  8.85842006, 16.80919696, 4.53742281,  9.91129079, 8.7158105,  10.8394648, 29.43458508, 45.37594954, 55.51568334, 43.45779085, 37.2094763,  39.71451434,  33.06066848, 42.13515667, 67.10040374, 41.76755369]
y_org = [1000.8495736296, 248.65894572, 397.08524446, 200.15068278, 323.88011377, 279.04768083, 337.28294253, 279.73294259, 293.89796886, 253.49593762, 328.76765463, 100.35301421,  95.74208171, 107.51680774, 102.18729387,  91.28501013, 99.97351786, 103.1226262,   99.94460628,  93.08889983, 104.66997988]

def tranFun(x, y):
    return y*(x**3*numpy.sin(x+y)-x**2*numpy.sin(2*x)+x*numpy.sin(3*x**2)-x**3)

y=[]
for X, Y in zip(x, y_org):
    y.append(tranFun(X, Y))

print(y)

train_x = x[:16]
train_y = y[:16]

test_x = x[16:]
test_y = y[16:]

#Identify trends in the training R^2 val.
#Use more complex input
r2 = float("-inf")
bestModel = None
for i in range(20):
    mymodel = numpy.poly1d(numpy.polyfit(train_x, train_y, i))
    nextR2 = r2_score(test_y, mymodel(test_x))
    if nextR2>r2 and r2_score(train_y, mymodel(train_x))>0.6:
        r2=nextR2
        numParameters = i+1
        bestModel = mymodel

print(numParameters)
print(r2)
print(r2_score(train_y, bestModel(train_x)))

# Create the scatter plot
plt.scatter(x, y)

# Optional: Add labels and a title for clarity
plt.xlabel("X-axis Label")
plt.ylabel("Y-axis Label")
plt.title("Scatter Plot of Two Lists")

plt.plot(bestModel)

# Display the plot
plt.show()
