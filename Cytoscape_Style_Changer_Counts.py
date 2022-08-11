"""Changes the "Styles" file from an exported Cytoscape website

Usage:
    ./TestDataExtractor.py


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

import csv
import json
from pathlib import Path
from operator import itemgetter
from pylab import cm
from pylab import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl



def jonTheSam(hexString):
    redHex = hexString[1:3]
    greenHex = hexString[3:5]
    blueHex = hexString[5:7]
    return int(redHex, 16), int(greenHex, 16), int(blueHex, 16)

def labelFormatter(sortedTuples):
    formatedList = []
    for i in sortedTuples:
        formatedList.append('{:.2f}'.format(i[1]) + '  ' + i[0])
    return formatedList

def fileImport():
    isThereAFile = True
    file_name = ''
    while isThereAFile:
        file_name = input('What\'s the name of the file? ')
        if file_name in '':
            file_name = 'Astrocyte1.csv'
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

    geneDict = {}
    countsDict = {}
    print('import first file')
    file_name = fileImport()




    try:
        with open(file_name, mode='r', encoding='UTF-8-sig') as csv_file:
            read_csv_file = csv.reader(csv_file, delimiter=';')
            # delimiter can cause problems, if it is not exported as ";" but as ",", "blank" or something similar
            for row in read_csv_file:
                if ',' in row[1]:
                    geneDict[row[0]] = float(row[1].replace(',', '.'))
                else:
                    geneDict[row[0]] = float(row[1])
    except Exception as error:
        print('Check the delimiters, delete headlines/titles, read the README for further information')
        input('press Enter to Exit')
        exit(1)

    print('import second file')
    file_name = fileImport()
    try:
        with open(file_name, mode='r', encoding='UTF-8-sig') as csv_file:
            read_csv_file = csv.reader(csv_file, delimiter=';')
            # delimiter can cause problems, if it is not exported as ";" but as ",", "blank" or something similar
            for row in read_csv_file:
                if ',' in row[1]:
                    countsDict[row[0]] = float(row[1].replace(',', '.'))
                else:
                    countsDict[row[0]] = float(row[1])
    except Exception as error:
        print('Check the delimiters, delete headlines/titles, read the README for further information')
        input('press Enter to Exit')
        exit(1)

    for key in geneDict:
        if key in [*countsDict]:
            geneDict[key] = geneDict[key]/countsDict[key]

    print('count calculation completed')




# if data input failed, possible errors might be new lines or delimiters in the CSV File, first troubleshooting step would be to check there.



    sortedExpressionLevels = list(geneDict.items())
    list.sort(sortedExpressionLevels, key=itemgetter(1))

    sortedDict = dict(sortedExpressionLevels)
    lableTicksValues = list(sortedDict.values())
    #for i in range(len(lableTicksValues)):
        #lableTicksValues[i] = round(lableTicksValues[i], 2)

    print('What should be the threshold?')
    threshold = int(input())

    overThresholdDict = {}
    underThresholdDict = {}

    for key in sortedDict:
        width = round(sortedDict[key])
        if width >= threshold:
            overThresholdDict[key] = sortedDict[key]
        else:
            underThresholdDict[key] = sortedDict[key]


    styles_sheet = {}
    with open('template_styles.json') as styles:
        styles_sheet = json.load(styles)

    numberOfItems = len(underThresholdDict)
    coolWarmColorGetter = cm.get_cmap('coolwarm', numberOfItems + 1) #+1 inside the ()

    gradientColors = []
    for i in range(coolWarmColorGetter.N):
        rgba = coolWarmColorGetter(i)
        gradientColors.append(matplotlib.colors.rgb2hex(rgba))

    for key in overThresholdDict:
        gradientColors.append('#B40426')
    underThresholdDict.update(overThresholdDict)
    sortedDict = underThresholdDict

    colorCount = 0

    for key in sortedDict:
        sortedDict[key] = jonTheSam(gradientColors[colorCount])
        colorCount += 1

    for i in styles_sheet:
        if 'title' in i:
            if i['title'] == 'default':
                for json_style in i['style']:
                    if 'content' in json_style['css']:
    # used to dig down the datastructure and find the correct values, to then change these accordingly.
                        if json_style['css']['content'].rstrip() in geneDict:
                            key = json_style['css']['content'].rstrip()
                            width = round(geneDict[key]/2)
                            if width <= 0:
                                json_style['css']['width'] = 3 #old value was 1
                                #threshold for value to not fall below 0, thus not showing an arrow anymore
                            elif width >= (threshold/2):
                                #threshold takes over from the first threshold for the coloration change, but due to
                                #changes in the width, this threshold might not tirgger, thus  change of the threshold is needed
                                json_style['css']['width'] = 3
                                #threshold for the purine pathway, need changes if other data is used

                            else:
                                json_style['css']['width'] = 3 #old value was width

                            json_style['css']['line-color'] = 'rgb(' + str(sortedDict[key][0]) + ',' + str(sortedDict[key][1]) \
                                                             + ',' + str(sortedDict[key][2]) + ')'
                            json_style['css']['line-style'] = 'solid'

                            json_style['css']['target-arrow-color'] = 'rgb(' + str(sortedDict[key][0]) + ',' + str(sortedDict[key][1]) \
                                                             + ',' + str(sortedDict[key][2]) + ')'

                            json_style['css']['source-arrow-color'] = 'rgb(' + str(sortedDict[key][0]) + ',' + str(sortedDict[key][1]) \
                                                                      + ',' + str(sortedDict[key][2]) + ')'
                        else:
                            json_style['css']['line-style'] = 'dashed'

    # The change of the JSON file resulted in the change of the overall style of the visualized data
    # and bridged the gap between the pure data and its representation in Cytostyle

    #for i in range(len(lableTicksValues)):
        #if lableTicksValues[i] == lableTicksValues[i+1]:
            #lableTicksValues[i+1] = round(())

    tickPlaceholder = []
    for i in range(len(lableTicksValues)):
        tickPlaceholder.append(i)

    fig, ax = plt.subplots(figsize=(3, 15))
    plt.subplots_adjust(right=0.3)

    cmap = mpl.colors.ListedColormap(gradientColors)
    norm = mpl.colors.BoundaryNorm(tickPlaceholder, colorCount)



    colobar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                 cax=ax, orientation='vertical', format='%.2f',         #why is format="%.1f" not working?
                 ticks=tickPlaceholder)
    colobar.set_label(label="Fold Change", size='large', weight='bold')
    #colobar.ax.set_title(">300")
    #colobar.set_label(label=">300", size="large", weight="bold", rotation=180)


    colobar.ax.set_yticklabels(labelFormatter(sortedExpressionLevels))
    #plt.show()
    plt.savefig("colorbar.png", dpi=1200)


    with open('web_session/data/styles.js', 'w', encoding='utf-8') as json_export:
        json_export.write('var styles = ')
        json.dump(styles_sheet, json_export, ensure_ascii=False, indent=2, sort_keys=True)



    print('Done')

    input('press enter to exit')

