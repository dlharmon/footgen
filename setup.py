from distutils.core import setup

classifiers = [
    'Development Status :: 3',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Topic :: Scientific/Engineering',
]

setup(name='footgen',
      version='0.1a',
      description="Footprint generator for Kicad and gEDA in Python",
      author="Darrell Harmon",
      author_email="darrell@harmoninstruments.com",
      url="http://dlharmon.com/geda/footgen.html",
      packages=['footgen'],
      license='GPLv3+',
      classifiers=classifiers,
)
