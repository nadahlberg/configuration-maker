from pathlib import Path
import json
import os
from dotenv import load_dotenv


def load_json(path):
    with open(str(path), 'r') as f:
        return json.loads(f.read())


def save_json(path, obj):
    with open(str(path), 'w') as w:
        w.write(json.dumps(obj, indent=4))


class Config():
    def __init__(self, path, config_keys, cli_command, autoload_env=True):
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.keys = config_keys
        self.cli_command = cli_command
        if autoload_env:
            load_dotenv()
            
    def load(self):
        config = {}
        if self.path.exists():
            try:
                config = load_json(self.path)
            except json.decoder.JSONDecodeError:
                self.path.unlink()
        for key in self.keys:
            value = os.environ.get(key.name, None)
            if value is None:
                value = config.get(key.name, None)
            if value is not None:
                if key.key_type == 'str':
                    value = str(value)
                if key.key_type == 'int':
                    value = int(value)
                if key.key_type == 'path':
                    value = Path(value)
            config[key.name] = value

        return config
    
    def update(self, group=None, reset=False):
        config = self.load()
        
        print('\n\n(leave blank to keep existing value)')
        for key in self.keys:
            if key.group == group or group is None:
                current_value = None
                if not reset:
                    current_value = config.get(key.name, None)
                prompt = key.name
                if current_value is not None:
                    masked_value = str(current_value)
                    mask_len = max([len(masked_value) - 4, 0])
                    masked_value = '*' * mask_len + masked_value[mask_len:]
                    prompt += ' [{}]'.format(masked_value)
                if key.description is not None:
                    print(key.description)
                value = input(prompt + ': ')
                print()
                if not value:
                    value = current_value
                else:
                    if key.key_type == 'str':
                        value = str(value)
                    elif key.key_type == 'int':
                        value = int(value)
                    elif key.key_type == 'path':
                        value = Path(value).resolve()

                config[key.name] = None if value is None else str(value)
        
        save_json(self.path, config)
        print('configuration saved to %s' % self.path)
    
    def __getitem__(self, key_name):
        config = self.load()
        value = config.get(key_name, None)
        if value is None:
            keys = [x for x in self.keys if x.name == key_name]
            if len(keys) > 0:
                group = keys[0].group or ''
                raise KeyError('The key "%s" is not in your configuration file, run "%s %s" to set value.' % (key_name, self.cli_command, group))
            else:
                raise KeyError('"%s" is not a valid configuration key' % key_name)
        return value
    
    def __str__(self):
        return str(self.load())


class ConfigKey():
    def __init__(self, name, group=None, key_type='str', description=None):
        self.name = name
        self.group = group
        allowed_key_types = ['str', 'int', 'path']
        if key_type not in allowed_key_types:
            raise ValueError('key_type must be one of %s' % allowed_key_types)
        self.key_type = key_type
        self.description = description




