# -*- coding: utf-8 -*-
from contextlib import contextmanager
import os

from ploceus.utils._collections import ThreadLocalRegistry


class Context(dict): pass


def new_context():
    rv = Context()
    rv['extra_vars'] = {}
    return rv

# TODO: scope
class ContextManager(object):

    def __init__(self):
        self.context = ThreadLocalRegistry(new_context)


    def get_context(self):
        return self.context()

def cd(path):

    from ploceus.runtime import context_manager
    context = context_manager.get_context()

    path = path.replace(' ', '\ ')
    if 'cwd' in context and \
       not path.startswith('/') and \
       not path.startswith('~'):
        new_cwd = os.path.join(context['cwd'], path)
    else:
        new_cwd = path

    return _setenv('cwd', new_cwd)


def local_mode():
    return _setenv('local_mode', True)


@contextmanager
def _setenv(name, value):

    from ploceus.runtime import context_manager
    context = context_manager.get_context()

    previous = context.get(name)
    context[name] = value
    yield
    if previous:
        context[name] = previous
        return
    context[name] = None
