from setuptools import setup

setup(
    name='cleverthumbnailer',
    version='0.1.0',
    description='Selects interesting and relevant short thumbnails for '
                'longer audio tracks',
    author='Jon Tutcher',
    author_email='jon.tutcher@bbc.co.uk',
    packages=['cleverthumbnailer', 'cleverthumbnailer.featureextractor'],
    entry_points={
        'console_scripts': [
            'cleverthumbnailer =  cleverthumbnailer.__main__:main'
        ]
    },
    install_requires=[
        'numpy',
        'qmsegmenter',
        'pysox',
        'enum',

    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 or ' +
        'later (GPLv2+)'
    ]
)
