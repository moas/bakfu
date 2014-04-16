# -*- coding: utf-8 -*-
import re
__processors__ = {}

def get_processor(name, regexp=None):
    if regexp == None:
        return __processors__.get(name, None)
    else:
        regexp = re.compile(regexp)
        return [key for key in __processors__.keys()
                if regexp.match(key)]


def register(name):
    def decorator(processor):
        global __processors__
        __processors__[name] = processor
        processor.registered_name = name
        return processor
    return decorator

'''

import bakfu.data.base
from bakfu.core.routes import __processors__
__processors__
bakfu.data.base.BaseDataSource
'''

