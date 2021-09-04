node = hou.pwd()
geo = node.geometry()

geo.clear()

point_positions = [
(0,0,0),
(1,0,0),
(1,0,1),
(0,0,1)
]

def reverse_face(positions):
    second_point = positions[1]
    fourth_point = positions[3]
    
    positions[1] = fourth_point
    positions[3] = second_point
    return positions


poly = geo.createPolygon()

for position in reverse_face(point_positions):
    point = geo.createPoint()
    point.setPosition(position)
    poly.addVertex(point)

