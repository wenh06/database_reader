# -*- coding: utf-8 -*-
"""
docstring, to write
"""

from .cpsc2018 import *
from .cpsc2019 import *
from .cpsc2020 import *
from .cpsc2021 import *


__all__ = [s for s in dir() if not s.startswith('_')]
