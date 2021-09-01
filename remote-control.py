import os

os.environ['HOUDINI_SCRIPT_LICENSE'] = 'hescape'

import hou

def get_file_content(file_name):
    f = open(file_name, "r")
    data = f.read()
    f.close()
    return data

python_script = get_file_content("./remote-control-script.py")

hou.hipFile.clear()

geo = hou.node("/obj").createNode("geo")

nullObj = geo.createNode("null")
pyObj = geo.createNode("python")
colorObj = geo.createNode("color")

colorObj.setInput(0, pyObj)
nullObj.setInput(0, colorObj)

pyObj.parm("python").set(python_script)

colorObj.parm("colortype").set(5)
colorObj.parm("rampattribute").set("color")
colorObj.parm("seed").set(2.39)

nullObj.setDisplayFlag(True)

cam = hou.node("/obj").createNode("cam")
cam.parmTuple("t").set((-9, 4, 4))
cam.parmTuple("r").set((-90, -90, 60))

geo.layoutChildren()
hou.node("/obj").layoutChildren()

mantra = hou.node("/out").createNode("ifd")
mantra.parm("vm_picture").set("/Users/rajanp/work/houdini/remote-control.jpg")
mantra.render()

hou.hipFile.save("remote-control.hipnc")

