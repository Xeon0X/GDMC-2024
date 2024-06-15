import yaml

class YamlReader:
    def __init__(self, yaml_file):
        self.data = self._load_yaml(yaml_file)
        
    def _load_yaml(self, yaml_file : str):
        with open(yaml_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        
        return data_loaded