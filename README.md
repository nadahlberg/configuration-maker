# Configuration Maker
Create customizable configurations for your Python modules that can be updated with a simple CLI

`pip install configuration-maker`

## Overview
Configuration Maker allows you to inject customizable groups of configuration variables into your Python modules.  These variables can be used to store API keys, data paths, and other information that your module may rely on but which need to be defined by the user.  While they serve a similar use-case to environment variables, these configuration variables have a few additional features:

- Easily implement a command-line interface for setting the values of configuration keys, automatically raise an informative error with the appropriate command when accessing a key that has not been set.
- Configuration keys are stored globally on the users device and can be accessed by the module from anywhere.
- Override saved configuration keys with enviroment variables for custom or localized configurations.
- Automatically enforce datatypes with built-in support for Path variables.
- Bundle configuration keys into groups and allow the user to run the CLI for groups individually.

## Tutorial

The `example_module` directory includes a minimal start.  This tutorial will briefly cover this module.

### Define a Configuration Object
See `example_module/src/example_module/config.py`

Define a `Config` by providing a path where the configuration should be stored as JSON, a list of `ConfigKey` objects, and the CLI command that should be called to update the configuration.  The `ConfigKey` objects only require the `name` of the key, but you can optionally assign them to a `group`, provide a `key_type` (currently 'str', 'int', and 'path' supported), and a `description`.

````
from pathlib import Path
from configuration_maker import Config, ConfigKey

keys = [
	ConfigKey(
		name='NAME',
		group='info'
	),

	ConfigKey(
		name='DATA_DIR',
		group='info',
		key_type='path',
		description='directory to store data',
	),

	ConfigKey(
		name='SOME_NUMBER',
		group='info',
		key_type='int',
	),
]

config = Config(
	path=Path.home() / '.cache' / 'example_module' / 'config.json',
	config_keys=keys,
	cli_command='example_module configure',
)
````

### Make the Configuration Object Accessible
See `example_module/src/example_module/__init__.py`

Import `config` into `__init__.py` so that it can be accessed anywhere as `example_module.config`.  You can access the stored values by indexing the configuration object with the name of a key like `example_module.config['SOME_KEY']`

````
from example_module.config import config
from example_module.cli import main as cli
````

### Create the CLI
See `example_module/src/example_module/cli.py`

The configuration object has an update function that can be used to walk the user through setting or editing the saved configuration.  Here we wrap this in as a click command.

````
import click
import example_module

@click.command()
def configure():
    example_module.config.update()

@click.group()
def main():
    pass

main.add_command(configure)

if __name__ == '__main__':
    configure()
````

The `config.update` function also accepts arguments for `group`, which only update the keys within the chosen group, and `reset` which will override any already saved values for the configuration variables being updates.  You might incorporate these into your command like function as such:

````
@click.command()
@click.argument('group')
@click.option('--reset/--no-reset', default=False, help='Delete existing group keys in config')
def configure(group, reset):
    example_module.config.update(group, reset)
````

### Testing Usage

The CLI is made accessible by adding an entry point in `example_module/setup.py`:

````
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
````

And we add a command to test things out in `example_module/src/example_module/cli.py`

````
@click.command()
def test():
    print('NAME saved as', example_module.config['NAME'])
    print('DATA_DIR located at', example_module.config['DATA_DIR'])
    print('SOME_NUMBER saved as', example_module.config['SOME_NUMBER'])

...

main.add_command(test)
````

Now we are ready to test.  From command line you can expect the following:

````
example_module test
> KeyError: 'The key "NAME" is not in your configuration file, run "example_module configure info" to set value.'

example_module configure

> (leave blank to keep existing value)
> NAME: Nathan
>
> directory to store data
> DATA_DIR: /path/to/data
>
> SOME_NUMBER: 42
>
> configuration saved to home/.cache/example_module/config.json

example_module test
> NAME saved as Nathan
> DATA_DIR located at /path/to/data
> SOME_NUMBER saved as 42
````

### Overriding Configuration Keys with Environment Variables
By default, a `.env` file will be automatically loaded from your working directory.  To disable this behavior you can set `autoload_env=False` when you initialize the `Config` object.  Any environment variable with the same name as configuration key will override the stored value for that configuration variable.

