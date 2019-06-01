#!/usr/bin/env python
# -*- coding=utf-8 -*-

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from flask import request, redirect, url_for

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc



def redirect_back(defualt='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(defualt, **kwargs))

