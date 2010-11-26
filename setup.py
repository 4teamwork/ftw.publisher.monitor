from setuptools import setup, find_packages
import os

version = '1.0'
maintainer = 'Jonas Baumann'

tests_require = [
    'collective.testcaselayer',
    ]


setup(name='ftw.publisher.monitor',
      version=version,
      description="Publisher monitoring system for monitoring the queue" + \
          ' (Maintainer: %s)' % maintainer,
      long_description=open("README.txt").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='ftw publisher monitoring',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='http://psc.4teamwork.ch/dist/ftw-publisher-monitor',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.publisher'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'z3c.autoinclude',
        'ftw.publisher.sender',
        'plone.fieldsets',
        # -*- Extra requirements: -*-
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
