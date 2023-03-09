from setuptools import setup, find_namespace_packages

setup(
    name='qmtools',
    version='1.6.0',
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={"qmtools.qmviolin.static": ["*.css", "*.png"]},
    entry_points={
        'console_scripts': [
            'qmtools   = qmtools.qmtools:main',
            'qmtraffic = qmtools.qmview.traffic_light_cli:main',
            'qmfetcher = qmtools.qmfetcher.fetcher_cli:main',
            'qmviolin  = qmtools.qmviolin.violin_cli:main'
        ]
    },
)
