import os.path
from setuptools import setup, find_packages

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as _f:
        contents = _f.read()
    return contents

setup(
    name="backlight-cli",
    version="0.1",
    author="andrew young",
    author_email="ayoung@thewulf.org",
    description="change the keyboard and monitor backlight brightness",
    keywords="backlight",
    long_description=read("README.md"),
    packages=find_packages(exclude=["tests", "tests.*"]),
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "backlight-cli = backlight.backlight:run"
        ]
    }
)
