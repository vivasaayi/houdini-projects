# Run a generator Box SOP Verb
node = hou.pwd()

geo = hou.Geometry()

temp = hou.Geometry()

# Remote Properties
remote_width = 1.5
remote_length = 8
remote_height=0.3

remote_x_origin = 0
remote_y_origin = -remote_height/2
remote_z_origin = remote_length/2
remote_margin = .05
remote_actual_space = remote_width - (2*remote_margin)

button_height = 0.1
color_attribute_added = False

# small Button Properties
small_button_diameter = remote_width/9
small_button_radius = small_button_diameter/2


# Medium Button Properties
medium_button_diameter = remote_actual_space/6
medium_button_radius = medium_button_diameter/2
medium_button_space = (medium_button_diameter * 2) 

# Large Button Properties
large_button_diameter = remote_width/6
large_button_radius = large_button_diameter/2


num_pad_offset = 0
num_pad_length = (medium_button_diameter * 4) + (medium_button_space * 3)
num_pad_z_center = (num_pad_length/2) + num_pad_offset
num_pad_z_top_left = num_pad_z_center - (num_pad_length/2)

# 3 buttons + space between them
num_pad_width = (medium_button_diameter * 3) + (medium_button_space * 2)
num_pad_x_center = 0
num_pad_x_top_left = num_pad_x_center - (num_pad_width/2) 

app_buttons_offset = num_pad_offset + num_pad_length
app_big_button_x_space = .1
app_big_button_z_space = .1
app_big_buttonpad_x_spaces = (4 * app_big_button_x_space)
app_big_button_width = (remote_actual_space - app_big_buttonpad_x_spaces)/2
app_big_buttonpad_z_spaces = (2 * app_big_button_z_space)
app_big_button_length = .3
app_buttons_x_center = 0
app_big_buttons_y_center = app_buttons_offset + (app_big_button_length/2)

app_small_button_x_space = .1
app_small_button_x_spaces = 8 * app_small_button_x_space
app_small_buttons_width = (remote_actual_space - app_small_button_x_spaces)/4
app_small_buttons_length = .1

app_button_pad_width = (remote_actual_space - app_big_button_x_space)

menu_buttons_offset = 2.5
menu_buttons_start_x = menu_buttons_offset

inner_circle_radius = (remote_actual_space - .2)/6
outer_circle_radius = (remote_actual_space - .2)/2

menu_buttons_offset = 4

play_button_offset = 5.5
play_buttons_start_x = play_button_offset

def create_box(t_tuple = (0,0,0), size_tuple = (1,1,1), group_name = None, color=None):
    boxVerb = hou.sopNodeTypeCategory().nodeVerb("box")    
    boxVerb.setParms( { 
                't' : t_tuple,
                'size' : size_tuple
               } )
    boxVerb.execute(temp, [])

    # ToDo: Refactor - should be common for all geometries
    if(group_name is not None):
        group_geo(temp, group_name)

    if(color is not None):
        color_attribute = temp.addAttrib(hou.attribType.Point, "color", 0)
        points = temp.points()
        for p in points:
            p.setAttribValue(color_attribute, color)

    geo.merge(temp)

def printPointGroupNames(geometry):
    for group in geometry.pointGroups():
        print(group.name())

def group_geo(geo, group_name):
    points = geo.points()
    group = geo.createPointGroup(group_name)
    group.add(points)

    prim_group = geo.createPrimGroup(group_name)
    prims = geo.prims()
    prim_group.add(prims)

def create_tube(merge=True, t_tuple = (0,0,0), radscale=1, height=1, cap=True, 
    group_name = None, color=None):
    global color_attribute_added
    temp_tube = hou.Geometry()
    tubeVerb = hou.sopNodeTypeCategory().nodeVerb("tube")
    tubeVerb.setParms( { 
                'type': 1,
                't' : t_tuple,
                'radscale': radscale,
                'height': height,
                'cap': cap,
               } )
    tubeVerb.execute(temp_tube, [])

    if(group_name is not None):
        group_geo(temp_tube, group_name)

    if(color is not None):
        color_attribute = temp_tube.addAttrib(hou.attribType.Point, "color", 0)
        points = temp_tube.points()
        for p in points:
            p.setAttribValue(color_attribute, color)

    if(merge):
        geo.merge(temp_tube)
    return temp_tube

def create_small_button(t_tuple = (0,0,0), group_name="small_button", color=None):
    create_tube(
        color=color,
        group_name=group_name,
        t_tuple=t_tuple,
        radscale=small_button_radius,
        height=button_height
    )

def create_medium_button(t_tuple = (0,0,0), group_name="medium_button", color=None):
    create_tube(
        color=color,
        group_name=group_name,
        t_tuple=t_tuple,
        radscale=medium_button_radius,
        height=button_height
    )

def create_large_button(t_tuple = (0,0,0), group_name="large_button", color=None):
    create_tube(
        color=color,
        group_name=group_name,
        t_tuple=t_tuple,
        radscale=large_button_radius,
        height=button_height
    )

