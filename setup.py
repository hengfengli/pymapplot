"""
PyMapPlot
--------------
Overlays on map tiles in Python. 
"""
from setuptools import setup

setup(
    name='pymapplot',
    version='0.0.1',
    url='https://github.com/HengfengLi/pymapplot',
    license='MIT',
    author='Hengfeng Li',
    author_email='hengf.li@gmail.com',
    description=('Overlays on map tiles in Python. '),
    long_description=__doc__,
    packages=['pymapplot'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    test_suite="tests",
    classifiers=[
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
