# for: core/plugins/__init__.py
# use: from core.plugins import *

import inspect
import importlib
import pathlib
import sys
from .core import *


plugins = {}

def reload_plugins():

    g = inspect.currentframe().f_back.f_globals

    for path in pathlib.Path(__file__).parent.glob('*.py'):
        if not path.name.startswith('_'):
            existing = sys.modules.get(f'{__name__}.{path.stem}')
            if existing:
                mod = importlib.reload(existing)
            else:
                mod = importlib.import_module(f'.{path.stem}', __name__)
            for name in mod.__dict__.get('__all__', dir(mod)):
                if not name.startswith('_'):
                    g[name] = getattr(mod, name)
                    plugins[path.stem] = path.stem.title()

def scrap_data(*args):
    if args:
        url = args[0]
        dom = get_domain_info(url)
        domain = dom['domain'].lower()
        func = plugins[domain]
        res = eval(f"{func}('{url}')")
        res = res.get_result()
        return res
    else:
        raise Exception(NameError,'No url Passed')
    

reload_plugins()