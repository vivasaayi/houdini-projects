# Run a generator Box SOP Verb
node = hou.pwd()
geo = node.geometry()

verb = hou.sopNodeTypeCategory().nodeVerb("box")

# Get a fresh geometry to write to
geo = hou.Geometry()

# Dictionary of parameter/values.  Unspecified values
# will be default (which may change each version!)
verb.setParms( { 
                't' : (1, 1, 2 ),
                'size' : (1, 2, 5)
               } )

# To run a generator we have to use verb.execute
# otherwise we become the input and override the size.
verb.execute(geo, [])

# Save results back to the node
node.geometry().clear()
node.geometry().merge(geo)

