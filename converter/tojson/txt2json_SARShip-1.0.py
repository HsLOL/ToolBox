"""This script is used to convert txt file to json file for SAR Ship-1.0 Dataset."""

import os
import json
import cv2


class txt2json(object):
    def __init__(self, root_path, img_folder_name, txt_folder_name, json_folder_name, json_name):
        self.root_path = root_path
        self.img_folder_name = img_folder_name
        self.txt_folder_name = txt_folder_name
        self.json_folder_name = json_folder_name
        self.json_name = json_name
        self.img_ext = 'tif'
        self.image_id = 0
        self.anno_id = 0
        self.txtlist = os.listdir(os.path.join(self.root_path, self.txt_folder_name))
        self.categories = []
        self._categories()

    def mkdir(self):
        if not os.path.exists(os.path.join(self.root_path, self.json_folder_name)):
            os.makedirs(os.path.join(self.root_path, self.json_folder_name))

    def _categories(self):
        for txtfile in self.txtlist:
            file = open(os.path.join(self.root_path, self.txt_folder_name, txtfile), 'r')
            for line in file:
                line = line.split(' ')
                obj = line[8]
                if obj not in self.categories:
                    self.categories.append(obj)

    def _readtxt(self, txtname):
        obj_infos = []  # list[list[xmin, ymin, xmax, ymax, cls_name], ...[]]
        txt_content = open(os.path.join(self.root_path, self.txt_folder_name, txtname), 'r')
        for line in txt_content:
            line = line.split(' ')
            xmin = int(float(line[0]))
            ymin = int(float(line[1]))
            xmax = int(float(line[4]))
            ymax = int(float(line[5]))
            cls_name = line[8]
            obj_infos.append([xmin, ymin, xmax, ymax, cls_name])
        return obj_infos

    def _images(self, img_name, height, width):
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

        for txtname in self.txtlist:
            img_name = txtname.replace('txt', self.img_ext)
            height, width, c = cv2.imread(os.path.join(self.root_path, self.img_folder_name, img_name)).shape
            assert c == 3, 'Image channels in SSDD Dataset is not equal to 3 !'
            assert height == 512 and width == 512, f'{img_name} has wrong height or width.'
            single_img = self._images(img_name, height, width)
            data_coco['images'].append(single_img)
            obj_infos = self._readtxt(txtname)
            for obj_info in obj_infos:
                xmin, ymin, xmax, ymax = obj_info[0], obj_info[1], obj_info[2], obj_info[3]
                cls_name = obj_info[4]
                single_obj = self.annotation(xmin, ymin, xmax, ymax, cls_name, single_img['id'])
                data_coco['annotations'].append(single_obj)
        json.dump(data_coco, open(os.path.join(self.root_path, self.json_folder_name, self.json_name), 'w'), indent=4)


if __name__ == '__main__':
    trans = txt2json(root_path=r'/home/fzh/Data/SAR-Ship-1.0/manual/',
                     img_folder_name='trainImages/',
                     txt_folder_name='trainTxt/',
                     json_folder_name='annotations',
                     json_name='instances_train.json'
    )
    print(f'[Info]: The Current dataset include categories: {trans.categories}.')
    trans.save_json()
    print(f'[Info]: json file has created.')