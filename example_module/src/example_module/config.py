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
