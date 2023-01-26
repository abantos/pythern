import os.path

import bolt

import pythern.about as about

bolt.register_task('default', ['pip', 'ut'])
bolt.register_task('clear-pyc', ['delete-pyc.source', 'delete-pyc.tests'])
bolt.register_task('ut', ['clear-pyc', 'nose'])
bolt.register_task('ct', ['conttest'])

# CI/CD tasks
bolt.register_task('run-unit-tests', ['clear-pyc', 'mkdir', 'nose.ci'])



PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, about.project)
TEST_DIR = os.path.join(PROJECT_ROOT, 'tests')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
COVERAGE_DIR = os.path.join(OUTPUT_DIR, 'coverage')


config = {
    'pip': {
        'command': 'install',
        'options': {
            'r': os.path.join(PROJECT_ROOT, 'requirements.txt'),
        },
    },
    'delete-pyc': {
        'recursive': True,
        'source': {
            'sourcedir': SRC_DIR,
        },
        'tests': {
            'sourcedir': TEST_DIR,
        },
    },
    'mkdir': {
        'directory': OUTPUT_DIR,
    },
    'nose': {
        'directory': TEST_DIR,
        'ci': {
            'options': {
                'with-xunit': True,
                'xunit-file': os.path.join(OUTPUT_DIR, 'unit_tests_log.xml'),
                'with-coverage': True,
                'cover-erase': True,
                'cover-package': about.project,
                'cover-html': True,
                'cover-html-dir': COVERAGE_DIR,
                'cover-branches': True,
            },
        }
    },
    'conttest': {
        'task': 'ut'
    }
}
