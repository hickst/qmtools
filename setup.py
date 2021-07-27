from setuptools import setup, find_packages

setup(
    name='QMView',
    version='0.0.8',
    packages=find_packages(),
    # package_data={'qmview': ['resources/*.txt', 'resources/*.properties']},
    # include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'run_traffic  = qmview.traffic_light_cli:main'
        ]
    },
)
