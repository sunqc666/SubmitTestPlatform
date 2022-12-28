"""

======================

@author:sunqiucheng

@time:2022/11/14:7:11 下午

======================

"""
from flask import g, render_template, request
from functools import wraps



class CompareVersion:
    def compare_data_version(self, func):
        @wraps(func)
        def warpper(*args, **kwargs):
            if hasattr(g, 'user'):
                return func(*args, **kwargs)
            else:
                return render_template('login.html')
        return warpper