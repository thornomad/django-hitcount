#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import pytest

DEFAULT_ARGS = [ 'tests' ]

sys.path.append(os.path.dirname(__file__))

def exit_on_failure(ret, message=None):
    if ret:
        sys.exit(ret)

def run_django_tests(args):
    """This will only work with a later version of Django (1.8?)"""
    from django.core.exceptions import ImproperlyConfigured

    try:
        from django.test.utils import get_runner
        from tests.conftest import pytest_configure

        settings = pytest_configure()
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        exit_on_failure(test_runner.run_tests(args))

    except ImproperlyConfigured:
        sys.exit('TEST #FAIL: The --django arg has only been tested with 1.8')

if __name__ == "__main__":
    args = DEFAULT_ARGS.append(sys.argv)

    try:
        sys.argv.remove('--django')
    except ValueError:
        args = DEFAULT_ARGS.append(sys.argv)
        exit_on_failure(pytest.main(args))
    else:
        args = DEFAULT_ARGS.append(sys.argv)
        run_django_tests(args)
