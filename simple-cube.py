import os
os.environ['HOUDINI_SCRIPT_LICENSE'] = 'hescape'

import hou

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
mergeNode.setRenderFlag(True)

cam = hou.node("/obj").createNode("cam")
cam.parmTuple("t").set((0, 5, 4))
cam.parmTuple("r").set((-45, 0, 0))

geo.layoutChildren()
hou.node("/obj").layoutChildren()

mantra = hou.node("/out").createNode("ifd")
mantra.parm("vm_picture").set("/Users/rajanp/work/houdini/simple-cube.jpg")
mantra.render()

hou.hipFile.save("simple-cube.hipnc")
