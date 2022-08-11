"""Generates a Heatmap from two different CSV files


License:
    MIT License

    Copyright (c) [2021] [Philipp Gessner]

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE."""
########################################################################################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
from pathlib import Path


def fileImport():
    isThereAFile = True
    file_name = ''
    while isThereAFile:
        file_name = input('What\'s the name of the file? ')
        if file_name in '':
            file_name = 'Astrocyte.csv'
        elif '.csv' not in file_name:
            file_name += '.csv'

        checkFileName = Path(file_name)
        if checkFileName.exists():
            print('File found', file_name)
            isThereAFile = False
        else:
            print('File not found', file_name)
    return file_name


if __name__ == '__main__':

    dict1 = {}
    dict2 = {}
    print('import first file')
    file_name1 ="Neuron.csv"

    # dict1
    file_name1 = fileImport()
    try:
        with open(file_name1, mode='r', encoding='UTF-8-sig') as csv_file:
            read_csv_file = csv.reader(csv_file, delimiter=';')
            # delimiter can cause problems, if it is not exported as ";" but as ",", "blank" or something similar
            for row in read_csv_file:
                if ',' in row[1]:
                    dict1[row[0]] = float(row[1].replace(',', '.'))
                else:
                    dict1[row[0]] = float(row[1])
    except Exception as error:
        print('Check the delimiters, delete headlines/titles, read the README for further information')
        input('press Enter to Exit')
        exit(1)

    if '.' in file_name1:
        file_name1 = file_name1.split('.')[0]

    numberOfGenes = 0
    listOfGenes = []

    for key in dict1:
        listOfGenes.append(key)

    numberOfGenes = len(listOfGenes)


    listOfExpressionLevels = []
    for key in listOfGenes:
        if key in [*dict1]:
            listOfExpressionLevels.append(dict1[key])
        else:
            listOfExpressionLevels.append(np.nan)

    data = {'Gene Names': np.tile(listOfGenes, 1),
            'Cell Types': np.repeat([file_name1], numberOfGenes),
            'values': listOfExpressionLevels
            }

    threshold1 = int(input('Please enter the threshold'))
    df1 = pd.DataFrame(data, columns=['Gene Names', 'Cell Types', 'values'])  # generates the dataframe
    df1 = df1.pivot('Gene Names', 'Cell Types', 'values', )
    df1 = df1.sort_values(by=[file_name1], ascending=False)


    print('import second file')
    #dict2
    file_name2 = "Astrocyte.csv"
    file_name2 = fileImport()
    try:
        with open(file_name2, mode='r', encoding='UTF-8-sig') as csv_file:
            read_csv_file = csv.reader(csv_file, delimiter=';')
            # delimiter can cause problems, if it is not exported as ";" but as ",", "blank" or something similar
            for row in read_csv_file:
                if ',' in row[1]:
                    dict2[row[0]] = float(row[1].replace(',', '.'))
                else:
                    dict2[row[0]] = float(row[1])
    except Exception as error:
        print('Check the delimiters, delete headlines/titles, read the README for further information')
        input('press Enter to Exit')
        exit(1)

    if '.' in file_name2:
        file_name2 = file_name2.split('.')[0]

    threshold2 = int(input('Please enter the threshold'))

    answer = input("Do you want to sort each column by itself or compare to the first import? "
                   "Please enter 1 for sorting each column and 2 for comparing the first import")

    #Plotting two dataframes with both their maximum values as each maximum values respectivly
    if answer in ['1', '']:
        numberOfGenes2 = 0
        listOfGenes2 = []

        for key in dict2:
            if key not in listOfGenes2:
                listOfGenes2.append(key)

        numberOfGenes2 = len(listOfGenes2)

        listOfExpressionLevels2 = []
        for key in listOfGenes2:
            if key in [*dict2]:
                listOfExpressionLevels2.append(dict2[key])
            else:
                listOfExpressionLevels2.append(np.nan)

        data = {'Gene Names': np.tile(listOfGenes2, 1),
                'Cell Types': np.repeat([file_name2], numberOfGenes2),
                'values': listOfExpressionLevels2
                }
        #threshold2 = int(input('Please enter the threshold'))

        df2 = pd.DataFrame(data, columns=['Gene Names', 'Cell Types', 'values'])  # generates the dataframe
        df2 = df2.pivot('Gene Names', 'Cell Types', 'values', )
        df2 = df2.sort_values(by=[file_name2], ascending=False)

        # figure generation and options
        fig, (ax1, ax2) = plt.subplots(ncols=2)
        fig.subplots_adjust(wspace=0.1)
        mask1 = df1.isnull()
        mask2 = df2.isnull()
        sns.set_context("paper", rc={"font.size": 10, "axes.titlesize": 10, "axes.labelsize": 10})
        sns.heatmap(df1, cmap="coolwarm", ax=ax1, cbar=False, annot=True, annot_kws={"size": 8}, mask=mask1, fmt='.2f',
                vmin=0, vmax=threshold1, yticklabels=1, cbar_kws={"label": "Expression Level [TPM]"})
        # Colorbar
        fig.colorbar(ax1.collections[0], ax=ax1, location="left", use_gridspec=False, pad=0.3, label="Expression Level [TPM]")
        # Colorbar
        ax1.xaxis.tick_top() #putting x-lable on top
        ax1.set_xticklabels(ax1.get_xmajorticklabels(),fontsize = 20) #changing xlable font size
        ax1.set_yticklabels(ax1.get_ymajorticklabels(), fontsize=6)
        ax1.set(xlabel=None)
        ax1.set(ylabel=None)


        sns.heatmap(df2, cmap="coolwarm", ax=ax2, cbar=False, annot=True, annot_kws={"size": 8}, mask=mask2, fmt='.2f',
                vmin=0, vmax=threshold2, yticklabels=1)
        # Colorbar
        fig.colorbar(ax2.collections[0], ax=ax2, location="right", use_gridspec=False, pad=0.3, label="Expression Level [TPM]")
        # Colorbar
        ax2.xaxis.tick_top()
        ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize=20)
        ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize=6)
        ax2.yaxis.set_label_position("right")
        ax2.set(xlabel=None)
        ax2.set(ylabel=None)
        # ax2.yaxis.labelpad = 0.1
        ax2.yaxis.tick_right()
        ax2.tick_params(rotation=0)
        # plt.show(dpi=1200)
        plt.savefig('Comparison_Heatmap', dpi=1200)

        print('done')
        input()
        exit(0)

    # Plotting two dataframes to the maximum value of the first dataframe
    if answer in ["2"]:

        numberOfGenes2 = 0
        listOfGenes2 = []

        for key in dict2:
            if key not in listOfGenes2:
                listOfGenes2.append(key)

        numberOfGenes2 = len(listOfGenes2)

        listOfExpressionLevels2 = []
        for key in listOfGenes2:
            if key in [*dict2]:
                listOfExpressionLevels2.append(dict2[key])
            else:
                listOfExpressionLevels2.append(np.nan)

        data = {'Gene Names': np.tile(listOfGenes2, 1),
                'Cell Types': np.repeat([file_name2], numberOfGenes2),
                'values': listOfExpressionLevels2
                }

        df2 = pd.DataFrame(data, columns=['Gene Names', 'Cell Types', 'values'])  # generates the dataframe
        df2 = df2.pivot('Gene Names', 'Cell Types', 'values', )
        df_sorted_as_df1 = df1.merge(df2, left_index=True, right_index=True)
        df_sorted_as_df1.drop(df_sorted_as_df1.iloc[:,0:1], inplace=True, axis=1)
        #df2 = df2.sort_values(by=[file_name1], ascending=False)

        # figure generation and options
        fig, (ax1, ax2) = plt.subplots(ncols=2)
        fig.subplots_adjust(wspace=0.1)
        mask1 = df1.isnull()
        mask2 = df_sorted_as_df1.isnull()
        sns.set_context("paper", rc={"font.size": 10, "axes.titlesize": 10, "axes.labelsize": 10})
        sns.heatmap(df1, cmap="coolwarm", ax=ax1, cbar=False, annot=True, annot_kws={"size": 8}, mask=mask1, fmt='.2f',
                    vmin=0, vmax=threshold1, yticklabels=1, cbar_kws={"label": "Expression Level [TPM]"})
        # Colorbar
        fig.colorbar(ax1.collections[0], ax=ax1, location="left", use_gridspec=False, pad=0.3, label="Expression Level [TPM]")
        # Colorbar
        ax1.xaxis.tick_top()
        ax1.set_xticklabels(ax1.get_xmajorticklabels(), fontsize=20)
        ax1.set_yticklabels(ax1.get_ymajorticklabels(), fontsize=6)
        ax1.set(xlabel=None)
        ax1.set(ylabel=None)

        sns.heatmap(df_sorted_as_df1, cmap="coolwarm", ax=ax2, cbar=False, annot=True, annot_kws={"size": 8}, mask=mask2, fmt='.2f',
                    vmin=0, vmax=threshold2, yticklabels=1)
        # Colorbar
        fig.colorbar(ax2.collections[0], ax=ax2, location="right", use_gridspec=False, pad=0.3,
                     label="Expression Level [TPM]")
        # Colorbar
        ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize=6)
        ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize=20)
        ax2.xaxis.tick_top()
        ax2.yaxis.set_label_position("right")
        ax2.set(xlabel=None)
        ax2.set(ylabel=None)
        # ax2.yaxis.labelpad = 0.1
        ax2.yaxis.tick_right()
        ax2.tick_params(rotation=0)
        # plt.show(dpi=1200)
        plt.savefig('Comparison_Heatmap', dpi=1200)

        print('done')
        input()
        exit(0)