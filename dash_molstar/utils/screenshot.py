import json
from .np import named_params

default_axes_params = {
    "alpha": 0.51,
    "colorX": 0xFF0000,
    "colorY": 0x00FF00,
    "colorZ": 0x0000FF,
    "scale": 0.33,
    "location": "bottom-left",
    "locationOffsetX": 0,
    "locationOffsetY": 0,
    "originColor": 0x808080,
    "radiusScale": 0.075,
    "showPlanes": True,
    "planeColorXY": 0x808080,
    "planeColorXZ": 0x808080,
    "planeColorYZ": 0x808080,
    "showLabels": False,
    "labelX": "X",
    "labelY": "Y",
    "labelZ": "Z",
    "labelColorX": 0x808080,
    "labelColorY": 0x808080,
    "labelColorZ": 0x808080,
    "labelOpacity": 1,
    "labelScale": 0.25
}

class Screenshot(object):
    def __init__(self, resolution=named_params('ultra-hd'), transparent=False, axes=named_params('off'), illumination=None, crop=None):
        self._resolution = resolution
        self._transparent = transparent
        self._axes = axes
        self._illumination = illumination
        self._crop = crop

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        if type(value) is not dict and value is not None:
            raise ValueError("Resolution must be a dict or None")
        if type(value) is dict:
            if 'name' not in value.keys() or 'params' not in value.keys():
                raise ValueError("Resolution dict must be \"NamedParams\"")
            valid_keys = {"width", "height"}
            if not value['params'].keys().issubset(valid_keys):
                raise ValueError(f"Resolution params contains invalid keys: {value['params'].keys() - valid_keys}")
        self._resolution = value

    @property
    def transparent(self):
        return self._transparent

    @transparent.setter
    def transparent(self, value):
        self._transparent = value

    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, value):
        if type(value) is not dict and value is not None:
            raise ValueError("Axes must be a dict or None")
        if type(value) is dict:
            if 'name' not in value.keys() or 'params' not in value.keys():
                raise ValueError("Axes dict must be \"NamedParams\"")
            valid_keys = {"alpha", "colorX", "colorY", "colorZ", "scale", "location", "locationOffsetX", "locationOffsetY", "originColor", "radiusScale", "showPlanes", "planeColorXY", "planeColorXZ", "planeColorYZ", "showLabels", "labelX", "labelY", "labelZ", "labelColorX", "labelColorY", "labelColorZ", "labelOpacity", "labelScale"}
            if not value['params'].keys().issubset(valid_keys):
                raise ValueError(f"Axes params contains invalid keys: {value['params'].keys() - valid_keys}")
        self._axes = value

    @property
    def illumination(self):
        return self._illumination

    @illumination.setter
    def illumination(self, value):
        if type(value) is not dict and value is not None:
            raise ValueError("Illumination must be a dict or None")
        if type(value) is dict:
            valid_keys = {"extraIterations", "targetIterationTimeMs"}
            if not valid_keys.issubset(value.keys()):
                raise ValueError(f"Illumination dict must contain keys: {valid_keys}")
        self._illumination = value

    @property
    def crop(self):
        return self._crop

    @crop.setter
    def crop(self, value):
        if type(value) is not dict and value is not None:
            raise ValueError("Crop must be a dict or None")
        if type(value) is dict:
            valid_keys = {"x", "y", "width", "height"}
            if not valid_keys.issubset(value.keys()):
                raise ValueError(f"Crop dict must contain keys: {valid_keys}")
        self._crop = value

    def reset_crop(self):
        self._crop = None

    def to_dict(self):
        """
        Convert screenshot config to a dictionary.

        Returns
        -------
        dict
            Dictionary containing all screenshot properties
        """
        d = {
            'resolution': self._resolution,
            'transparent': self._transparent,
            'axes': self._axes,
        }
        if self._illumination is not None:
            d['illumination'] = self._illumination
        if self._crop is not None:
            d['crop'] = self._crop
        return d

    def save_config(self, filename):
        """
        Save current screenshot configuration into JSON file.

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
    def from_config(cls, filename):
        """
        Load a JSON configuration file and construct a new screenshot instance

        Parameters
        ----------
        `filename` — str
            JSON filename to be loaded

        Returns
        -------
        `Screenshot`
            The screenshot instance
        """
        with open(filename, 'r') as f:
            config = json.load(f)

        instance = cls(
            resolution=config.get('resolution'),
            transparent=config.get('transparent'),
            axes=config.get('axes'),
            illumination=config.get('illumination'),
            crop=config.get('crop')
        )

        return instance