import os.path
import sys

import bolt

import pythern.about as about

bolt.register_task("default", ["pip", "ut"])
bolt.register_task("clear-pyc", ["delete-pyc.source", "delete-pyc.tests"])
bolt.register_task("ct", ["conttest"])
bolt.register_task("ut", ["clear-pyc", "shell.pytest"])

# CI/CD tasks
bolt.register_task("run-unit-tests", ["clear-pyc", "shell.pytest.coverage"])

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, about.project)
TEST_DIR = os.path.join(PROJECT_ROOT, "tests")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
COVERAGE_DIR = os.path.join(OUTPUT_DIR, "coverage")


config = {
    "pip": {
        "command": "install",
        "options": {
            "r": os.path.join(PROJECT_ROOT, "requirements.txt"),
        },
    },
    "shell": {
        "pytest": {
            "command": sys.executable,
            "arguments": ["-m", "pytest", TEST_DIR],
            "coverage": {
                "arguments": [
                    "-m",
                    "pytest",
                    f"--cov={about.project}",
                    "--cov-report",
                    f"html:{COVERAGE_DIR}",
                    TEST_DIR,
                ]
            },
        },
    },
    "delete-pyc": {
        "recursive": True,
        "source": {
            "sourcedir": SRC_DIR,
        },
        "tests": {
            "sourcedir": TEST_DIR,
        },
    },
    "mkdir": {
        "directory": OUTPUT_DIR,
    },
    "conttest": {"task": "ut"},
}
