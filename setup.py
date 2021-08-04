from setuptools import setup, find_packages

setup(
    name='QMTools',
    version='0.0.11',
    packages=find_packages(),
    package_data={'qmtools': ['resources/*.txt', 'resources/*.properties']},
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'run_traffic = qmtools.qmview.traffic_light_cli:main',
            'run_fetcher = qmtools.qmfetcher.fetcher_cli:main'
        ]
    },
)
