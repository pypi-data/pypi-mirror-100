from .ycecream import YcecreamModule, y, default, set_defaults
from .ycecream import __version__
import sys

sys.modules[__name__] = YcecreamModule(sys.modules[__name__])

