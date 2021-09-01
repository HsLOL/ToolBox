import torchvision
import cv2
import os
from lxml.etree import Element, SubElement, tostring


color_map = [[0, 0, 255], [0, 165, 255], [255, 0, 255],
             [139, 64, 39], [255, 111, 131], [255, 255, 0], [127,255, 0]]

classes = ['Boeing737-800', 'Boeing787', 'A220', 'A320/321', 'A330', 'ARJ21', 'other']


def write_in_xml(outpath, filepath, dets=None):
    # outpath: the save path of the output xml files
    # filepath: the name of the each xml file
    # dets: detection result [x1, y1, x2, y2, score, cls]

    # ------------------ fixed information -----------------------#
    filename = os.path.basename(filepath)
    node_root = Element('annotation')
    node_source = SubElement(node_root, 'source')

    node_filename = SubElement(node_source, 'filename')
    node_filename.text = filename
    node_origin = SubElement(node_source, 'origin')
    node_origin.text = 'GF3'

    node_research = SubElement(node_root, 'research')
    node_version = SubElement(node_research, 'version')
    node_version.text = '1.0'
    node_provider = SubElement(node_research, 'provider')
    node_provider.text = 'Company/School of team'
    node_author = SubElement(node_research, 'author')
    node_author.text = 'team name'
    node_pluginname = SubElement(node_research, 'pluginname')
    node_pluginname.text = 'Airplane Detection and Recognition'
    node_pluginclass = SubElement(node_research, 'pluginclass')
    node_pluginclass.text = 'Detection'
    node_time = SubElement(node_research, 'time')
    node_time.text = '2021-07-2021-11'
    # ---------------------- fixed information ------------------------#


    node_objects = SubElement(node_root, 'objects')
    for det in dets:
        single_det = []
        single_det[:5] = list(map(float, det[:5]))
        cls_idx = int(det[5])
        node_object = SubElement(node_objects, 'object')
        node_coordinate = SubElement(node_object, 'coordinate')
        node_coordinate.text = 'pixel'
        node_type = SubElement(node_objects, 'type')
        node_type.text = 'rectangle'
        node_description = SubElement(node_object, 'description')
        node_description.text = 'None'
        node_possibleresult = SubElement(node_object, 'possibleresult')
        node_object_name = SubElement(node_possibleresult, 'name')
        node_object_name.text = classes[cls_idx]
        node_object_probability = SubElement(node_possibleresult, 'probability')
        node_object_probability.text = str(single_det[4])
        node_object_points = SubElement(node_objects, 'points')

        # 4 points: left_up, right_up, right_bottom, left_bottom
        node_object_point = SubElement(node_object_points, 'point')
        node_object_point.text = str(single_det[0]) + ',' + str(single_det[1])

        node_object_point = SubElement(node_object_points, 'point')
        node_object_point.text = str(single_det[2]) + ',' + str(single_det[1])

        node_object_point = SubElement(node_object_points, 'point')
        node_object_point.text = str(single_det[2]) + ',' + str(single_det[3])

        node_object_point = SubElement(node_object_points, 'point')
        node_object_point.text = str(single_det[0]) + ',' + str(single_det[3])

    xml = tostring(node_root, pretty_print=True)
    xmlpath = os.path.join(outpath, filename.replace('tif', 'xml'))
    with open(xmlpath, 'wb') as f:
        f.write(xml)
