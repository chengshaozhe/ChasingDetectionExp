import pandas as pd
import os
import glob
DIRNAME = os.path.dirname(__file__)
import matplotlib.pyplot as plt
# matplotlib.style.use('ggplot')
import numpy as np
from scipy.stats import ttest_ind

if __name__ == '__main__':
    dataPath = os.path.join(DIRNAME, 'visualSearchResults')
    df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(dataPath, '*.csv'))))
    # df.to_csv("all.csv")

    # print(df.head(6))
    nubOfSubj = len(df["name"].unique())
    statDF = pd.DataFrame()

    # df = df.loc[df['trail'].isin(range(41))]
    df = df.loc[df['trail'].isin(range(41, 81))]

    df["hit"] = df.apply(lambda row: 1 if row['condition'] == 1 and row['chosenWolfIndex'] == 1.0 and row['chosenSheepIndex'] == 0.0 else 0, axis=1)
    df["hitControl"] = df.apply(lambda row: 1 if row['condition'] == 3 and row['chosenWolfIndex'] == 1.0 and row['chosenSheepIndex'] == 0.0 else 0, axis=1)

    df["wolfMasterExp"] = df.apply(lambda row: 1 if row['condition'] == 1 and row['chosenWolfIndex'] == 2.0 and row['chosenSheepIndex'] == 1.0 else 0, axis=1)
    df["wolfMasterControl"] = df.apply(lambda row: 1 if row['condition'] == 3 and row['chosenWolfIndex'] == 2.0 and row['chosenSheepIndex'] == 1.0 else 0, axis=1)

    df['keyCheck'] = df.apply(lambda row: 0 if pd.isnull(row['chosenWolfIndex']) else 1, axis=1)
    df['search'] = df.apply(lambda row: 1 if (row['condition'] % 2 == 1 and row['keyCheck'] == 1) or (row['condition'] % 2 == 0 and row['keyCheck'] == 0) else 0, axis=1)
    # print(df.head(6))

    statDF['expSearchAcc'] = df[(df['condition'] == 1) | (df['condition'] == 2)].groupby('name')["search"].mean()
    statDF['controlSearchAcc'] = df[(df['condition'] == 3) | (df['condition'] == 4)].groupby('name')["search"].mean()
    statDF['searchAcc'] = df.groupby('name')["search"].mean()
    statDF['searchAccSD'] = df.groupby('name')["search"].std()
    # print('searchAcc mean, std:', np.mean(statDF['searchAcc']), np.std(statDF['searchAcc']))

    exp = df[df['condition'] == 1]
    control = df[df['condition'] == 3]

    # statDF["hitNumber"] = df.groupby('name')["hit"].sum()
    # statDF["hitControlNumber"] = df.groupby('name')["hitControl"].sum()
    # statDF["wolfMasterNumberExp"] = df.groupby('name')["wolfMasterExp"].sum()
    # statDF["wolfMasterNumberControl"] = df.groupby('name')["wolfMasterControl"].sum()

    statDF["hitRate"] = df[(df['condition'] == 1)].groupby('name')["hit"].mean()
    statDF['hitControlRate'] = df[(df['condition'] == 3)].groupby('name')["hitControl"].mean()

    statDF["expReactionTime"] = exp.groupby('name')["reactionTime"].mean()
    statDF["controlReactionTime"] = control.groupby('name')["reactionTime"].mean()

    print(statDF)
    # statDF.to_csv("statDF.csv")


# plot
    fig = plt.figure()
    axForDraw = fig.add_subplot(1, 1, 1)

    # x = np.arange(2)
    # xlabel = ['exp', 'control']

    x = np.arange(nubOfSubj)
    plt.xlabel('subj')
    xlabel = list(np.arange(1, nubOfSubj + 1))
    xlabel = df["name"].unique()

    plt.xticks(x, xlabel)


# Identification
    a = statDF["hitRate"]
    b = statDF["hitControlRate"]
    # c = statDF["wolfMasterExpRate"]
    # d = statDF["wolfMasterControlRate"]
    # print('ttest', ttest_ind(statDF["hitRate"], statDF["hitControlRate"]))
    # a = [statDF["hitRate"].mean(), statDF["hitControlRate"].mean()]
    plt.ylabel('Identification accuracy')
    axForDraw.set_ylim(0, 1)

# search acc
    # a = statDF['expSearchAcc']
    # b = statDF['controlSearchAcc']
    # c = statDF['searchAcc']
    # print('ttest', ttest_ind(statDF["expSearchAcc"], statDF["controlSearchAcc"]))
    # a = [statDF["expSearchAcc"].mean(), statDF["controlSearchAcc"].mean()]
    # plt.ylabel('search accuracy')
    # axForDraw.set_ylim(0, 0.7)

# reacition time
    # a = statDF["expReactionTime"]
    # b = statDF["controlReactionTime"]
    # a = [statDF["expReactionTime"].mean(), statDF["controlReactionTime"].mean()]
    # plt.ylabel('Response Time')
    # axForDraw.set_ylim(0, 25000)

    totalWidth, n = 1, nubOfSubj
    width = totalWidth / n
    xSeq = x - (totalWidth - width) / nubOfSubj

    # plt.bar(x, a, width=0.5)

    plt.bar(xSeq, a, width=width, label='exp')
    plt.bar(xSeq + width, b, width=width, label='control')
    # plt.bar(xSeq + width * 2, c, width=width, label='wolfMasterExpRate')
    # plt.bar(xSeq + width * 3, d, width=width, label='wolfMasterControlRate')

    plt.legend(loc='best')
    # plt.title('search for chasing with line')
    # plt.title('search for chasing with line trial=1-40')
    plt.title('search for chasing with line trial=41-80')

    plt.show()
