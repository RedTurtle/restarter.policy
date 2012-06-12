from setuptools import setup, find_packages

version = '1.0'

long_description = (
    open('README.md').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='restarter.policy',
      version=version,
      description="restarter project policy package",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='earthquake plone terremoto',
      author='RedTurtle',
      author_email='info@redturtle.it',
      url='http://www.redturtle.it',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['restarter', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          #'z3c.jbot',
          #'eea.facetednavigation',
          #'collective.disqus',
          #'sc.social.like',
          #'collective.contentleadimage',
          #'Products.PloneKeywordManager',
          #'plonesocial.auth.rpx',
          #'cioppino.twothumbs',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone

      [zopectl.command]
      statistics = restarter.policy:processor
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["templer.localcommands"],
      )
