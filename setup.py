from setuptools import setup, find_packages

setup(
    name='QMView',
    version='0.0.2',
    packages=find_packages(),
    # package_data={'qmview': ['resources/*.txt', 'resources/*.properties']},
    # include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'test_traffic    = test.test_traffic_light:main'
        ]
    },
)
