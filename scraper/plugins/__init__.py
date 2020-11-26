# for: core/plugins/__init__.py
# use: from core.plugins import *

import inspect
import importlib
import pathlib
import sys
import os
from .core import *


plugins = {}
all_added = {}
first_start = 1 


def reload_plugins():
    global first_start
    g = inspect.currentframe().f_back.f_globals
    all_plugs = pathlib.Path(__file__).parent.glob('*.py')
    #Verify the old imported files if theyre still there or not!
    if not first_start:
        for k in list(all_added.keys()):
            if not k.split('/')[-1].startswith('_'):
                if not os.path.exists(k):
                    funcs = all_added[k]
                    for func in funcs:
                        del g[func]
                    del all_added[k]

    #Ive performed deletion first because if we reload new modules and the delete we might deletethe imports that are common in other files and it will create errors while running!
    #Now will check and Import other plugins 
    for path in all_plugs:
        all_classes = []
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
                    all_classes.append(name)
            all_added[path.__str__()] = all_classes
    first_start = 0



def get_curr_globals():
    g = inspect.currentframe().f_back.f_globals
    existing = sys.modules
    return g,existing,all_added

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