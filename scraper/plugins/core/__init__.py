import importlib
import re
from requests_html import HTMLSession as r
from fake_headers import Headers as Headerss
import tldextract
import simplejson as json
import resource
import os
from os import replace
from bs4 import BeautifulSoup
from lxml import html
import pickle
import pathlib
import re
import importlib
import random

cwd  = str(pathlib.Path(__file__).parent.absolute())

plugs_db_loc = cwd+'/../plugs.db'

modules = []

def load_plugins1():
    allfiles = os.listdir(cwd)
    pysearchre = re.compile('.py$', re.IGNORECASE)
    pluginfiles = filter(pysearchre.search,
                           os.listdir(cwd))

    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = map(form_module, pluginfiles)

    for plugin in plugins:
             #plugn = plugin
             if not plugin.startswith('__'):
                modules.append(importlib.import_module(plugin, package="plugins"))
    allmodules = modules
    return modules



class mydict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def get_url_string(string): 
  
    # findall() has been used  
    # with valid conditions for urls in string 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url] 


    

def get_domain_info(url):
    dom = tldextract.extract(url)
    domain = dom.domain
    suffix = dom.suffix
    fqdn = dom.fqdn
    full = dom.fqdn
    scheme = url.split(':')[0]
    full = scheme+'://'+full
    dom = {}
    dom['domain'] = domain
    dom['suffix'] = suffix
    dom['full'] = full
    dom['scheme'] = scheme
    dom['fqdn'] = fqdn
    return dom

