# Legacy API (for backward compatibility): from dash_molstar.utils import molstar_helper
# Recommended: from dash_molstar.helpers import Camera, Target, Representation, shapes

from .target import Target
from .representations import Representation
from .camera import Camera
from .screenshot import Screenshot, default_axes_params
from . import shapes
from .np import named_params

# Re-export molstar_helper for backward compatibility
from ..helpers import molstar_helper



__all__ = [
    "Target",
    "Representation",
    "Camera",
    "shapes",
    "molstar_helper",
    "Screenshot",
    "default_axes_params",
    "named_params",
]