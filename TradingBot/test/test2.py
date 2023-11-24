import talib
from talib import stream
from talib.abstract import Function, _func_obj_mapping
import numpy as np

def sstream(func_name, *args, **kwargs):
    if func_name not in _func_obj_mapping:
        raise Exception('%s not supported by TA-LIB.' % func_name)
    if 'Function has an unstable period' in Function(func_name).function_flags:
        print(f'{func_name} indicator as an a unstable period')
        return getattr(talib, 'EMA')(*args, **kwargs)[-1]
    else:
        return getattr(stream, 'EMA')(*args, **kwargs)
