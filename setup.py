from setuptools import setup, find_packages

setup(
	name='configuration-maker',
	version='0.1.4',    
	description='Create configuration files for Python modules that can be updated by CLI',
	url='https://github.com/nadahlberg/configuration-maker',
	author='Nathan Dahlberg',
	author_email='nadahlberg@gmail.com',
	package_dir={'': 'src'},
	packages=find_packages('src'),
	install_requires=[
		'pathlib',
		'click',
		'python-dotenv',
	],
)
