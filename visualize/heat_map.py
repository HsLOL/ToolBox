# coding=utf-8
#
# 用CAM可视化指定某一层的特征图
#
# 实现流程
# 1. 用register_forward_hook获取指定层的输出特征(feature map)
# 2. 对输入的图片进行输入网络前的预处理，并喂入网络进行前向传播，用hook获取相应的输出特征图
# 3. 得到多通道特征图 1) 可以只可视化单个通道的特征，2) 也可以将得到的特征图按通道的维度进行相加，可视化所有通道
# 4. 对单个通道特征图 或 按维度相加后的特征图进行归一化处理
# 5. 进行 * 255 和 np.unit8()的运算
# 6. 最后应用cv2.ColorMap()获得热力图，并与原始图像进行叠加

from models.model import RetinaNet
import torch
from torchvision import transforms
import cv2
import numpy as np
from config import cfg
import matplotlib.pyplot as plt
import argparse
import os
from detect import im_detect


def hook_fn(module, inputs, outputs):
    p_in.append(inputs)
    p_out.append(outputs)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--backbone', type=str, default='resnet50')
    parser.add_argument('--device', type=int, default=2)
    parser.add_argument('--weight_file', type=str, default='120_28072.pth')
    parser.add_argument('--target_sizes', type=int, default=800)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    model = RetinaNet(backbone=args.backbone, loss_func=cfg.loss_func, pretrained=False)
    checkpoint = os.path.join(cfg.output_path, 'checkpoints', args.weight_file)

    # from checkpoint load model weight file
    # model weight
    chkpt = torch.load(checkpoint, map_location='cpu')
    pth = chkpt['model']
    model.load_state_dict(pth)
    model.cuda(device=args.device)
    # ------------------------------------------------------------------------------------------------------------------

    # Step 2 获取想要某一层的输入和输出特征图(实际只用输出)
    p_in = []  # 指定层的输入特征图
    p_out = []  # 指定层的输出特征图

    # 将hook挂上
    # model.cls_branch.register_forward_hook(hook_fn)  # Maybe the best to cls CAM
    # model.reg_branch.register_forward_hook(hook_fn)
    model.reg_head.head.register_forward_hook(hook_fn)  # Maybe the best to reg CAM
    # model.cls_head.head.register_forward_hook(hook_fn)

    img_path = r'heatmap_results/original/000399.jpg'

    image = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    img_h, img_w, img_c = image.shape
    ori_img = image.copy()

    model.eval()
    with torch.no_grad():
        dets = im_detect(model,
                         image,
                         target_sizes=args.target_sizes,
                         use_gpu=True,
                         conf=cfg.score_thr,
                         device=args.device)
    # ------------------------------------------------------------------------------------------------------------------
    for index in range(len(p_out)):
        featuremap_list = p_out[index]  # cls_branch([P3', P4', P5', P6', P7'])
        # featuremap = featuremap_list[0]  # 选取BiFPN中的某一输出特征图 0 - P3 1 - P4 2 - P5 3 - P6 4 - P7
        featuremap = featuremap_list
        print(featuremap.shape)

        featuremap = featuremap.squeeze(0)  # (batch_size, channel, H, W) ---> (channel, H, W)
        channel_num, H, W = featuremap.size()[0], featuremap.size()[1], featuremap.size()[2]

        channel_map = featuremap[0, :, :]  # 取出第一个通道的特征图
        channel_map = channel_map.cpu().numpy()
        # cv2.imwrite('first.jpg', channel_map)
        # row_num = 8
        # for index in range(1, 24):  # 通过遍历的方式，将64个通道的tensor拿出
        #     plt.subplot(row_num, row_num, index)  # 绘制子图的个数
        #     # plt.imshow(feature_map[index - 1], cmap='gray')#feature_map[0].shape=torch.Size([55, 55])
        #     # 将上行代码替换成，可显示彩色
        #     plt.imshow(transforms.ToPILImage()(temp1[index, :, :]))  # feature_map[0].shape=torch.Size([55, 55])
        #     plt.axis('off')
        #     # plt.savefig('feature_map_save//'+str(index) + ".png", feature_map[index - 1])
        # plt.savefig('all.jpg')
        # plt.show()

        for idx in range(1, channel_num):
            channel_map = channel_map + featuremap[idx, :, :].cpu().numpy()  # shape(64, 64)
        channel_map = np.maximum(channel_map, 0)
        min_v = np.min(channel_map)
        max_v = np.max(channel_map)

        # 对两种归一化方式均进行了可视化，感觉效果差不多
        channel_map = (channel_map - min_v) / (max_v - min_v)  # 第一种归一化方法
        # channel_map = (channel_map - min_v) / max_v  # 第二种归一化方法

        # 若想要使用cv2.applyColorMap()，必须进行 *255 和 np.uint8()的操作
        heat_map = np.uint8(cv2.resize(channel_map, (img_w, img_h)) * 255)
        # cv2.imwrite('gray.jpg', heat_map)

        heat_mapp = cv2.applyColorMap(heat_map, cv2.COLORMAP_JET)
        res = cv2.addWeighted(ori_img, 0.5, heat_mapp, 0.5, 0)
        cv2.imwrite(f'res_{index}.jpg', res)
