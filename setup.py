from setuptools import setup

setup(
    name="igconvert",
    author="Zhongren Gao",
    version='1.0',
    py_modules=['converter'],
    install_requires=[
        'Click',
        'fuzzywuzzy'
    ],
    entry_points='''
        [console_scripts]
        igconvert=src.converter_cmd:convert
    ''',
    include_package_data=True,
    package_data={
        '': ['*.json'],
    }
)