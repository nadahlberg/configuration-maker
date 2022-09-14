from setuptools import setup, find_packages

setup(
	name='example_module',
	version='0.1.0',
	package_dir={'': 'src'},
	packages=find_packages('src'),
	install_requires=[
		'configuration-maker',
		'click'
	],
	entry_points={
		'console_scripts': [
			'example_module = example_module:cli',
		],
	},
)