def boolean(source, modifier):
    boolean_verb = hou.sopNodeTypeCategory().nodeVerb("boolean::2.0")
    buffer = hou.Geometry()
    boolean_verb.setParms({ 
                    "booleanop": 2
               })
    boolean_verb.execute(buffer, [source, modifier])
    geo.merge(buffer)


def scatter(dest):
    scatter = hou.sopNodeTypeCategory().nodeVerb("scatter::2.0")
    buffer = hou.Geometry()
    scatter.setParms({ 
                'group': "large_circle_button"
               })
    scatter.execute(buffer, [dest])
    geo.merge(buffer)
    
def create_number_pad():
    group_name = "numpad"
    color = 1

    # create_box(
    #     color=color,
    #     group_name=group_name,
    #     t_tuple=(0, 0, num_pad_z_center),
    #     size_tuple=(num_pad_width, 0, num_pad_length)
    # )

    x_button_space = num_pad_width/4
    z_button_space = num_pad_length/5

    x_index = num_pad_x_top_left + x_button_space
    z_index = num_pad_z_top_left + z_button_space

    for i in range(1,13):
        create_medium_button(
            color=color,
            group_name=group_name,
            t_tuple=(x_index, button_height/2, z_index)
        )

        x_index = x_index + x_button_space

        if(i % 3 == 0):
            x_index = num_pad_x_top_left + x_button_space
            z_index = z_index + z_button_space

def create_circle_button():
    color=5
    group_name="large_circle_button"

    create_tube(
        t_tuple=(0, 0, menu_buttons_offset),
        color=color,
        group_name=group_name,
        radscale=inner_circle_radius,
        height=button_height
    )

    modifier_circle = create_tube(
        t_tuple=(0, 0, menu_buttons_offset),
        color=color,
        group_name=group_name,
        merge=False,
        radscale=inner_circle_radius + .1,
        height=button_height + .2
    )

    outer_circle = create_tube(
        t_tuple=(0, 0, menu_buttons_offset),
        color=color,
        merge=False,
        radscale=outer_circle_radius,
        height=button_height,
        group_name=group_name
    )

    boolean(outer_circle, modifier_circle)
    
def create_menu_buttons():
    group_name = "menu"
    color = 4
    circle_radius = outer_circle_radius + large_button_radius + .1
    
    for i in range(1,4):
        t_v = hou.Vector3(circle_radius, button_height/2, 0)
        rotation_matrix = hou.hmath.buildRotate(0, 45 * i, 0)
        t_tuple = t_v * rotation_matrix
        t_tuple[2] = t_tuple[2] + menu_buttons_offset
        create_large_button(
            color=color,
            group_name=group_name,
            t_tuple=t_tuple
        )

    for i in range(1,4):
        t_v = hou.Vector3(circle_radius, button_height/2, 0)
        rotation_matrix = hou.hmath.buildRotate(0, -45 * i, 0)
        t_tuple = t_v * rotation_matrix
        t_tuple[2] = t_tuple[2] + menu_buttons_offset
        create_large_button(
            color=color,
            group_name=group_name,
            t_tuple=t_tuple
        )

    create_circle_button()

def create_play_buttons():
    group_name = "playbuttons"
    color = 2
    z_index = play_button_offset
    x_index = (-num_pad_width/2) + small_button_diameter
    button_space = (small_button_diameter *2) 
    
    for i in range(1,10):
        x_index = x_index + button_space
        create_small_button(
            group_name=group_name,
            color=color,
            t_tuple=(x_index, button_height/2, z_index)
        )
        if(i % 3 == 0):
            x_index = (-num_pad_width/2) + small_button_diameter
            z_index = z_index + button_space

def create_app_buttons():
    color=230
    group_name="appbuttons"

    big_button_x_division = app_button_pad_width/4
    x_index = app_buttons_x_center - big_button_x_division

    for i in range(1,3):
        create_box(
            color=color,
            group_name=group_name,
            t_tuple=(x_index, 0, app_big_buttons_y_center),
            size_tuple=(app_big_button_width, button_height, app_big_button_length)
        )
        x_index = x_index + (2*big_button_x_division) 


    small_button_x_division = app_button_pad_width/8
    x_index = app_buttons_x_center - (3 * small_button_x_division)

    for i in range(1,5):
        create_box(
            color=color,
            group_name=group_name,
            t_tuple=(x_index, 0, app_big_buttons_y_center + .3),
            size_tuple=(app_small_buttons_width, button_height, app_small_buttons_length)
        )
        x_index = x_index + (2 * small_button_x_division) 

def create_remote():
    color=78
    group_name="remote"
    create_box(
        color=color,
        group_name=group_name,
        t_tuple=(remote_x_origin,remote_y_origin,remote_z_origin),
        size_tuple=(remote_width, remote_height, remote_length)
    )

create_remote()
create_number_pad()
create_app_buttons()
create_menu_buttons()
create_play_buttons()

printPointGroupNames(geo)

# Save results back to the node
node.geometry().clear()
node.geometry().merge(geo)

