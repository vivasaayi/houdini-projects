node = hou.pwd()
geo = node.geometry()

geo.clear()

point_positions = [
(0,0,0),
(1,0,0),
(1,0,1),
(0,0,1)
]

poly = geo.createPolygon()
for position in point_positions:
    point = geo.createPoint()
    point.setPosition(position)
    poly.addVertex(point)
