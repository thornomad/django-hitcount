#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import subprocess

import pytest
# from flake8.main import main as flake8_main

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


def flake8_main(args):
    print('Flake8 code linting ...')
    ret = subprocess.call(['flake8'] + args)
    print('Flake8 failed' if ret else 'Flake8 passed')
    return ret


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('extra_args', metavar="args", type=str, nargs='*',
                        help='Additional arguments to pass to the test runner')
    parser.add_argument('--django',
                        help='Use Django test runner (>=1.8). Additional arguments in the form of tests.test_filename',
                        action='store_true')
    parser.add_argument('--no-flake8',
                        help='Disable flake8 testing',
                        action='store_true')
    parser.add_argument('--flake8-only',
                        help='Only perform flake8 testing',
                        action='store_true')

    args = parser.parse_args()
    extra_args = args.extra_args

    if not args.flake8_only:
        if args.django:
            run_django_tests(extra_args)
            extra_args = []
        else:
            exit_on_failure(pytest.main(extra_args))

    if not args.no_flake8:
        exit_on_failure(flake8_main(extra_args))
