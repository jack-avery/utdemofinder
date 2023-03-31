import json
import os

CONFIG_PATH = "config.txt"
"""Path to the user config file to use"""

DEFAULT = {
    "demo_folder": False 
}

class Config:
    """
    Configuration class for UTDemoFinder.
    """

    demo_folder: str = False
    """Demo folder"""

    def read(self):
        """
        Read from `CONFIG_PATH` and return the contained json.

        Create the file with the default if it does not exist.
        """
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as cfgfile:
                cfg = json.loads(cfgfile.read())
        
        else:
            cfg = self.write(DEFAULT)
        
        self.demo_folder = cfg['demo_folder']
            
    def write(self, cfg: dict):
        """
        Write `cfg` to `CONFIG_PATH` and return what was written if successful.

        :param cfg: The configuration to write.
        """
        with open(CONFIG_PATH, "w") as cfgfile:
            cfgfile.write(json.dumps(self.json(), indent=4))
            return cfg
    
    def json(self):
        return {
            "demo_folder": self.demo_folder
        }

