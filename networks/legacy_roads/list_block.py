from gdpc import Block


air = Block('air')

stairs_devant = Block("oak_stairs", {"facing": "east"})
stairs_derriere = Block("oak_stairs", {"facing": "west"})
stairs_droite = Block("oak_stairs", {"facing": "north"})
stairs_gauche = Block("oak_stairs", {"facing": "south"})

stairs_devant_retourner = Block(
    "oak_stairs", {"facing": "east", "half": "top"})
stairs_derriere_retourner = Block(
    "oak_stairs", {"facing": "west", "half": "top"})
stairs_droite_retourner = Block(
    "oak_stairs", {"facing": "north", "half": "top"})
stairs_gauche_retourner = Block(
    "oak_stairs", {"facing": "south", "half": "top"})


stairs_quartz_devant = Block(
    "quartz_stairs", {"facing": "east", "half": "top"})
stairs_quartz_derriere = Block(
    "quartz_stairs", {"facing": "west", "half": "top"})
stairs_quartz_droite = Block(
    "quartz_stairs", {"facing": "north", "half": "top"})
stairs_quartz_gauche = Block(
    "quartz_stairs", {"facing": "south", "half": "top"})


door_east = Block("oak_door", {"facing": "east"})


oak_planks = Block("oak_planks")
oak_log = Block("oak_log")
spruce_wood = Block("spruce_wood")


black_stained_glass = Block("black_stained_glass")


white_concrete_powder = Block("white_concrete_powder")
white_concrete = Block("white_concrete")

grass_block = Block("grass_block")
podzol = Block("podzol")

block_quartz = Block("quartz_block")


block_white_concrete = Block("white_concrete")


oak_slab = Block('oak_slab')
quartz_slab_up = Block('quartz_slab', {"type": "top"})

oak_fence = Block('oak_fence')


style_basique = {
    'mur': "white_concrete",
    'sol': "oak_planks",
    'grass': "grass_block",
    'chemin': "quartz_block",
    'fence': 'oak_fence',
    'toit_esca': 'oak_stairs',
    'toit_planche': "oak_planks",
    'toit_slab': 'oak_slab',
    'glass': "glass",
    'door': 'oak_door'


}

style_jungle = {
    'mur': "light_gray_concrete",
    'sol': "acacia_planks",
    'grass': "grass_block",
    'chemin': "podzol",
    'fence': 'acacia_fence',
    'toit_esca': 'acacia_stairs',
    'toit_planche': "acacia_planks",
    'toit_slab': 'acacia_slab',
    'glass': "glass",
    'door': 'acacia_door'


}
style_end = {
    'mur': "purple_concrete",
    'sol': "crimson_planks",
    'grass': "grass_block",
    'chemin': "amethyst_block",
    'fence': 'crimson_fence',
    'toit_esca': 'crimson_stairs',
    'toit_planche': "crimson_planks",
    'toit_slab': 'crimson_slab',
    'glass': "glass",
    'door': 'crimson_door'


}

style_birch = {
    'mur': "yellow_concrete",
    'sol': "birch_planks",
    'grass': "grass_block",
    'chemin': "rooted_dirt",
    'fence': 'birch_fence',
    'toit_esca': 'birch_stairs',
    'toit_planche': "birch_planks",
    'toit_slab': 'birch_slab',
    'glass': "glass",
    'door': 'birch_door'


}
