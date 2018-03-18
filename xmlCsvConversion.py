import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def conversion(path):
    fileList = []
    for xmlFile in glob.glob(path + '/*.xml'):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            fileList.append(value)
    columns = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xmlOutput = pd.DataFrame(fileList), columns=columns)
    return xmlOutput

for directory in ['train','test']:
    getPath = os.path.join(os.getcwd(), 'images/{}'.format(directory))
    xmlOutput = conversion(getPath)
    xmlOutput.to_csv('data/{}_labels.csv'.format(directory), index=None)
    print('Converted both train and test labels from xml to csv!')
