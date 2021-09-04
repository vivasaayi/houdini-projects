node = hou.pwd()
geo = node.geometry()

geo.clear()

rows = 30
columns = 30
radius = 1.0
rows_angle = 180.0/rows
cols_angle = 180.0/columns

points = []
    
division_length = radius/columns
    
print(division_length)
print(rows_angle)

y_start = hou.Vector3(0, 1, 0)
row_array = []

for row in range(1, rows):
    rotation = hou.hmath.buildRotate(0, 0, -(rows_angle * row))
    row_array.append(y_start * rotation)
    
points.append(row_array)
    
for col in range(0, (columns *2) - 1):
    rotated_row_array = []
    rot_angle = (cols_angle * (col +1))
    for row in range(0, rows-1):
        p = row_array[row]
        rotation = hou.hmath.buildRotate(0, rot_angle, 0)
        rotated = p * rotation
        rotated_row_array.append(rotated)
        continue
        
    points.append(rotated_row_array)
    

    
#print("Points Length", len(points), len(row_array))
#for i in range(0, len(points)):
#    poly = geo.createPolygon()
#    arr = points[i]
#    print(len(arr), "\n\n,")
#    for j in range(0, len(arr)):
#        point = geo.createPoint()
#        point.setPosition(arr[j])
#        continue
        
        

topPoint = geo.createPoint()
topPoint.setPosition((0,1,0))

bottomPoint = geo.createPoint()
bottomPoint.setPosition((0,-1,0))

print("Points Length", len(points), len(row_array))
for i in range(0, len(points)):
    first_col = points[i]
    second_col_inx = i+1
    
    if (i+1 == len(points)):
         second_col_inx =0
        
    second_col = points[second_col_inx]
    
    top_tri_poly = geo.createPolygon()
    tt_p1 = topPoint
    tt_p2 = geo.createPoint()
    tt_p2.setPosition(first_col[0])
    tt_p3 = geo.createPoint()
    tt_p3.setPosition(second_col[0])
    
    top_tri_poly.addVertex(tt_p1)
    top_tri_poly.addVertex(tt_p3)
    top_tri_poly.addVertex(tt_p2)
    
    bottom_tri_poly = geo.createPolygon()
    tt_p1 = bottomPoint
    tt_p2 = geo.createPoint()
    tt_p2.setPosition(first_col[len(first_col) -1])
    tt_p3 = geo.createPoint()
    tt_p3.setPosition(second_col[len(second_col) -1])
    
    bottom_tri_poly.addVertex(tt_p1)
    bottom_tri_poly.addVertex(tt_p2)
    bottom_tri_poly.addVertex(tt_p3)
    
    for ix in range(0, len(first_col) -1):
        poly = geo.createPolygon()
        p1 = first_col[ix]
        p2 = second_col[ix]
        p3 = second_col[ix + 1]
        p4 = first_col[ix + 1]
        point1 = geo.createPoint()
        point2 = geo.createPoint()
        point3 = geo.createPoint()
        point4 = geo.createPoint()
        #print(point)
        point1.setPosition(p1)
        point2.setPosition(p2)
        point3.setPosition(p3)
        point4.setPosition(p4)
        poly.addVertex(point1)
        poly.addVertex(point2)
        poly.addVertex(point3)
        poly.addVertex(point4)
        continue
        
        
