class ColorPrinter():
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    COLORS = ['PURPLE','CYAN','DARKCYAN','BLUE','GREEN','YELLOW','RED']

    def p(self, text, bold=False, underline= False):
        """purple"""
        return self.PURPLE + text + self.END
    def c(self, text, bold=False, underline= False):
        """cyan"""
        return self.CYAN + text + self.END
    def dc(self, text, bold=False, underline= False):
        """darkcyan"""
        return self.DARKCYAN + text + self.END
    def b(self, text, bold=False, underline= False):
        """blue"""
        return self.BLUE + text + self.END
    def g(self, text, bold=False, underline= False):
        """green"""
        return self.GREEN + text + self.END
    def y(self, text, bold=False, underline= False):
        """yellow"""
        return self.YELLOW + text + self.END
    def r(self, text, bold=False, underline= False):
        """red"""
        return self.RED + text + self.END

import talib
from talib import stream
from talib.abstract import Function, _func_obj_mapping

def sstream(func_name, *args, **kwargs):
    if func_name not in _func_obj_mapping:
        raise Exception('%s not supported by TA-LIB.' % func_name)
    if 'Function has an unstable period' in Function(func_name).function_flags or 'EMA' in func_name:
        print(f'{func_name} indicator as an a unstable period')
        return getattr(talib, 'EMA')(*args, **kwargs)[-1]
    else:
        return getattr(stream, 'EMA')(*args, **kwargs)
