from gdpc import Editor, Block, geometry

editor = Editor(buffering=True)

# Get a block
block = editor.getBlock((0,48,0))

# Place a block
editor.placeBlock((448, 92, 515), Block("stone"))

# Build a cube
geometry.placeCuboid(editor, (458, 92, 488), (468, 99, 471), Block("oak_planks"))