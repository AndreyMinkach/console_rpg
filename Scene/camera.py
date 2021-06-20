import numpy as np
from pyrr import matrix44

from Helpers.location_helper import Vector2


class Camera:
    _instance: 'Camera' = None

    __slots__ = ['_position', '_zoom', '_window_width', '_window_height', '_zoom_matrix', '_projection_matrix',
                 '_world_to_screen_multiplier', '_view_matrix']

    def __init__(self, window, position: Vector2 = Vector2.zero, zoom: float = 1):
        self.__class__._instance = self

        self._position: np.array = np.array([0, 0], dtype=np.float32)
        self._zoom: float = 1
        self._window_width: int = window.width
        self._window_height: int = window.height

        self._zoom_matrix: np.array = np.identity(4)
        self._projection_matrix: np.array = np.identity(4)
        # represents world to screen camera matrix
        self._world_to_screen_multiplier: float = 1.0
        # represents camera position
        self._view_matrix: np.array = np.identity(4)

        Camera.set_position(position.x, position.y)
        Camera.set_zoom(zoom)
        self.update_projection_matrix(window.width, window.height)

    @classmethod
    def set_zoom(cls, zoom_value: float):
        """
        Sets the zoom value of the camera, a larger value corresponds to a smaller scale and vice versa
        """
        self = cls._instance

        self._zoom = 1 / zoom_value
        self._zoom_matrix[0, 0] = self._zoom
        self._zoom_matrix[1, 1] = self._zoom
        self._zoom_matrix[2, 2] = self._zoom

    @classmethod
    def get_zoom(cls) -> float:
        """
        Returns the zoom value of the camera
        """
        return 1.0 / cls._instance._zoom

    @classmethod
    def world_to_screen(cls, x: float, y: float) -> (int, int):
        """
        Converts specified vector values to screen space

        :param x: X coordinate
        :param y: Y coordinate
        :return: Converted vector in screen space
        """
        self = cls._instance
        a = self._world_to_screen_multiplier * self._zoom
        b = self._zoom
        s_x = round((a * x + 1.0) * 0.5 * self._window_width)
        s_y = round((b * y + 1.0) * 0.5 * self._window_height)
        return s_x, s_y

    @classmethod
    def screen_to_world(cls, x: int, y: int) -> (float, float):
        """
        Converts specified vector values to world space

        :param x: X coordinate
        :param y: Y coordinate
        :return: Converted vector in world space
        """
        self = cls._instance
        s_x = 2.0 * (x / self._window_width) - 1.0
        s_y = 2.0 * (y / self._window_height) - 1.0
        a = 1.0 / (self._world_to_screen_multiplier * self._zoom)
        b = 1.0 / self._zoom
        return s_x * a, s_y * b

    @classmethod
    def add_zoom(cls, zoom_value: float):
        """
        Adds a zoom_value parameter to the camera's zoom value
        """
        cls.set_zoom(cls._instance._zoom + 1 / zoom_value)

    @classmethod
    def set_position(cls, x: float, y: float):
        """
        Sets the position of the camera in world space

        :param x: Horizontal position
        :param y: Vertical position
        """
        self = cls._instance

        self._position[0], self._position[1] = -x, -y
        self._view_matrix[3, 0:2] = self._position

    @classmethod
    def get_position(cls) -> (float, float):
        """
        Returns the position of the camera in world space
        """
        self = cls._instance
        return self._position[0], self._position[1]

    @classmethod
    def add_position(cls, x: float, y: float):
        """
        Adds the input (x, y) vector to the camera position
        """
        cls._instance.set_position(cls._instance._position[0] + x, cls._instance._position[1] + y)

    @classmethod
    def get_view_matrix(cls) -> np.array:
        return cls._instance._view_matrix

    @classmethod
    def get_projection_matrix(cls) -> np.array:
        return cls._instance._projection_matrix

    @classmethod
    def get_zoom_matrix(cls) -> np.array:
        return cls._instance._zoom_matrix

    @classmethod
    def update_projection_matrix(cls, width: int, height: int):
        """
        Calculates the projection matrix

        :param width: Width of app window
        :param height: height of app window
        :return: Calculated projection matrix
        """
        self = cls._instance
        aspect_ratio = width / height
        self._window_width = width
        self._window_height = height
        self._projection_matrix = matrix44.create_orthogonal_projection(-aspect_ratio, aspect_ratio,
                                                                        -1.0, 1.0, -1.0, 1.0)
        self._world_to_screen_multiplier = (2.0 / (aspect_ratio + aspect_ratio))
