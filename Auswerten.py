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

tDiffsList = []
relativeDiffsList = []

for datafileN in range(len(datafiles)):
        
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
    yAxisNp = np.asarray(yAxisNp)
    if(datafileN == 2):
        offset = 14
        xAxisNp = [xVal-offset for xVal in xAxisNp]
        xAxisNp = np.asarray(xAxisNp)
    if(datafileN == 0):
        offset = -4
        xAxisNp = [xVal-offset for xVal in xAxisNp]
        xAxisNp = np.asarray(xAxisNp)


    fig, ax = plt.subplots(figsize=(12, 5), tight_layout=True)
    ax.plot(xAxisNp, yAxisNp)
    if(datafileN == 0):
        ax.set(xlabel='Zeit (in s)', ylabel='Auslenkung (in cm)',
            title='Auslenkung pro Zeit mit markierten Extrempunkten (Dicke Feder mit 250g)')
    if(datafileN == 1):
        ax.set(xlabel='Zeit (in s)', ylabel='Auslenkung (in cm)',
            title='Auslenkung pro Zeit mit markierten Extrempunkten (D??nne Feder mit 500g)')
    if(datafileN == 2):
        ax.set(xlabel='Zeit (in s)', ylabel='Auslenkung (in cm)',
            title='Auslenkung pro Zeit mit markierten Extrempunkten (Dicke Feder mit 500g (1))')
    if(datafileN == 2):
        ax.set(xlabel='Zeit (in s)', ylabel='Auslenkung (in cm)',
            title='Auslenkung pro Zeit mit markierten Extrempunkten (Dicke Feder mit 500g (2))')


    ax.axhline(y=0, color='r', linestyle='-')


    # for local maxima
    maxs = argrelextrema(yAxisNp, np.greater)
    ax.plot([xAxisNp[max] for max in maxs],[yAxisNp[max] for max in maxs],"ro")

    # for local minima
    mins = argrelextrema(yAxisNp, np.less)
    ax.plot([xAxisNp[min] for min in mins],[yAxisNp[min] for min in mins],"bo")

    fig.savefig(datafiles[datafileN].replace("Data",".").replace(".csv","")+".png")
    plt.show()

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
    tDiffs = []
    for i in range(mins.size):
        diffs.append((float(yAxisNp[maxs[i]])-float(yAxisNp[mins[i]])))
        tDiffs.append((xAxisNp[maxs[i]] + xAxisNp[mins[i]])/2)

    relativeDiffs = []
    for i in range(mins.size):
        relativeDiffs.append(diffs[i]/max(diffs))


    fig2, ax2 = plt.subplots(figsize=(12, 5), tight_layout=True)
    ax2.plot(tDiffs, relativeDiffs)
    if(datafileN == 0):
        ax2.set(xlabel='Zeit (in s)', ylabel='Auslenkung (relativ zur Maximalauslenkung)',
            title='Relative Auslenkung pro Zeit (Dicke Feder mit 250g)')
    if(datafileN == 1):
        ax2.set(xlabel='Zeit (in s)', ylabel='Auslenkung (relativ zur Maximalauslenkung)',
            title='Relative Auslenkung pro Zeit (D??nne Feder mit 500g)')
    if(datafileN == 2):
        ax2.set(xlabel='Zeit (in s)', ylabel='Auslenkung (relativ zur Maximalauslenkung)',
            title='Relative Auslenkung pro Zeit (Dicke Feder mit 500g (1))')
    if(datafileN == 3):
        ax2.set(xlabel='Zeit (in s)', ylabel='Auslenkung (relativ zur Maximalauslenkung)',
            title='Relative Auslenkung pro Zeit (Dicke Feder mit 500g (2))')
    fig2.savefig(datafiles[datafileN].replace("Data",".").replace(".csv","")+"2.png")
    tDiffsList.append(tDiffs)
    relativeDiffsList.append(relativeDiffs)


fig3, ax3 = plt.subplots(figsize=(12, 5), tight_layout=True)
lenList = [len(tDiff) for tDiff in tDiffsList]
maxXLenIndex = lenList.index(max(lenList))

ax3.plot(tDiffsList[0], relativeDiffsList[0],"-r",label="Dicke Feder mit 250g")
ax3.plot(tDiffsList[1], relativeDiffsList[1],"-g",label="D??nne Feder mit 500g")
ax3.plot(tDiffsList[2], relativeDiffsList[2],"-b",label="Dicke Feder mit 500g (1)")
ax3.plot(tDiffsList[3], relativeDiffsList[3],"-m",label="Dicke Feder mit 500g (2)")

ax3.set(xlabel='Zeit (in s)', ylabel='Auslenkung (relativ zur Maximalauslenkung)',
        title='Relative Auslenkung pro Zeit (kombiniert)')
ax3.legend()

fig3.savefig("Zusammen.png")

print(datafiles)