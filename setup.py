from setuptools import setup, find_packages
import os

version = '2.0b1-dev'
maintainer = 'Jonas Baumann'

tests_require = [
    'pyquery',
    'unittest2',
    'mocker',
    'zope.configuration',
    'plone.testing',
    'ftw.testing',
    'plone.app.testing',
    ]


setup(name='ftw.publisher.monitor',
      version=version,
      description='An ftw.publisher addon for monitoring the '
      'publisher queue and alerting when there is a problem.',

      long_description=open('README.rst').read() + '\n' +
      open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw publisher monitoring',
      author='4teamwork AG',
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

        'zope.annotation',
        'zope.component',
        'zope.formlib',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.app.component',
        'ZODB3',
        'Zope2',

        'plone.fieldsets',
        'plone.app.layout',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.CMFPlone',

        'ftw.publisher.sender',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
