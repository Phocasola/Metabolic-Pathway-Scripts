"""can calculate the mean values from two different CSV files

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
from pathlib import Path

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
    
    dict1 = {}
    dict2 = {}
    print('import first file')
    file_name = fileImport()
    
    try:
        with open(file_name, mode='r', encoding='UTF-8-sig') as csv_file:
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

    print('import second file')
    file_name = fileImport()
    try:
        with open(file_name, mode='r', encoding='UTF-8-sig') as csv_file:
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

    for key in dict1:
        if key in [*dict2]:
            dict1[key] += dict2[key]
            dict1[key] /= 2
            
    print('calculations complete')
    input('press Enter to exit')
    
    with open('Mean_Data.csv', mode='w', newline='', encoding='UTF-8-sig') as exportFile:
        exportFileWriter = csv.writer(exportFile, delimiter=';', lineterminator='\r\n')
        exportFileWriter.writerows(dict1.items())
            
    
            
        