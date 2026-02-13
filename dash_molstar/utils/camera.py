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
        self.__radius: float = 100.0
        self.__radiusMax: float = 100.0
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

        # Camera offset in camera space (relative to target)
        cam_offset = (values[9], values[10], values[11])

        # Target/rotation center in world coordinates
        target = (values[12], values[13], values[14])

        # Clipping planes
        front_clip = values[15]
        rear_clip = values[16]

        # Projection mode
        is_ortho = values[17] != 0

        # Transform camera offset from camera space to world space
        # position = R^T * cam_offset + target
        # (R^T because PyMOL stores the inverse rotation)
        position = (
            rot[0][0] * cam_offset[0] + rot[1][0] * cam_offset[1] + rot[2][0] * cam_offset[2] + target[0],
            rot[0][1] * cam_offset[0] + rot[1][1] * cam_offset[1] + rot[2][1] * cam_offset[2] + target[1],
            rot[0][2] * cam_offset[0] + rot[1][2] * cam_offset[1] + rot[2][2] * cam_offset[2] + target[2]
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
            'fov': 45.0,  # PyMOL default FOV
            'position': position,
            'up': up,
            'target': target,
            'radius': radius,
            'radiusMax': max(radius, rear_clip),
            'minNear': max(1.0, front_clip) if front_clip > 0 else 5.0,
            'minFar': 1.0
        })

    @classmethod
    def from_chimera_view(cls, view: str) -> 'Camera':
        """
        Create a Camera from Chimera/ChimeraX matrixset format.

        Chimera matrix format (from `matrixget` command) is 3 rows x 4 columns:
        ```
        Model 0.0
            r00 r01 r02 tx
            r10 r11 r12 ty
            r20 r21 r22 tz
        ```

        Each row contains 3 rotation matrix elements plus 1 translation component.
        This represents a 3x4 transformation matrix [R|t].

        For camera view (from `cofr` and `view` commands), the format may also be:
        ```
        center: x y z
        viewSize: s
        ```

        Parameters
        ----------
        `view` — str
            String output from Chimera's matrixget or view commands

        Returns
        -------
        `Camera`
            A new Camera instance with converted settings

        Example
        -------
        >>> view_str = '''Model 0.0
        ...     0.688816 0.672651 -0.270321 -3.40168
        ...     0.327689 0.0437142 0.943774 1.87208
        ...     0.646647 -0.738668 -0.190309 11.6143'''
        >>> camera = Camera.from_chimera_view(view_str)
        """
        lines = [l.strip() for l in view.strip().split('\n') if l.strip()]

        rot = []
        translation = [0.0, 0.0, 0.0]
        center = None
        view_size = None

        i = 0
        while i < len(lines):
            line = lines[i]

            # Skip model header lines
            if line.startswith('Model') or line.startswith('model'):
                i += 1
                continue

            # Check for center directive
            if line.lower().startswith('center:'):
                parts = line.split(':')[1].strip().split()
                center = tuple(float(x) for x in parts[:3])
                i += 1
                continue

            # Check for viewSize directive
            if line.lower().startswith('viewsize:'):
                view_size = float(line.split(':')[1].strip())
                i += 1
                continue

            # Try to parse as matrix rows (3 rotation values + 1 translation per row)
            parts = line.split()
            if len(parts) >= 4:
                try:
                    # Each row: r0 r1 r2 t
                    row_rot = [float(parts[0]), float(parts[1]), float(parts[2])]
                    row_trans = float(parts[3])
                    if len(rot) < 3:
                        rot.append(row_rot)
                        translation[len(rot) - 1] = row_trans
                except ValueError:
                    pass
            elif len(parts) == 3:
                # Fallback: 3-column format (rotation only)
                try:
                    row = [float(x) for x in parts[:3]]
                    if len(rot) < 3:
                        rot.append(row)
                except ValueError:
                    pass
            i += 1

        # Default values if not found
        if center is None:
            center = (0.0, 0.0, 0.0)
        if view_size is None:
            view_size = 100.0
        if len(rot) < 3:
            rot = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        translation = tuple(translation)

        # The model matrix in Chimera transforms model coords to camera coords
        # We need to invert this to get camera position in world coords

        # Target is at the center (or translated center)
        target = (
            center[0] + translation[0],
            center[1] + translation[1], 
            center[2] + translation[2]
        )

        # Camera looks down -Z axis in camera space
        # Position is behind the target along the viewing direction
        distance = view_size * 2.5  # Approximate conversion factor

        # The rotation matrix columns give us the camera axes
        # Camera position = target + distance * viewing_direction
        # Viewing direction is the third column of transposed rotation (or third row of rotation)
        view_dir = (rot[2][0], rot[2][1], rot[2][2])
        dir_len = math.sqrt(view_dir[0]**2 + view_dir[1]**2 + view_dir[2]**2)
        if dir_len > 0:
            view_dir = (view_dir[0]/dir_len, view_dir[1]/dir_len, view_dir[2]/dir_len)

        position = (
            target[0] - view_dir[0] * distance,
            target[1] - view_dir[1] * distance,
            target[2] - view_dir[2] * distance
        )

        # Up vector is the second row of rotation matrix
        up = (rot[1][0], rot[1][1], rot[1][2])
        up_len = math.sqrt(up[0]**2 + up[1]**2 + up[2]**2)
        if up_len > 0:
            up = (up[0]/up_len, up[1]/up_len, up[2]/up_len)

        return cls({
            'mode': 'perspective',
            'fov': 45.0,
            'position': position,
            'up': up,
            'target': target,
            'radius': view_size,
            'radiusMax': view_size * 2,
            'minNear': 5.0,
            'minFar': 1.0
        })

    @classmethod
    def from_vmd_view(cls, view: str) -> 'Camera':
        """
        Create a Camera from VMD display/molinfo settings.

        VMD view can be obtained via several methods:
        1. `display get` commands for projection settings
        2. `molinfo top get {center_matrix rotate_matrix scale_matrix global_matrix}`

        Expected format (from VMD Tcl console):
        ```
        rotate_matrix: {{r00 r01 r02 r03} {r10 r11 r12 r13} {r20 r21 r22 r23} {r30 r31 r32 r33}}
        center_matrix: {{1 0 0 cx} {0 1 0 cy} {0 0 1 cz} {0 0 0 1}}
        scale_matrix: {{s 0 0 0} {0 s 0 0} {0 0 s 0} {0 0 0 1}}
        global_matrix: {{1 0 0 tx} {0 1 0 ty} {0 0 1 tz} {0 0 0 1}}
        ```

        Or simplified format:
        ```
        center: x y z
        rotate: r00 r01 r02 r10 r11 r12 r20 r21 r22
        scale: s
        translate: tx ty tz
        projection: perspective|orthographic
        nearclip: n
        farclip: f
        ```

        Parameters
        ----------
        `view` — str
            String containing VMD view settings

        Returns
        -------
        `Camera`
            A new Camera instance with converted settings

        Example
        -------
        >>> view_str = '''center: 10.0 20.0 30.0
        ... rotate: 1 0 0 0 1 0 0 0 1
        ... scale: 0.05
        ... translate: 0 0 -50
        ... projection: perspective'''
        >>> camera = Camera.from_vmd_view(view_str)
        """
        # Default values
        center = [0.0, 0.0, 0.0]
        rotation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        scale = 1.0
        translate = [0.0, 0.0, 0.0]
        projection = 'perspective'
        near_clip = 5.0
        far_clip = 1000.0

        lines = view.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Parse center
            if line.lower().startswith('center:') or line.lower().startswith('center_matrix:'):
                # Extract numbers
                nums = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', line)
                if len(nums) >= 3:
                    # For center_matrix, find the translation components (indices 3, 7, 11)
                    if 'matrix' in line.lower() and len(nums) >= 12:
                        center = [float(nums[3]), float(nums[7]), float(nums[11])]
                    else:
                        center = [float(nums[0]), float(nums[1]), float(nums[2])]

            # Parse rotation
            elif line.lower().startswith('rotate:') or line.lower().startswith('rotate_matrix:'):
                nums = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', line)
                if 'matrix' in line.lower() and len(nums) >= 16:
                    # 4x4 matrix format
                    rotation = [
                        [float(nums[0]), float(nums[1]), float(nums[2])],
                        [float(nums[4]), float(nums[5]), float(nums[6])],
                        [float(nums[8]), float(nums[9]), float(nums[10])]
                    ]
                elif len(nums) >= 9:
                    # 3x3 rotation values
                    rotation = [
                        [float(nums[0]), float(nums[1]), float(nums[2])],
                        [float(nums[3]), float(nums[4]), float(nums[5])],
                        [float(nums[6]), float(nums[7]), float(nums[8])]
                    ]

            # Parse scale
            elif line.lower().startswith('scale:') or line.lower().startswith('scale_matrix:'):
                nums = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', line)
                if nums:
                    scale = float(nums[0])

            # Parse translate/global
            elif line.lower().startswith('translate:') or line.lower().startswith('global_matrix:'):
                nums = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', line)
                if 'matrix' in line.lower() and len(nums) >= 12:
                    translate = [float(nums[3]), float(nums[7]), float(nums[11])]
                elif len(nums) >= 3:
                    translate = [float(nums[0]), float(nums[1]), float(nums[2])]

            # Parse projection mode
            elif line.lower().startswith('projection:'):
                if 'ortho' in line.lower():
                    projection = 'orthographic'
                else:
                    projection = 'perspective'

            # Parse clipping planes
            elif line.lower().startswith('nearclip:'):
                nums = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', line)
                if nums:
                    near_clip = float(nums[0])

            elif line.lower().startswith('farclip:'):
                nums = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', line)
                if nums:
                    far_clip = float(nums[0])

        # VMD uses a different coordinate system
        # The center is negated and transformed
        target = (
            -center[0] + translate[0],
            -center[1] + translate[1],
            -center[2] + translate[2]
        )

        # VMD scale affects the viewing distance
        # Smaller scale = further away
        if scale > 0:
            distance = 50.0 / scale  # Approximate conversion
        else:
            distance = 100.0

        # Calculate camera position
        # View direction is the third column of rotation matrix (looking down -Z)
        view_dir = (rotation[0][2], rotation[1][2], rotation[2][2])
        dir_len = math.sqrt(view_dir[0]**2 + view_dir[1]**2 + view_dir[2]**2)
        if dir_len > 0:
            view_dir = (view_dir[0]/dir_len, view_dir[1]/dir_len, view_dir[2]/dir_len)

        position = (
            target[0] - view_dir[0] * distance,
            target[1] - view_dir[1] * distance,
            target[2] - view_dir[2] * distance
        )

        # Up vector is the second row of rotation
        up = (rotation[0][1], rotation[1][1], rotation[2][1])
        up_len = math.sqrt(up[0]**2 + up[1]**2 + up[2]**2)
        if up_len > 0:
            up = (up[0]/up_len, up[1]/up_len, up[2]/up_len)

        # Estimate radius from clipping planes
        radius = (far_clip - near_clip) / 2.0 if far_clip > near_clip else distance / 2.0

        return cls({
            'mode': projection,
            'fov': 45.0,
            'position': position,
            'up': up,
            'target': target,
            'radius': radius,
            'radiusMax': max(radius, far_clip),
            'minNear': max(1.0, near_clip),
            'minFar': 1.0
        })
