from setuptools import setup, find_packages, Command
from subprocess import check_call
import os


class BuildUICommand(Command):
    description = 'Build the standalone front end and include it in the sdist'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        dest = os.path.join(
                os.path.abspath('geobrowser_plugin'),
                'external_web_client')

        install = ['yarn', 'install']
        build = ['yarn', 'build']
        copy = ['cp', '-r', 'dist', dest]
        commands = [install, build, copy]

        os.chdir(os.path.abspath('gui'))
        for cmd in commands:
            check_call(cmd)


class CleanBuildCommand(Command):
    description = 'Clean the files generated by BuildUICommand'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        destDir = os.path.join(
                os.path.abspath('geobrowser_plugin'),
                'external_web_client')

        srcDir = os.path.join(
                os.path.abspath('gui'),
                'dist')

        removeDest = ['rm', '-rf', destDir]
        removeSrc = ['rm', '-rf', srcDir]
        commands = [removeDest, removeSrc]

        for cmd in commands:
            check_call(cmd)


with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='girder-geobrowser',
    version='0.2.3',
    description='Map-oriented custom Girder app'
                'for geospatial metadata browsing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/girder/geo_browser',
    maintainer='Kitware, Inc.',
    maintainer_email='kitware@kitware.com',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'shapely'
    ],
    entry_points={
        'girder.plugin': [
            'geobrowser = geobrowser_plugin:GeoBrowserPlugin'
        ],
        'girder.cli_plugins': [
            'extract-geospatial = geobrowser_plugin.extraction:extract'
        ]
    },
    cmdclass={
        'build_ui': BuildUICommand,
        'clean_build': CleanBuildCommand,
    }
)
