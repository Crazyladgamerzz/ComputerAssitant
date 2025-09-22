
#Dev config
DEBUG_GRAPH = True
SKIP_SECURITY = False
CONFIRM_EVERY_LOOP = True
MAX_SCRATCHPAD_LEN = -1
OLLAMA_URL = 'localhost:11434'

import json
import os
from pydantic import BaseModel

user_config_path = os.path.join(os.path.dirname(__file__),'config_.json')

#User config
class Config(BaseModel):
    EXEC_HUMAN_CONFIRMATION: bool
    MAX_ITERATIONS: int

    def set_max_iterations(self,max_iterations):
        try:
            self.MAX_ITERATIONS = int(max_iterations)
            update_config()
            return 'Successfully updated max iterations'
        except Exception as e:
            return str(e)
        
    def set_human_confirmation(self,b):
        try:
            self.EXEC_HUMAN_CONFIRMATION = bool(b)
            update_config()
            return 'Successfully updated human confirmation'
        except Exception as e:
            return str(e)

def load_config():
    with open(user_config_path, "r") as f:
        global config
        config = Config(**json.load(f))

def update_config():
    with open(user_config_path, "w") as f:
        global config
        json.dump(config.model_dump(), f, indent=2)
    #load_config()