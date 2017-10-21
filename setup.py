from setuptools import setup, find_packages

setup(
    name='k8ie',
    version='0.1',
    py_modules=['k8ie'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Jinja2',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        k8ie=k8ie:cli
    ''',
)
