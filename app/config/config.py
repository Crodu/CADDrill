import json
import os
# from ..utils.motorUtils import setupConfig

def load_config(config_path='config.json'):
  if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration file not found: {config_path}")

  with open(config_path, 'r') as config_file:
    config = json.load(config_file)

  return config

def replace_config(config_path='config.json', new_config={}, controller=None):
  with open(config_path, 'w') as config_file:
    json.dump(new_config, config_file, indent=2)
  controller.setupConfig(new_config)
  return new_config

def set_config_value(config_path='config.json', key=None, value=None, controller=None):
  config = load_config(config_path)
  
  keys = key.split('.')
  sub_config = config
  for k in keys[:-1]:
    if k not in sub_config:
      sub_config[k] = {}
    sub_config = sub_config[k]
  
  sub_config[keys[-1]] = value
  
  return replace_config(config_path, config, controller)
  