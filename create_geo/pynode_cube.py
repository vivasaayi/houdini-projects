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
    first_point = positions[0]
    second_point = positions[1]
    third_point = positions[2]
    fourth_point = positions[3]
    
    return [first_point, fourth_point, third_point, second_point]


def create_face(positions):
    poly = geo.createPolygon()
    for position in positions:
        point = geo.createPoint()
        point.setPosition(position)
        poly.addVertex(point)
        
def translate(point_pos, axis, distance):
    updated_positions = []
    for p in point_pos:
        p_list = list(p)
        p_list[axis] = p_list[axis] + distance
        updated_positions.append(tuple(p_list))
    return  updated_positions
   
def simple_rotate_x_90(point_pos):
    third_point = point_pos[2]
    fourth_point = point_pos[3]
    
    third_point_list = list(third_point)
    fourth_point_list = list(fourth_point)
    
    # Change Y to 1
    third_point_list[1] = 1
    fourth_point_list[1] = 1
    
    # Change Z tp 0
    third_point_list[2] = 0
    fourth_point_list[2] = 0

    return [point_pos[0], point_pos[1], tuple(third_point_list), tuple(fourth_point_list)]

 
def simple_rotate_y_90(point_pos):
    second_point = point_pos[1]
    third_point = point_pos[2]
    
    second_point_list = list(second_point)
    third_point_list = list(third_point)
    
    # Change Y to 1
    second_point_list[1] = 1
    third_point_list[1] = 1
    
    # Change X tp 0
    second_point_list[0] = 0
    third_point_list[0] = 0

    return [point_pos[0], tuple(second_point_list), tuple(third_point_list), point_pos[3]]
 
#top_face
top_face = translate(point_positions, 1, 1)
bottom_face = reverse_face(point_positions)
back_face = simple_rotate_x_90(point_positions)
front_face = translate(reverse_face(back_face), 2, 1)
left_face = simple_rotate_y_90(point_positions)
right_face = translate(reverse_face(left_face), 0, 1)

create_face(bottom_face)
create_face(top_face)
create_face(back_face)
create_face(front_face)
create_face(left_face)
create_face(right_face)
