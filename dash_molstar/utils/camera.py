import json, math, re
from typing import Optional, Dict, Any, Tuple, Union, Literal

Vec3 = Tuple[float, float, float]
CameraMode = Literal['perspective', 'orthographic']


class Camera:
    def __init__(self, snapshot: Optional[Dict[str, Any]] = None):
        self.__mode: CameraMode = 'perspective'
        self.__fov: float = 45.0
        self.__position: Vec3 = (0.0, 0.0, 100.0)
        self.__up: Vec3 = (0.0, 1.0, 0.0)
        self.__target: Vec3 = (0.0, 0.0, 0.0)
        self.__radius: float = 59.94
        self.__radiusMax: float = 59.94
        self.__fog: float = 15.0
        self.__clipFar: bool = True
        self.__minNear: float = 5.0
        self.__minFar: float = 1.0

        if snapshot:
            if 'mode' in snapshot:
                self.mode = snapshot['mode']
            if 'fov' in snapshot:
                self.fov = snapshot['fov']
            if 'position' in snapshot:
                self.position = snapshot['position']
            if 'up' in snapshot:
                self.up = snapshot['up']
            if 'target' in snapshot:
                self.target = snapshot['target']
            if 'radius' in snapshot:
                self.radius = snapshot['radius']
            if 'radiusMax' in snapshot:
                self.radiusMax = snapshot['radiusMax']
            if 'fog' in snapshot:
                self.fog = snapshot['fog']
            if 'clipFar' in snapshot:
                self.clipFar = snapshot['clipFar']
            if 'minNear' in snapshot:
                self.minNear = snapshot['minNear']
            if 'minFar' in snapshot:
                self.minFar = snapshot['minFar']
    
    @property
    def mode(self) -> CameraMode:
        """Camera mode: 'perspective' or 'orthographic'"""
        return self.__mode
    
    @mode.setter
    def mode(self, value: CameraMode):
        if value not in ('perspective', 'orthographic'):
            raise ValueError("mode must be 'perspective' or 'orthographic'")
        self.__mode = value
    
    @property
    def fov(self) -> float:
        """Field of view in degrees"""
        return self.__fov
    
    @fov.setter
    def fov(self, value: float):
        self.__fov = float(value)
    
    @property
    def position(self) -> Vec3:
        """Camera position as (x, y, z) tuple"""
        return self.__position
    
    @position.setter
    def position(self, value: Union[Vec3, list]):
        if len(value) != 3:
            raise ValueError("position must be a 3-element tuple or list")
        self.__position = (float(value[0]), float(value[1]), float(value[2]))
    
    # Up 
    @property
    def up(self) -> Vec3:
        """Camera up vector as (x, y, z) tuple"""
        return self.__up
    
    @up.setter
    def up(self, value: Union[Vec3, list]):
        if len(value) != 3:
            raise ValueError("up must be a 3-element tuple or list")
        self.__up = (float(value[0]), float(value[1]), float(value[2]))
    
    @property
    def target(self) -> Vec3:
        """Camera target/look-at point as (x, y, z) tuple"""
        return self.__target
    
    @target.setter
    def target(self, value: Union[Vec3, list]):
        if len(value) != 3:
            raise ValueError("target must be a 3-element tuple or list")
        self.__target = (float(value[0]), float(value[1]), float(value[2]))
    
    @property
    def radius(self) -> float:
        """Camera visible radius (object outside will be in fog)"""
        return self.__radius
    
    @radius.setter
    def radius(self, value: float):
        self.__radius = float(value)
    
    @property
    def radiusMax(self) -> float:
        """Maximum camera visible radius (radius of all visible objects)"""
        return self.__radiusMax
    
    @radiusMax.setter
    def radiusMax(self, value: float):
        self.__radiusMax = float(value)
    
    @property
    def fog(self) -> float:
        """Fog intensity (0-100)"""
        return self.__fog
    
    @fog.setter
    def fog(self, value: float):
        self.__fog = float(value)
    
    @property
    def clipFar(self) -> bool:
        """Whether to clip at far plane"""
        return self.__clipFar
    
    @clipFar.setter
    def clipFar(self, value: bool):
        self.__clipFar = bool(value)
    
    @property
    def minNear(self) -> float:
        """Minimum near clipping plane distance"""
        return self.__minNear
    
    @minNear.setter
    def minNear(self, value: float):
        self.__minNear = float(value)
    
    @property
    def minFar(self) -> float:
        """Minimum far clipping plane distance"""
        return self.__minFar
    
    @minFar.setter
    def minFar(self, value: float):
        self.__minFar = float(value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert camera state to a dictionary.
        
        Returns
        -------
        dict
            Dictionary containing all camera properties
        """
        return {
            'mode': self.__mode,
            'fov': self.__fov,
            'position': list(self.__position),
            'up': list(self.__up),
            'target': list(self.__target),
            'radius': self.__radius,
            'radiusMax': self.__radiusMax,
            'fog': self.__fog,
            'clipFar': self.__clipFar,
            'minNear': self.__minNear,
            'minFar': self.__minFar
        }
    
    def save_config(self, filename: str):
        """
        Save current camera configuration into JSON file.

        Parameters
        ----------
        `filename` — str
            JSON filename to be saved
        """
        if not filename.endswith('.json'): filename+='.json' 
        config = self.to_dict()
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)

    @classmethod
    def from_config(cls, filename: str) -> 'Camera':
        """
        Load a JSON configuration file and construct a new camera instance

        Parameters
        ----------
        `filename` — str
            JSON filename to be loaded

        Returns
        -------
        `Camera`
            The camera instance
        """
        with open(filename, 'r') as f:
            config = json.load(f)
        
        instance = cls(config)
        return instance

    @classmethod
    def from_pymol_view(cls, view: Union[str, Tuple[float, ...], list]) -> 'Camera':
        """
        Create a Camera from PyMOL's get_view() output.

        PyMOL view consists of 18 floats:
        - 0-8: 3x3 rotation matrix (row-major, camera coords relative to world)
        - 9-11: camera position offset relative to target (usually (0, 0, -distance))
        - 12-14: rotation center / target point (world coordinates)
        - 15: front clipping plane distance
        - 16: rear clipping plane distance  
        - 17: orthoscopic flag (1=orthographic, 0=perspective)

        Parameters
        ----------
        `view` — Union[str, Tuple[float, ...], list]
            Either a string output from PyMOL's get_view() command,
            or a tuple/list of 18 floats

        Returns
        -------
        `Camera`
            A new Camera instance with converted settings

        Raises
        ------
        `ValueError`
            If the input does not contain exactly 18 values

        Example
        -------
        >>> # From PyMOL console output string
        >>> view_str = '''(
        ...     0.984808,    0.000000,   -0.173648,
        ...     0.000000,    1.000000,    0.000000,
        ...     0.173648,    0.000000,    0.984808,
        ...     0.000000,    0.000000, -150.000000,
        ...    10.000000,   20.000000,   30.000000,
        ...   100.000000,  200.000000,    0.000000 )'''
        >>> camera = Camera.from_pymol_view(view_str)
        """
        # Parse input
        if isinstance(view, str):
            # Remove parentheses, newlines, and split by comma
            cleaned = view.replace('(', '').replace(')', '').replace('\n', ' ')
            values = [float(x.strip()) for x in cleaned.split(',') if x.strip()]
        else:
            values = list(view)

        if len(values) != 18:
            raise ValueError(f"PyMOL view must contain exactly 18 values, got {len(values)}")

        # Extract rotation matrix (3x3, row-major)
        rot = [
            [values[0], values[1], values[2]],
            [values[3], values[4], values[5]],
            [values[6], values[7], values[8]]
        ]

        # Camera offset in camera space: position of target relative to camera
        cam_offset = (values[9], values[10], values[11])

        # Target/rotation center in world coordinates
        target = (values[12], values[13], values[14])

        # Clipping planes
        front_clip = values[15]
        rear_clip = values[16]

        # Projection mode
        is_ortho = values[17] != 0

        # Transform camera offset from camera space to world space
        offset_world = (
            rot[0][0] * cam_offset[0] + rot[1][0] * cam_offset[1] + rot[2][0] * cam_offset[2],
            rot[0][1] * cam_offset[0] + rot[1][1] * cam_offset[1] + rot[2][1] * cam_offset[2],
            rot[0][2] * cam_offset[0] + rot[1][2] * cam_offset[1] + rot[2][2] * cam_offset[2]
        )
        position = (
            target[0] - offset_world[0],
            target[1] - offset_world[1],
            target[2] - offset_world[2]
        )

        # Up vector is the second row of the transposed rotation matrix
        up = (rot[1][0], rot[1][1], rot[1][2])

        # Normalize up vector
        up_len = math.sqrt(up[0]**2 + up[1]**2 + up[2]**2)
        if up_len > 0:
            up = (up[0]/up_len, up[1]/up_len, up[2]/up_len)

        # Calculate camera distance and radius
        distance = math.sqrt(cam_offset[0]**2 + cam_offset[1]**2 + cam_offset[2]**2)
        radius = (rear_clip - front_clip) / 2.0 if rear_clip > front_clip else distance / 2.0

        return cls({
            'mode': 'orthographic' if is_ortho else 'perspective',
            'fov': math.radians(abs(values[17])),
            'position': position,
            'up': up,
            'target': target,
            'radius': radius,
            'radiusMax': max(radius, rear_clip),
            'minNear': 5.0,
            'minFar': 0
        })
