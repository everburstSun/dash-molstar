import json
from typing import Optional, Dict, Any
from importlib import resources

class Representation(object):
    def __init__(self, type: str = 'cartoon', color: Optional[str] = None, size: Optional[str] = None):
        self._params = self._load_valid_params('representation_params.json')
        
        self._type = 'cartoon'
        self._color = None
        self._size = None
        self._type_params: Dict[str, Any] = {}
        self._color_params: Dict[str, Any] = {}
        self._size_params: Dict[str, Any] = {}
        
        self.type = type
        if color:
            self.color = color
        if size:
            self.size = size

    def _load_valid_params(self, filename: str) -> Dict[str, Any]:
        try:
            with resources.open_text('dash_molstar.utils', filename) as f:
                return json.load(f)
        except (ImportError, FileNotFoundError):
            raise FileNotFoundError(f"Unable to locate the parameter definition file.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"The parameter definition file has been broken, please reinstall the package.")

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        if value in self._params.get('type', []):
            self._type = value
            self._type_params = {}  # reset type_params
        else:
            raise ValueError(f"Invalid type: {value}. Must be one of {self._params.get('type', [])}")

    @property
    def color(self) -> Optional[str]:
        return self._color

    @color.setter
    def color(self, value: Optional[str]):
        if value is None or value in self._params.get('color', []):
            self._color = value
            self._color_params = {}  # reset color_params
        else:
            raise ValueError(f"Invalid color: {value}. Must be one of {self._params.get('color', [])} or None")

    @property
    def size(self) -> Optional[str]:
        return self._size

    @size.setter
    def size(self, value: Optional[str]):
        if value is None or value in self._params.get('size', []):
            self._size = value
            self._size_params = {}  # reset size_params
        else:
            raise ValueError(f"Invalid size: {value}. Must be one of {self._params.get('size', [])} or None")

    def set_type_params(self, params: Dict[str, Any]):
        valid_params = self._params['typeParams'][self._type]
        self._set_params(self._type_params, params, valid_params, 'type')

    def set_color_params(self, params: Dict[str, Any]):
        if not self._color:
            raise ValueError("Color must be set before setting color params")
        valid_params = self._params['colorParams'][self._color]
        self._set_params(self._color_params, params, valid_params, 'color')

    def set_size_params(self, params: Dict[str, Any]):
        if not self._size:
            raise ValueError("Size must be set before setting size params")
        valid_params = self._params['sizeParams'][self._size]
        self._set_params(self._size_params, params, valid_params, 'size')

    def _set_params(self, target: Dict[str, Any], params: Dict[str, Any], valid_params: list, param_type: str):
        for key, value in params.items():
            if key in valid_params:
                target[key] = value
            else:
                print(f"Warning: '{key}' is not a valid parameter for {param_type}. Ignoring this parameter.")

    def np(self, name, params=None):
        """
        Generate `NamedParams` for parameters

        Parameters
        ----------
        `name` — str
            Parameter name
        `params` — any
            Parameters

        Returns
        -------
        `dict`
            NamedParams
        """
        return {'name': name, 'params': params}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Return the dict for creating representation

        Returns
        -------
        `Dict[str, Any]`
            Representation dict
        """
        result = {'type': self._type}
        if self._type_params:
            result['typeParams'] = self._type_params
        if self._color:
            result['color'] = self._color
            if self._color_params:
                result['colorParams'] = self._color_params
        if self._size:
            result['size'] = self._size
            if self._size_params:
                result['sizeParams'] = self._size_params
        return result
    
    def save_config(self, filename: str):
        """
        Save current representation configuration into JSON file.

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
    def from_config(cls, filename: str) -> 'Representation':
        """
        Load a JSON configuration file and construct a new representation instance

        Parameters
        ----------
        `filename` — str
            JSON filename to be loaded

        Returns
        -------
        `Representation`
            The representation instance
        """
        with open(filename, 'r') as f:
            config = json.load(f)
        
        instance = cls(
            type=config.get('type', 'cartoon'),
            color=config.get('color'),
            size=config.get('size')
        )
        
        if 'typeParams' in config:
            instance.set_type_params(config['typeParams'])
        if 'colorParams' in config:
            instance.set_color_params(config['colorParams'])
        if 'sizeParams' in config:
            instance.set_size_params(config['sizeParams'])
        
        return instance
    
if __name__ == '__main__':
    rep = Representation('cartoon')