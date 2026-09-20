from dataclasses import dataclass, field

from dotenv import load_dotenv

@dataclass
class Conf:
    path: str
    dir: str
    table: str = "poose_migrations"

    @classmethod
    def get_env(): 
        pass




    
     
    