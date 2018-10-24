import os.path

import bolt

bolt.register_task('default', ['pip', 'ut'])
bolt.register_task('clear-pyc', ['delete-pyc.source', 'delete-pyc.tests'])
bolt.register_task('ut', ['clear-pyc', 'nose'])
bolt.register_task('ct', ['conttest'])



PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, 'dichotomy')
TEST_DIR = os.path.join(PROJECT_ROOT, 'tests')


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
    'nose': {
        'directory': TEST_DIR
    },
    'conttest': {
        'task': 'ut'
    }
}
