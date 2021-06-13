from typing import Callable, Any

from Helpers.location_helper import Vector2
from Scene.lighting import Lighting
from Scene.spatial_hash import SpatialHash


class HitBox:
    """
    Represents a basic AABB for collision checks
    """
    __slots__ = ['_position', '_size', '_anchor', 'light_caster', 'action', '_previous_position', '_right_upper',
                 '_center', 'index_in_list']

    def __init__(self, position: Vector2, size: Vector2, anchor: Vector2 = Vector2(0.5, 0.5),
                 light_caster: bool = False, action: Callable[..., Any] = None):
        self._position = position
        self._size = size
        self._anchor = anchor
        self.light_caster = light_caster
        self._right_upper = position + size
        self._center = position + size * anchor
        self.index_in_list = None

        self.action: Callable[..., Any] = action
        self._previous_position: Vector2 = None

        self._initialize()

    def _initialize(self):
        """
        Does some post-initialization of the hitbox object
        """
        if self.light_caster is True:
            Lighting.add_caster(self)
        SpatialHash.add_hitbox(self)

    @property
    def position(self) -> Vector2:
        """
        Returns the hitbox position vector
        """
        return self._position

    @position.setter
    def position(self, value: Vector2):
        """
        Sets a new position for the hitbox

        :param value: New hitbox position
        """
        old_cell_index, _, _ = SpatialHash.get_cell_index_from_center_pos(self._center)
        new_center = value + self._size * self._anchor
        new_cell_index, _, _ = SpatialHash.get_cell_index_from_center_pos(new_center)
        if SpatialHash.check_cell_index(new_cell_index) is False:
            print('WARNING: The position of hitbox was not updated!')
            return

        if old_cell_index != new_cell_index:
            # we need to transfer the hitbox from the current cell into another cell
            SpatialHash.transfer_hitbox(self, old_cell_index, new_cell_index)

        self._position = value
        self._right_upper = value + self._size
        self._center = value + self._size * self._anchor
        self._previous_position = None

    @property
    def size(self) -> Vector2:
        """
        Returns the size of the hitbox
        """
        return self._size

    @size.setter
    def size(self, value: Vector2):
        """
        Sets a new size for the hitbox
        """
        self._size = value
        self._right_upper = self.position + value
        self._center = self.position + value * self._anchor

    @property
    def anchor(self) -> Vector2:
        """
        Returns the anchor of the hitbox
        """
        return self._anchor

    @anchor.setter
    def anchor(self, value: Vector2):
        """
        Sets a new anchor for the hitbox
        """
        self._anchor = value
        self._center = self.position + self.size * value

    @property
    def center(self) -> Vector2:
        """
        Returns the center vector of the hitbox
        """
        return self._center

    def intersect(self, other: 'HitBox') -> bool:
        """
        Checks for intersection of the current hitbox and other hitbox

        :param other: The hitbox with which intersection is possible
        :return: True if hitboxes are intersected, otherwise False
        """
        lb1 = self._position
        ru1 = self._right_upper
        lb2 = other._position
        ru2 = other._right_upper

        # check if hitboxes are not intersecting
        if (lb1.x >= ru2.x) or (ru1.x <= lb2.x) or (ru1.y <= lb2.y) or (lb1.y >= ru2.y):
            return False

        # otherwise return True
        return True

    def update(self):
        """
        Updates the hitbox and checks for possible intersections with other hitboxes
        """
        # there is no need to calculate the intersections when there is nothing to do with them
        if self.action is None:
            return

        # there is no need to calculate the intersections when nothing changed from the previous frame
        if self._position != self._previous_position:
            nearby_objects = SpatialHash.get_nearby(self)

            # loop through all neighbour objects
            for other in nearby_objects:
                if other is self:
                    continue
                if self.intersect(other) is True:
                    # perform action
                    self.action(other)

            # update the previous position with the current position
            self._previous_position = self._position
