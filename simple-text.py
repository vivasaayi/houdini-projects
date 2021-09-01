import os

os.environ['HOUDINI_SCRIPT_LICENSE'] = 'hescape'

import hou

try:
    hou.hipFile.load("test.hipnc")
except hou.LoadWarning as e:
    print(e)

hou.hipFile.clear()

# Some links to create
links = [
        ("Side Effects Software", "http://sidefx.com/"),
        ("Houdini Engine", "http://sidefx.com/engine"),
        ("OdForce", "http://odforce.net/"),
]

# Delete all the existing objects in /obj
# (Don't use this shelf tool in a real scene!)
for child in hou.node("/obj").children():
    child.destroy()

# Loop through the RSS feed articles, creating an object for each one
# encountered.
for index, (text, url) in enumerate(links):
    # Create an object with a font SOP inside, and set the text to the
    # article's text.  Note that we set run_init_scripts to False so the
    # geometry object doesn't contain a file sop.
    geo = hou.node("/obj").createNode("geo", run_init_scripts=False)
    font = geo.createNode("font")
    font.parm("text").set(text)

    # Append a color sop to the font SOP to change the color to black
    # so it's more readable in the viewer.
    color = geo.createNode("color")
    color.setFirstInput(font)
    color.parmTuple("color").set((0, 1, 0))
    color.setDisplayFlag(True)

    # Create a script to open the URL in the browser pane
    script = 'python -c "hou.ui.curDesktop().showSideHelp().setUrl(\'%s\')"' % url
    # Set it as the "pick script" for the object
    geo.parm("pickscript").set(script)

    # Move the geometry object's y position so the text doesn't overlap.
    geo.parm("ty").set(-2 * index)

# Fix the layout of the new nodes in the network editor
hou.node("/obj").layoutChildren()

hou.hipFile.save("text.hipnc")
