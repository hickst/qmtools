from setuptools import setup, find_packages

setup(
    name='QMTools',
    version='1.5.0',
    packages=find_packages(),
    package_data={'qmtools': ['qmtools/qmviolin/static/*']},
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'qmtraffic = qmtools.qmview.traffic_light_cli:main',
            'qmfetcher = qmtools.qmfetcher.fetcher_cli:main',
            'qmviolin  = qmtools.qmviolin.violin_cli:main'
        ]
    },
)
