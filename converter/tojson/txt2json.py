import os
import json
import cv2


class txt2json(object):
    def __init__(self, txt_in_path, img_path, json_out_path, json_name):
        self.categories = ['Boeing737-800', 'Boeing787', 'A220', 'A320/321', 'A330', 'ARJ21', 'other']
        self.txt_in_path = txt_in_path
        self.txt_list = os.listdir(txt_in_path)
        self.img_path = img_path
        self.json_path = json_out_path
        self.img_ext = 'tif'
        self.image_id = 0
        self.anno_id = 0
        self.data_coco = {}
        self.output_json_name = json_name

    def mkdir(self):
        if not os.path.exists(self.json_path):
            os.mkdir(self.json_path)

    def images(self, img_name, height, width):
        single_image = {}
        single_image['file_name'] = img_name
        single_image['id'] = self.image_id
        self.image_id += 1
        single_image['width'] = width
        single_image['height'] = height
        return single_image

    def annotation(self, xmin, ymin, xmax, ymax, cls_name, img_id):
        single_obj = {}
        obj_width = xmax - xmin
        obj_height = ymax - ymin
        single_obj['poly'] = [xmin, ymin, xmax, ymax]
        single_obj['obj_widht'] = obj_width
        single_obj['obj_height'] = obj_height
        single_obj['iscrowd'] = 0
        single_obj['image_id'] = img_id
        single_obj['category_id'] = self.categories.index(cls_name) + 1
        single_obj['id'] = self.anno_id
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

        for txt in self.txt_list:
            img_name = txt.replace('txt', self.img_ext)
            height, width, _ = cv2.imread(os.path.join(self.img_path, img_name)).shape
            single_img = self.images(img_name, height, width)
            data_coco['images'].append(single_img)
            txt_file = open(os.path.join(self.txt_in_path, txt), 'r')
            for line in txt_file:
                line = line.split(' ')
                line[:8] = map(float, line[:8])
                xmin, ymin, xmax, ymax = line[0], line[1], line[4], line[5]
                cls_name = line[8]
                single_obj = self.annotation(xmin, ymin, xmax, ymax, cls_name, single_img['id'])
                data_coco['annotations'].append(single_obj)
        json.dump(data_coco, open(os.path.join(self.json_path, self.output_json_name), 'w'), indent=4)


if __name__ == '__main__':
    trans = txt2json(
        txt_in_path=r'/home/fzh/Compete/TrainData/splitTrainData/valid_labelTxt/',  # input txt path
        img_path=r'/home/fzh/Compete/TrainData/splitTrainData/valid_images/',       # reference image path
        json_out_path=r'/home/fzh/Compete/TrainData/splitTrainData/annotations',    # the save path of the json file
        json_name='train.json'  # the file name of the output json file
    )
    trans.save_json()



