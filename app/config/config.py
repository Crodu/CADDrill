import json
import os
from ..utils.motorUtils import setupConfig

def load_config(config_path='config.json'):
  if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration file not found: {config_path}")

  with open(config_path, 'r') as config_file:
    config = json.load(config_file)

  return config

def replace_config(config_path='config.json', new_config={}):
  with open(config_path, 'w') as config_file:
    json.dump(new_config, config_file, indent=2)
  setupConfig(new_config)
  return new_config