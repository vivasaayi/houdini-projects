import os

os.environ['HOUDINI_SCRIPT_LICENSE'] = 'hescape'

import hou

def get_file_content(file_name):
    f = open(file_name, "r")
    data = f.read()
    f.close()
    return data

python_script = get_file_content("./python-script.py")

try:
    hou.hipFile.load("test.hipnc")
except hou.LoadWarning as e:
    print(e)

hou.hipFile.clear()

geo = hou.node("/obj").createNode("geo")

nullObj = geo.createNode("null")
pyObj = geo.createNode("python")

nullObj.setInput(0, pyObj)

pyObj.parm("python").set(python_script)

pyObj.setDisplayFlag(True)

cam = hou.node("/obj").createNode("cam")
cam.parmTuple("t").set((11.3119, 4.52025, -3.47445))
cam.parmTuple("r").set((-146.009, 58.1698, -124.48))

geo.layoutChildren()
hou.node("/obj").layoutChildren()

mantra = hou.node("/out").createNode("ifd")
mantra.parm("vm_picture").set("$HOME/custom-scatter.jpg")
mantra.render()

hou.hipFile.save("custom-scatter.hipnc")

