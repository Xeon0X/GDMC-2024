import json

class JsonReader:
    def __init__(self, json_file):
        self.data = self._load_json(json_file)
        
    def _load_json(self, json_file : str):
        f = open(json_file)
        js = json.load(f)
        
        return js