#!/usr/bin/env python
import argparse
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Django Model Revisions test suite.")
    parser.add_argument(
        'modules', nargs='*', metavar='module',
        help='Optional path(s) to test modules; e.g. "i18n" or '
             '"i18n.tests.TranslationTests.test_lazy_objects".',
    )
    parser.add_argument(
        '-v', '--verbosity', default=1, type=int, choices=[0, 1, 2, 3],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output',
    )
    parser.add_argument(
        '-k', '--keepdb', action='store_true', dest='keepdb', default=False,
        help='Tells Django to preserve the test database between runs.',
    )

    options = parser.parse_args()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=options.verbosity,
        keepdb=options.keepdb
    )
    failures = test_runner.run_tests(options.modules or ["tests"])
    sys.exit(bool(failures))
