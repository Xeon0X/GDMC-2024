import World


def get_data(world: World):
    heightmap, watermap, treemap = world.getData()
    heightmap.save('./data/heightmap.png')
    watermap.save('./data/watermap.png')
    treemap.save('./data/treemap.png')


def main():
    world = World.World()
    get_data(world)


if __name__ == '__main__':
    main()
