import csv,os 
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema


datafiles = ["./Data/"+datafile for datafile in os.listdir("Data/")]
datasRaw = {}
for datafile in datafiles:
    with open(datafile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        datasRaw[datafile] = [row for row in reader]

data = {}
for i, dataRaw in enumerate([datasRaw[datafile] for datafile in datafiles]):
    data[datafiles[i]] = []
    for j,row in enumerate(dataRaw):
        data[datafiles[i]].append([])
        if(row[0].isdigit()):
            data[datafiles[i]][j].append(int(row[0]))

            for dataColum in range(1,len(row)):
                if(row[dataColum].find("E")<0):
                    data[datafiles[i]][j].append(float(0))
                else:
                    ePart = row[dataColum][row[dataColum].find("E"):]
                    eInt = int(ePart[ePart.find("E")+1:])
                    eIntString = "+"+str(eInt) if eInt >= 0 else str(eInt)
                    dataFloatStr = row[dataColum].replace(ePart,"E"+eIntString)
                    dataFloat = dataFloatStr.replace(",",".")
                    data[datafiles[i]][j].append(float(dataFloat))
        else:
            print(row)


datafileN = 1

xAxis = []
yAxis = [] 

test = data[datafiles[datafileN]]
for testRow in test:
    if(len(testRow) > 0):   
        xAxis.append(float(testRow[1]))
        yAxis.append(float(testRow[3]))

xAxisNp = np.asarray(xAxis)
yAxisNp = np.asarray(yAxis)

avg = np.average(yAxisNp)
yAxisNp = [yVal-avg for yVal in yAxisNp]
yAxisNp = np.asarray(yAxis)


fig, ax = plt.subplots(figsize=(12, 5), tight_layout=True)
ax.plot(xAxisNp, yAxisNp)

ax.set(xlabel='Zeit (in s)', ylabel='Auslenkung (in cm?)',
       title='Test')
ax.axhline(y=0, color='r', linestyle='-')


# for local maxima
maxs = argrelextrema(yAxisNp, np.greater)
ax.plot([xAxisNp[max] for max in maxs],[yAxisNp[max] for max in maxs],"ro")

# for local minima
mins = argrelextrema(yAxisNp, np.less)
ax.plot([xAxisNp[min] for min in mins],[yAxisNp[min] for min in mins],"bo")

maxs = np.array(maxs)
mins = np.array(mins)

lowest = mins.size 
if(maxs.size>mins.size):
    maxs = np.delete(maxs,range(mins.size,maxs.size))
    mins = mins[0]


if(maxs.size<mins.size):
    mins = np.delete(mins,range(maxs.size,mins.size))
    maxs = maxs[0]

diffs = []
for i in range(mins.size):
    diffs.append((float(yAxisNp[maxs[i]])-float(yAxisNp[mins[i]])))


fig.savefig(datafiles[datafileN].replace("Data",".")+".png")
plt.show()


fig2, ax2 = plt.subplots(figsize=(12, 5), tight_layout=True)
ax2.plot(range(mins.size), diffs)
fig2.savefig(datafiles[datafileN].replace("Data",".")+"2.png")

