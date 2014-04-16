from setuptools import setup, find_packages
import os

version = '1.0b3.dev0'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='vilaix.core',
      version=version,
      description="",
      long_description=README + "\n" + HISTORY,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='core vilaix',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/UPCnet/vilaix.core.git',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['vilaix'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'vilaix.theme',
          'plone.app.dexterity',
          'loremipsum',
          'upc.genweb.banners',
          'upc.genweb.logosfooter',
          'collective.portlet.twitter'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
