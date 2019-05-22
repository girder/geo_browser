from setuptools import setup

setup(
    name='girder-geobrowser',
    version='0.0.1',
    description='',
    maintainer='Kitware, Inc.',
    maintainer_email='kitware@kitware.com',
    entry_points={
        'girder.plugin': [
            'geobrowser = geobrowser_plugin:GeoBrowserPlugin'
        ]
    },
    install_requires=[
        'shapely'
    ],
)
