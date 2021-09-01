# coding=utf-8

import cv2
import os

# opencv B-G-R
color_map = [[0, 0, 255], [0, 165, 255], [255, 0, 255],
             [139, 64, 39], [255, 111, 131], [255, 255, 0], [127,255, 0]]

diff_color = [255, 255, 255]


def draw_box(poly, image, clsname, color, diff, imgsavepath, imgname, showdiff=True):
    imgname = imgname.replace('tif', 'png')
    for idx in range(len(poly)):
        difficult = diff[idx]
        if showdiff and difficult == '2':
            single_color = diff_color
        elif showdiff and difficult != '2':
            single_color = color[idx]
        else:
            continue
        single = poly[idx]
        single_name = clsname[idx]
        cv2.rectangle(img=image, pt1=(single[0], single[1]), pt2=(single[4], single[5]), color=single_color, thickness=2)
        cv2.putText(image, single_name, (single[0]+10, single[1]+10), cv2.FONT_HERSHEY_COMPLEX, 0.5, color=single_color)
    cv2.imwrite(os.path.join(imgsavepath, imgname), image)


def visualize_gt(txtpath, imgpath, imgsavepath, classes, issplit=True):
    imglist = os.listdir(imgpath)
    invalid_txt = []
    for image_id in imglist:
    # for idx in range(2):
    #     image_id = imglist[idx]
    #     print(image_id)
        txtfile = open(os.path.join(txtpath, image_id.replace('tif', 'txt')), 'r')
        poly_list_per_image = []
        clsname_list_per_image = []
        color_list_per_image = []
        difficult_list_per_image = []
        image = cv2.imread(os.path.join(imgpath, image_id))
        for line in txtfile:
            line = line.split(' ')
            if issplit is False and (len(line) == 1 or len(line) == 4):
                continue
            difficult = line[9].split('\n')[0]
            difficult_list_per_image.append(difficult)
            clsname = line[8]
            clsname_list_per_image.append(clsname)
            color = color_map[classes.index(clsname)]
            color_list_per_image.append(color)
            poly = list(map(float, line[:8]))  # str -> float -> int
            poly = list(map(int, poly[:]))
            poly_list_per_image.append(poly)  # poly = []

        if len(poly_list_per_image) == 0:
            invalid_txt.append(image_id)
            continue
        draw_box(poly_list_per_image, image, clsname=clsname_list_per_image, color=color_list_per_image, diff=difficult_list_per_image, imgsavepath=imgsavepath, imgname=image_id)


if __name__ == '__main__':
    classes = ['Boeing737-800', 'Boeing787', 'A220', 'A320/321', 'A330', 'ARJ21', 'other']

    # # check split result
    visualize_gt(txtpath=r'/home/fzh/Compete/ValData/splitValData/labelTxt/',
                 imgpath=r'/home/fzh/Compete/ValData/splitValData/images/',
                 imgsavepath=r'/home/fzh/Compete/ValData/splitValData/drawgt/',
                 classes=classes,
                 issplit=True)

    # # original result
    # visualize_gt(txtpath=r'/home/fzh/Compete/TrainData/labelTxt/',
    #              imgpath=r'/home/fzh/Compete/TrainData/images/',
    #              imgsavepath=r'/home/fzh/Compete/TrainData/drawgt/',
    #              classes=classes,
    #              issplit=False)

