import os
from dotenv import load_dotenv

def custom_loadenv():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    env_local_path = os.path.join(project_root, '.env.local')
    env_path = os.path.join(project_root, '.env')

    if os.path.exists(env_local_path):
        return load_dotenv(dotenv_path=env_local_path, override=True)
    
    if os.path.exists(env_path):
        return load_dotenv(dotenv_path=env_path)
    
    return load_dotenv()
