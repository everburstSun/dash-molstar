# Legacy API (for backward compatibility): from dash_molstar.utils import molstar_helper
# Recommended: from dash_molstar.helpers import Camera, Target, Representation, shapes

from .target import Target
from .representations import Representation
from .camera import Camera
from . import shapes

# Re-export molstar_helper for backward compatibility
from ..helpers import molstar_helper