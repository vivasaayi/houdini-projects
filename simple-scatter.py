import os

os.environ['HOUDINI_SCRIPT_LICENSE'] = 'hescape'

import hou

print("Welcome to Python Programming")

try:
    hou.hipFile.load("test.hipnc")
except hou.LoadWarning as e:
    print(e)

hou.hipFile.clear()

geo = hou.node("/obj").createNode("geo")

box1 = geo.createNode("box")
box2 = geo.createNode("box")

box2.parm("sizex").set(2)
box2.parm("sizey").set(2)
box2.parm("sizey").set(2)

box2.parmTuple("size").set((1.5, 1.5, 1.5))


box2.parm("tx").set(1.5)

box1Color = geo.createNode("color")
box1Color.parmTuple("color").set((0, 1, 0))
box1Color.setInput(0, box1)

box2Color = geo.createNode("color")
box2Color.parmTuple("color").set((0, 0, 1))
box2Color.setInput(0, box2)

mergeNode = geo.createNode("merge")
mergeNode.setInput(0, box1Color)
mergeNode.setInput(1, box2Color)
mergeNode.setDisplayFlag(True)

grid = geo.createNode("grid")
grid.parm("type").set("poly")

sphere = geo.createNode("sphere")
sphere.parm("type").set("poly")
sphere.parm("scale").set(0.1)

scatter = geo.createNode("scatter")
scatter.parm("seed").set(6)
scatter.setInput(0, grid)

copyToPoints1 = geo.createNode("copytopoints")
copyToPoints1.setInput(0, sphere)
copyToPoints1.setInput(1, scatter)
copyToPoints1.setDisplayFlag(True)

geo.layoutChildren()

hou.hipFile.save("modified-scatter.hipnc")
