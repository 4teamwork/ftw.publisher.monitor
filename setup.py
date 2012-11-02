from setuptools import setup, find_packages
import os

version = '2.0b1-dev'
maintainer = 'Jonas Baumann'

tests_require = [
    'ftw.testing',
    'plone.app.testing',
    'plone.testing',
    'unittest2',
    ]


setup(name='ftw.publisher.monitor',
      version=version,
      description='An ftw.publisher addon for monitoring the '
      'publisher queue and alerting when there is a problem.',

      long_description=open('README.rst').read() + '\n' +
      open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw publisher monitoring',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.publisher.monitor',

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
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
