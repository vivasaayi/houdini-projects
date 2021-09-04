node = hou.pwd()
geo = node.geometry()

geo.clear()

num_cols=3.0
num_rows=4.0

grid_width = 5.0
grid_col_width = grid_width/num_cols

grid_length = 5.0
grid_row_width = grid_length/num_rows

xpos = 0
zpos = 0

for i in range(0, 6):
    zpos = 0
    for j in range(0, 6):
        zpos = zpos + grid_row_width
        point = geo.createPoint()
        point.setPosition((xpos, 0, zpos))
        
    print(grid_col_width, "",)
    xpos = xpos + grid_col_width
