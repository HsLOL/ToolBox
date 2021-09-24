from xml.dom.minidom import Document


def Another_writeXml(tmp, imgname, bboxes, hbb=True):
    category_set = ['Boeing737-800', 'Boeing787', 'A220', 'A320/321', 'A330', 'ARJ21', 'other']
    doc = Document()
    # owner
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    # owner
    # source
    source = doc.createElement('source')
    annotation.appendChild(source)

    filename = doc.createElement('filename')
    source.appendChild(filename)
    filename_txt = doc.createTextNode(imgname)
    filename.appendChild(filename_txt)

    origin = doc.createElement('origin')
    source.appendChild(origin)
    origin_txt = doc.createTextNode("GF3")
    origin.appendChild(origin_txt)

    #research#
    research = doc.createElement('research')
    annotation.appendChild(research)

    version = doc.createElement('version')
    research.appendChild(version)
    version_txt = doc.createTextNode("1.0")
    version.appendChild(version_txt)

    provider = doc.createElement('provider')
    research.appendChild(provider)
    provider_txt = doc.createTextNode("Company/School of team")
    provider.appendChild(provider_txt)

    author = doc.createElement('author')
    research.appendChild(author)
    author_txt = doc.createTextNode("kong tian shen ying")
    author.appendChild(author_txt)

    pluginname = doc.createElement('pluginname')
    research.appendChild(pluginname)
    pluginname_txt = doc.createTextNode("Airplane Detection and Recognition")
    pluginname.appendChild(pluginname_txt)

    pluginclass = doc.createElement('pluginclass')
    research.appendChild(pluginclass)
    pluginclass_txt = doc.createTextNode("Detection")
    pluginclass.appendChild(pluginclass_txt)

    time = doc.createElement('time')
    research.appendChild(time)
    time_txt = doc.createTextNode("2021-07-2021-11")
    time.appendChild(time_txt)

    objects = doc.createElement("objects")
    annotation.appendChild(objects)

    for bbox in bboxes:
        # threes#
        object_new = doc.createElement("object")
        objects.appendChild(object_new)

        coordinate = doc.createElement('coordinate')
        object_new.appendChild(coordinate)
        coordinate_txt = doc.createTextNode("pixel")
        coordinate.appendChild(coordinate_txt)

        type = doc.createElement('type')
        object_new.appendChild(type)
        type_txt = doc.createTextNode("rectangle")
        type.appendChild(type_txt)

        description = doc.createElement('description')
        object_new.appendChild(description)
        description_txt = doc.createTextNode("None")
        description.appendChild(description_txt)

        possibleresult = doc.createElement("possibleresult")
        object_new.appendChild(possibleresult)

        name = doc.createElement('name')
        possibleresult.appendChild(name)
        name_txt = doc.createTextNode(category_set[int(bbox[5])])
        name.appendChild(name_txt)

        probability = doc.createElement('probability')
        possibleresult.appendChild(probability)
        probability_txt = doc.createTextNode(str(float(bbox[4])))
        probability.appendChild(probability_txt)

        # threes-1#
        points = doc.createElement('points')
        object_new.appendChild(points)

        if hbb:
            point = doc.createElement('point')
            points.appendChild(point)
            point_txt = doc.createTextNode(str(float(bbox[0]))+','+str(float(bbox[1])))
            point.appendChild(point_txt)

            point = doc.createElement('point')
            points.appendChild(point)
            point_txt = doc.createTextNode(str(float(bbox[2]))+','+str(float(bbox[1])))
            point.appendChild(point_txt)

            point = doc.createElement('point')
            points.appendChild(point)
            point_txt = doc.createTextNode(str(float(bbox[2]))+','+str(float(bbox[3])))
            point.appendChild(point_txt)

            point = doc.createElement('point')
            points.appendChild(point)
            point_txt = doc.createTextNode(str(float(bbox[0]))+','+str(float(bbox[3])))
            point.appendChild(point_txt)

            point = doc.createElement('point')
            points.appendChild(point)
            point_txt = doc.createTextNode(str(float(bbox[0])) + ',' + str(float(bbox[1])))
            point.appendChild(point_txt)
        else:
            print('obb')

    xmlname = os.path.splitext(imgname)[0]
    tempfile = os.path.join(tmp, xmlname + '.xml')
    with open(tempfile, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return

