from setuptools import setup, find_packages

setup(
    name='k8tie',
    version='0.1',
    py_modules=['k8tie'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'yaml',
        'Jinja2',
    ],
    entry_points='''
        [console_scripts]
        k8tie=k8tie:cli
    ''',
)
