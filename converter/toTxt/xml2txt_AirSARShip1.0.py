"""This script is used to convert xml file to txt file for AIR SAR Ship1.0 Dataset."""

import xml.etree.ElementTree as ET
import os


class xml2txt(object):
    def __init__(self, data_path, xml_folder_name, txt_folder_name):
        self.data_path = data_path
        self.xml_folder_name = xml_folder_name
        self.txt_folder_name = txt_folder_name
        self.txt_ext = 'txt'
        self.xmllist = os.listdir(os.path.join(self.data_path, self.xml_folder_name))

    def read_xml(self, xmlname):
        obj_infos = []  # [[xmin, ymin, xmax, ymax, cls_name], ... []]
        infile = open(os.path.join(self.data_path, self.xml_folder_name, xmlname))
        tree = ET.parse(infile)
        root = tree.getroot()

        for obj in root.iter('object'):
            cls_name = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            obj_infos.append([xmin, ymin, xmax, ymax, cls_name])
        return obj_infos

    def mkdir(self):
        if not os.path.exists(os.path.join(self.data_path, self.txt_folder_name)):
            os.makedirs(os.path.join(self.data_path, self.txt_folder_name))

    def save_txt(self):
        self.mkdir()

        for xmlname in self.xmllist:
            txt_name = xmlname.replace('xml', self.txt_ext)
            obj_infos = self.read_xml(xmlname)

            with open(os.path.join(self.data_path, self.txt_folder_name, txt_name), 'w') as f:
                for obj_info in obj_infos:
                    xmin, ymin, xmax, ymax, cls_name = obj_info[0], obj_info[1], obj_info[2], obj_info[3], obj_info[4]
                    # cls_name xmin ymin xmax ymax
                    line = str(cls_name) + ' ' + str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax) + '\n'
                    f.write(line)


if __name__ == '__main__':
    trans = xml2txt(data_path=r'/data/fzh/SAR-Ship-1.0/',
                    xml_folder_name='labelXml/',
                    txt_folder_name='labelTxt/')

    trans.save_txt()
    print(f'[Info]: txt file has created.')