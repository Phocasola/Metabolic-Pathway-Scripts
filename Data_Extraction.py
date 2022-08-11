"""Filters relevant data out of an CSV-file and saves it in a separate CSV-file

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
    SOFTWARE.

in recogniztion of my dear friend Samuel Alves Santos, aka Jonthe, who helped me with this lovely piece of code."""
########################################################################################################################
import csv
from pathlib import Path


if __name__ == '__main__':

    completeDict = {}
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

    answer = input('Do you want to convert from FPKM to TPM? Please answer with YES or NO ')
    if answer in ['YES', 'yes', 'y', '']:
        try:
            with open(file_name, mode='r', encoding='UTF-8-sig') as csv_file:
                read_csv_file = csv.reader(csv_file, delimiter=';')
                # delimiter can cause problems, if it is not exported as ";" but as ",", "blank" or something similar
                for row in read_csv_file:
                    if ',' in row[1]:
                        completeDict[row[0]] = float(row[1].replace(',', '.'))
                    else:
                        completeDict[row[0]] = float(row[1])
        except Exception as error:
            print('Check the delimiters, delete headlines/titles, read the README for further information')
            input('press Enter to Exit')
            exit(1)

        sumFPKM = 0
        for key in completeDict:
            sumFPKM += completeDict[key]

        for key in completeDict:
            completeDict[key] = (completeDict[key]/sumFPKM)*1000000

        print('conversion completed')

    else:
        try:
            with open(file_name, mode='r', encoding='UTF-8-sig') as csv_file:
                read_csv_file = csv.reader(csv_file, delimiter=';')
                # delimiter can cause problems, if it is not exported as "," but as ";", "blank" or something similar
                for row in read_csv_file:
                    if ',' in row[1]:
                        completeDict[row[0]] = float(row[1].replace(',', '.'))
                    else:
                        completeDict[row[0]] = float(row[1])
        except Exception as error:
            print('Check the delimiters, delete headlines/titles, read the README for further information')
            input('press Enter to Exit')
            exit(1)

        print('There will be no conversion')

    outputFileName = file_name.split('.')[0]
    outputFileName = outputFileName + '_extracted.csv'
    isThereAKeyFile = True
    while isThereAKeyFile:
        file_name = input('What\'s the name of the file with the Data extraction key words? ')
        if file_name in '':
            file_name = 'Data_extraction_keys.csv'
        elif '.csv' not in file_name:
            file_name += '.csv'

        checkFileName = Path(file_name)
        if checkFileName.exists():
            print('File found', file_name)
            isThereAKeyFile = False
        else:
            print('File not found', file_name)

    dataExtractionDict = {}

    with open(file_name, mode='r', encoding='UTF-8-sig') as csv_file:
        read_csv_file = csv.reader(csv_file, delimiter=';')
        # delimiter can cause problems, if it is not exported as ";" but as ",", "blank" or something similar
        for row in read_csv_file:
            if row[1] == '':
                dataExtractionDict[row[0]] = row[0]
            else:
                dataExtractionDict[row[0]] = row[1]
    #opening the file and copying the wanted data into a dictionary

    finalDict = {}
    notFoundGenes = []
    #test=[*completeDict]
    for key, value in dataExtractionDict.items():
        if key in [*completeDict]:
            if value in [*finalDict]:
                finalDict[value] += completeDict[key]
            else:
                finalDict[value] = completeDict[key]
        else:
            notFoundGenes.append(key)
    print('The following gene have not been found', notFoundGenes)
    #checking if all needed data have been found and if not changing the output accordingly. Allowing the user to know if data is missing.

    with open('Extracted_Data/%s' %outputFileName, mode='w', newline='', encoding='UTF-8-sig') as exportFile:
        exportFileWriter = csv.writer(exportFile, delimiter=';', lineterminator='\r\n')
        exportFileWriter.writerows(finalDict.items())

    print('Done')

    input('press enter to exit')
