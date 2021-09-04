node = hou.pwd()
geo = node.geometry()

geo.clear()

input_geo = node.inputs()[0].geometry()
points = node.inputs()[1].geometry().points()

for p in points:
    copy_geo = input_geo.freeze()
    p_pos = p.position()
    translate = hou.hmath.buildTranslate(p_pos[0], p_pos[1], p_pos[2])
    copy_geo.transform(translate)
    geo.merge(copy_geo)

    