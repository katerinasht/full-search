def get_spn(corners):
    lowerCorner = corners['lowerCorner'].split()
    upperCorner = corners['upperCorner'].split()
    x = str(float(upperCorner[0]) - float(lowerCorner[0]))
    y = str(float(upperCorner[1]) - float(lowerCorner[1]))
    return [x, y]