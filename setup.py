try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'auto updater',
	'author': 'Antoine Orozco',
	'url': 'URL to get it at.',
	'download_url': 'Where to download it.',
	'author_email': 'orozco_antoine@yahoo.fr'
	'version': '0.1',
	'install_requires': ['nose', 'pyinode', 'gevent'],
	'packages': ['auto_updater'],
	'scripts': [],
	'name': 'auto_updater'
}

setup(**config)
