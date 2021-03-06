#!/usr/bin/python
# -*- coding: utf-8 -*-

import werkzeug.contrib.cache
import logging

__version__ = '0.0.1'

memory_cache = werkzeug.contrib.cache.SimpleCache()

def clear_cache(cache=None):
    cache = cache or memory_cache
    cache.clear()

def cached(cache=memory_cache, timeout=3600):
    import functools
    def decorator(func):
        @functools.wraps(func)
        def cached_func(*args, **kwargs):
            keys = [func.__name__, str(args), str(kwargs.values())]
            cache_key = ';'.join(keys)
            cached = cache.get(cache_key)
            if cached: return cached
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            return result
        return cached_func
    return decorator
    
	
import unittest
    
class CachingTests(unittest.TestCase):
    def test_cached(self):
        from werkzeug.contrib.cache import SimpleCache
        cache = SimpleCache()
        func = lambda : True
        cached_func = cached(cache)(func)
        
        self.assertTrue(cached_func())
        func = lambda : False
        self.assertTrue(cached_func())
