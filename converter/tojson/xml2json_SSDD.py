"""This script is used to convert SSDD xml(s) to json file."""


"""Json file content is following like this.
[ images: {'file_name': image_name, 'id': image_id, 'width': image_width, 'height': image_height},
  categories: {'id': 1, 'name': category_name},  # Note: the id is begin at 1 !
  annotations: {'bbox': [xmin, ymin, xmax, ymax], 'obj_width': obj_width, 'obj_height': obj_height,
                'area': obj_width * obj_height, 'iscrowd': 0, 'image_id': image_id,
                'category_id': category_id, 'id': obj_id}
]
"""
import xml.etree.ElementTree as ET
import os
import json
import cv2


class xml2json(object):
    def __init__(self, data_path, img_folder_name, xml_folder_name, json_folder_name, json_name):
        self.data_path = data_path
        self.img_folder_name = img_folder_name
        self.xml_folder_name = xml_folder_name
        self.json_name = json_name
        self.json_folder_name = json_folder_name
        self.img_ext = 'jpg'
        self.image_id = 0
        self.anno_id = 0
        self.data_coco = {}
        self.categories = []
        self.xmllist = os.listdir(os.path.join(self.data_path, self.xml_folder_name))
        self.get_categories()

    # find all categories in dataset
    def get_categories(self):
        for xmlfile in os.listdir(os.path.join(self.data_path, self.xml_folder_name)):
            infile = open(os.path.join(self.data_path, self.xml_folder_name, xmlfile))
            tree = ET.parse(infile)
            root = tree.getroot()

            # find all categories in dataset
            for obj in root.iter('object'):
                category = obj.find('name').text
                if category not in self.categories:
                    self.categories.append(category)

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
        if not os.path.exists(os.path.join(self.data_path, self.json_folder_name)):
            os.makedirs(os.path.join(self.data_path, self.json_folder_name))

    def images(self, img_name, height, width):
        single_image = {}
        single_image['file_name'] = img_name  # str
        single_image['id'] = self.image_id  # int
        self.image_id += 1
        single_image['width'] = width  # int
        single_image['height'] = height  # int
        return single_image

    def annotation(self, xmin, ymin, xmax, ymax, cls_name, img_id):
        single_obj = {}
        obj_width = xmax - xmin
        obj_height = ymax - ymin
        single_obj['bbox'] = [xmin, ymin, xmax, ymax]  # original is poly
        single_obj['obj_width'] = obj_width
        single_obj['obj_height'] = obj_height
        single_obj['area'] = obj_width * obj_height
        single_obj['iscrowd'] = 0
        single_obj['image_id'] = img_id
        single_obj['category_id'] = self.categories.index(cls_name) + 1
        single_obj['id'] = self.anno_id  # int
        self.anno_id += 1
        return single_obj

    def save_json(self):
        self.mkdir()
        data_coco = {}
        data_coco['images'] = []
        data_coco['categories'] = []
        data_coco['annotations'] = []
        for idx, name in enumerate(self.categories):
            single_category = {'id': idx + 1, 'name': name}
            data_coco['categories'].append(single_category)

        for xmlname in self.xmllist:
            img_name = xmlname.replace('xml', self.img_ext)
            height, width, c = cv2.imread(os.path.join(self.data_path, self.img_folder_name, img_name)).shape
            assert c == 3, 'Image channels in SSDD Dataset is not equal to 3 !'
            single_img = self.images(img_name, height, width)
            data_coco['images'].append(single_img)

            obj_infos = self.read_xml(xmlname)
            for obj_info in obj_infos:
                xmin, ymin, xmax, ymax = obj_info[0], obj_info[1], obj_info[2], obj_info[3]
                cls_name = obj_info[4]
                single_obj = self.annotation(xmin, ymin, xmax, ymax, cls_name, single_img['id'])
                data_coco['annotations'].append(single_obj)
        json.dump(data_coco, open(os.path.join(self.data_path, self.json_folder_name, self.json_name), 'w'), indent=4)


if __name__ == '__main__':
    trans = xml2json(data_path=r'/data/fzh/SSDD_data/',
                     img_folder_name='val/',
                     xml_folder_name='val_xml/',
                     json_folder_name='annotations',
                     json_name='instances_val.json'
    )
    print(f'[Info]: The Current dataset include categories: {trans.categories}.')
    trans.save_json()
    print(f'[Info]: json file has created.')
