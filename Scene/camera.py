import numpy as np
from pyrr import Matrix44


class Camera:
    _instance: 'Camera' = None

    def __init__(self, window):
        self.__class__._instance = self

        self._position: list = [0.0] * 3
        self.zoom = 1
        self._zoom_matrix: Matrix44 = Matrix44.from_scale([self.zoom] * 3)
        self._projection_matrix = self.update_projection_matrix((window.width, window.height))
        # represents camera's aspect ratio and camera zoom
        self._camera_matrix = np.array(self._projection_matrix * self._zoom_matrix, dtype=np.float32)

        # represents camera position
        self._view_matrix = np.array(Matrix44.from_translation(self._position), dtype=np.float32)

    @classmethod
    def set_zoom(cls, zoom_value: float):
        """
        Sets the zoom value of the camera, a larger value corresponds to a smaller scale and vice versa
        """
        cls._instance.zoom = 1 / zoom_value
        cls._instance._zoom_matrix = Matrix44.from_scale([cls._instance.zoom] * 3)
        cls._instance._camera_matrix = np.array(cls._instance._projection_matrix * cls._instance._zoom_matrix,
                                                dtype=np.float32)

    @classmethod
    def add_zoom(cls, zoom_value: float):
        """
        Adds a zoom_value parameter to the existing camera's zoom value
        """
        cls.set_zoom(cls._instance.zoom + 1 / zoom_value)

    @classmethod
    def set_position(cls, x: float, y: float):
        """
        Sets the position of the scene object in world space
        :param x: Horizontal position
        :param y: Vertical position
        """
        cls._instance._position = [x, y, 0]
        cls._instance._view_matrix = np.array(Matrix44.from_translation(cls._instance._position), dtype=np.float32)

    @classmethod
    def add_position(cls, x: float, y: float):
        """
        Adds the input (x, y) vector to the existing scene object position
        """
        cls._instance.set_position(cls._instance._position[0] + x, cls._instance._position[1] + y)

    @classmethod
    def get_view_matrix(cls) -> np.array:
        return cls._instance._view_matrix

    @classmethod
    def get_camera_matrix(cls) -> np.array:
        return cls._instance._camera_matrix

    @staticmethod
    def update_projection_matrix(window_size: (int, int)):
        """
        Calculates the projection matrix
        :param window_size: Size of app window
        :return: Calculated projection matrix
        """
        width, height = window_size
        aspect_ratio = width / height
        return Matrix44.orthogonal_projection(-aspect_ratio, aspect_ratio, -1.0, 1.0, -1.0, 1.0).transpose()
