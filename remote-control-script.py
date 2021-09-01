# Run a generator Box SOP Verb
node = hou.pwd()

geo = hou.Geometry()
temp = hou.Geometry()

# Remote Properties
remote_width = 1.5
button_height = 0.1

num_pad_offset = 0.3
app_buttons_offset = 1.8
menu_buttons_offset = 3
play_button_offset = 6


# small Button Properties
small_button_diameter = remote_width/9
small_button_radius = small_button_diameter/2


# Medium Button Properties
medium_button_diameter = remote_width/7
medium_button_radius = medium_button_diameter/2

# Large Button Properties
large_button_diameter = remote_width/6
large_button_radius = large_button_diameter/2


def create_box(t_tuple = (0,0,0), size_tuple = (1,1,1)):
    boxVerb = hou.sopNodeTypeCategory().nodeVerb("box")    
    boxVerb.setParms( { 
                't' : t_tuple,
                'size' : size_tuple
               } )
    boxVerb.execute(temp, [])
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

def create_tube(merge=True, t_tuple = (0,0,0), radscale=1, height=1, cap=True, group_name = None):
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

    if(merge):
        geo.merge(temp_tube)
    return temp_tube

def create_small_button(t_tuple = (0,0,0)):
    create_tube(
        t_tuple=t_tuple,
        radscale=small_button_radius,
        height=button_height
    )

def create_medium_button(t_tuple = (0,0,0)):
    create_tube(
        t_tuple=t_tuple,
        radscale=medium_button_radius,
        height=button_height
    )

def create_large_button(t_tuple = (0,0,0)):
    create_tube(
        t_tuple=t_tuple,
        radscale=large_button_radius,
        height=button_height
    )

def poly_extrude(dest):
    print("Poly Extrude") 
    scatter = hou.sopNodeTypeCategory().nodeVerb("scatter::2.0")
    
    
    buffer = hou.Geometry()
    
    scatter.setParms({ 
                'group': "large_circle_button"
               })

    scatter.execute(buffer, [dest])
    
    geo.merge(buffer)
    
    

def create_number_pad():
    z_index = 0
    x_index = 0
    button_space = (medium_button_diameter *2) 
    for i in range(1,13):
        x_index = x_index + button_space
        create_medium_button(
            t_tuple=(x_index, button_height/2, z_index)
        )
        if(i % 3 == 0):
            x_index = 0
            z_index = z_index + button_space

def create_circle_button():
    inner_circle_radius = .2
    outer_circle_radius = inner_circle_radius + .1

    create_tube(
        radscale=inner_circle_radius,
        height=button_height + .2
    )

    tube = create_tube(
        merge=False,
        radscale=outer_circle_radius,
        height=button_height,
        cap=False,
        group_name="large_circle_button"
    )

    poly_extrude(tube)

def create_menu_buttons():
    for i in range(1,4):
        create_large_button(
            t_tuple=(i, button_height/2, 3)
        )

    for i in range(1,4):
        create_large_button(
            t_tuple=(i, button_height/2, 5)
        )

    create_circle_button()

def create_play_buttons():
    z_index = play_button_offset
    x_index = 0
    button_space = (small_button_diameter *2) 
    for i in range(1,10):
        x_index = x_index + button_space
        create_small_button(
            t_tuple=(x_index, button_height/2, z_index)
        )
        if(i % 3 == 0):
            x_index = 0
            z_index = z_index + button_space

def create_app_buttons():
    big_box_button_length = (remote_width /2) - (remote_width/10)
    big_box_button_width = big_box_button_length/2

    small_box_button_length = (remote_width /5) - (remote_width/10)
    small_box_button_width = small_box_button_length/2

    for i in range(1,3):
        create_box(
            t_tuple=(i, 0, app_buttons_offset),
            size_tuple=(big_box_button_length, button_height, big_box_button_width)
        )

    small_buttons_offset = app_buttons_offset + big_box_button_width + .4
    for i in range(1,5):
        create_box(
            t_tuple=(i, 0, small_buttons_offset),
            size_tuple=(small_box_button_length, button_height, small_box_button_width)
        )

# create_number_pad()
create_menu_buttons()
# create_play_buttons()
# create_app_buttons()

printPointGroupNames(geo)

# Save results back to the node
node.geometry().clear()
node.geometry().merge(geo)

