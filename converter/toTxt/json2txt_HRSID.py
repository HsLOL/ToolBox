"""This script is used to convert json file to txt file for HRSID dataset."""
import json
import os


class Json2txt(object):
    def __init__(self, data_path, json_folder_name, txt_folder_name, set_name):
        self.data_path = data_path
        self.set_name = set_name
        self.json_folder_name = json_folder_name
        self.txt_folder_name = txt_folder_name
        self.json_file = f'{set_name}.json'
        self.json_dict = self._readjson()
        self.categories = self._categories()
        self.images = self._images()
        self.annotations = self._annotations()

    def _categories(self):
        cat_dict = {}
        for single_category in self.json_dict['categories']:
            id = single_category['id']
            name = single_category['name']
            cat_dict[id] = name
        return cat_dict

    def _images(self):
        image_dict = {}
        for single_image in self.json_dict['images']:
            file_name = single_image['file_name']
            id = single_image['id']
            image_dict[id] = file_name
        return image_dict

    def _annotations(self):
        anno_dict = {}
        start = 0
        for idx in range(len(self.images)):
            image_name = self.images[idx]
            annotation_list = []
            for single_annotation in self.json_dict['annotations'][start:]:
                image_id = single_annotation['image_id']
                if image_id == idx:
                    start += 1
                    cat = self.categories.get(single_annotation['category_id'])
                    bbox = single_annotation['bbox']
                    bbox = list(map(int, bbox))
                    xmin = bbox[0]
                    ymin = bbox[1]
                    xmax = bbox[0] + bbox[2]
                    ymax = bbox[1] + bbox[3]

                    # cls_name xmin ymin xmax ymax
                    line = cat + ' ' + str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax)
                    annotation_list.append(line)
                else:
                    break
            anno_dict[image_name] = annotation_list
        return anno_dict

    def _readjson(self):
        json_file = os.path.join(self.data_path, self.json_folder_name, self.json_file)
        with open(json_file, 'r') as f:
            json_dict = json.load(f)
        return json_dict

    def _makedir(self):
        if not os.path.exists(os.path.join(self.data_path, self.txt_folder_name)):
            os.makedirs(os.path.join(self.data_path, self.txt_folder_name))

    def savetxt(self):
        self._makedir()
        for imageidx in self.images:
            image_name = self.images[imageidx]
            image_annot = self.annotations[image_name]
            with open(os.path.join(self.data_path, self.txt_folder_name, image_name.replace('jpg', 'txt')), 'w') as f:
                for single_annot in image_annot:
                    f.write(single_annot + '\n')
        print(f'[Info]: {self.set_name} set txt files have created.')


if __name__ == '__main__':
    op = Json2txt(data_path='/home/fzh/Data/HRSID/',
                  json_folder_name='inshore_offshore/',
                  txt_folder_name='offshore-ground-truth/',
                  set_name='offshore')
    op.savetxt()
