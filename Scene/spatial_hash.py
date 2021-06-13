import math

from Helpers.location_helper import Vector2


class SpatialHash:
    _instance: 'SpatialHash' = None
    _neighbours_position = [Vector2(-1, 0), Vector2(0, -1), Vector2(1, 0), Vector2(0, 1),
                            Vector2(-1, -1), Vector2(-1, 1), Vector2(1, 1), Vector2(1, -1)]
    __slots__ = ['world_size', 'half_world_size', 'cell_size', 'cells_number', 'cells', 'boundary_dimensions']

    def __init__(self, world_size: Vector2, cell_size: Vector2):
        self.__class__._instance = self
        self.world_size = world_size
        self.half_world_size = world_size * 0.5
        self.cell_size = cell_size
        self.cells_number = Vector2.zero
        self.cells = {}
        self.boundary_dimensions = Vector2.zero

        self.initialize_grid()

    def initialize_grid(self):
        """
        Does some post-initialization logic
        """
        rows = math.ceil(self.world_size.y / self.cell_size.y)
        columns = math.ceil(self.world_size.x / self.cell_size.x)

        self.cells_number = Vector2(columns, rows)
        self.cells = {i: [] for i in range(rows * columns)}
        # calculate values for the boundaries check
        self.boundary_dimensions = self.cells_number - Vector2.one

    @classmethod
    def get_cell_index_from_hitbox(cls, hitbox):
        """
        Returns the index of the cell which contains hitbox object
        """
        return cls.get_cell_index_from_center_pos(hitbox.center)

    @classmethod
    def get_cell_index_from_center_pos(cls, center):
        """
        Returns the index of the cell which contains hitbox object
        """
        self = cls._instance
        x = center.x // self.cell_size.x
        y = center.y // self.cell_size.y
        return x + y * self.cells_number.x, x, y

    @classmethod
    def check_cell_index(cls, index: int) -> bool:
        return 0 <= index <= len(cls._instance.cells) - 1

    @classmethod
    def add_hitbox(cls, hitbox):
        """
        Adds a hitbox to one of the cells based on the hitbox position
        """
        self = cls._instance
        index, _, _ = cls.get_cell_index_from_hitbox(hitbox)
        if cls.check_cell_index(index):
            self.cells[index].append(hitbox)
            hitbox.index_in_list = len(self.cells[index]) - 1
        else:
            print('WARNING: The hitbox object with position {0} and size {1} '
                  'was not added to the SpatialHash cells!'.format(hitbox.position.tuple(), hitbox.size.tuple()))

    @classmethod
    def transfer_hitbox(cls, hitbox, old_cell_index, new_cell_index):
        self = cls._instance
        old_cell_list = self.cells[old_cell_index]
        hitbox_index = hitbox.index_in_list
        last_index = len(old_cell_list) - 1
        # swap the hitbox item with the last item inside the old_cell_list
        old_cell_list[hitbox_index], old_cell_list[last_index] = old_cell_list[last_index], old_cell_list[hitbox_index]
        # there is an item placed at the hitbox_index now, this item was the last before the swap operation, so we
        # need to update its index too
        old_cell_list[hitbox_index].index_in_list = hitbox_index
        # our hitbox is the last item in old_cell_list now, so we need to remove it
        old_cell_list.pop()
        # append the hitbox to new cell list
        self.cells[new_cell_index].append(hitbox)
        # update hitbox.index_in_list with the new value
        hitbox.index_in_list = len(self.cells[new_cell_index]) - 1

    @classmethod
    def get_nearby(cls, hitbox) -> list:
        """
        Finds and returns the list of all nearby hitboxes

        :param hitbox: HitBox object for which we want to find nearby hitboxes
        :return: List of nearby hitboxes
        """
        self = cls._instance
        nearby_objects = []
        current_cell_index, x, y = self.get_cell_index_from_hitbox(hitbox)
        current_cell_pos = Vector2(x, y)
        nearby_objects[0:0] = self.cells[current_cell_index]

        # loop through all possible cell neighbours offsets
        for neighbour_pos in cls._neighbours_position:
            # find position of the neighbour cell
            pos = current_cell_pos + neighbour_pos
            # checks the boundaries of the found position
            if 0 <= pos.x <= self.boundary_dimensions.x and 0 <= pos.y <= self.boundary_dimensions.y:
                # calculate index for neighbour cell
                neighbour_index = int(pos.x + pos.y * self.cells_number.x)
                # insert all the hitboxes of the neighbour cell into our result list
                nearby_objects[0:0] = self.cells[neighbour_index]

        return nearby_objects
