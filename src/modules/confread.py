#!/usr/bin/env python3

import configparser as cp
import os

default_config_path = "./powerplay.conf"
default_config_section = "database"

class confread():
    def __init__(self):
        '''
        This section initializes the class instance and immediatly reads the config file.
        For clearance, it does not check whether any values are filled in. It just reads.
        '''

        self.config = cp.ConfigParser()

        if os.path.exists(default_config_path):
            self.config.read(default_config_path)
        else:
            print(f"The config file does not exist. Please provide a compliant configuration file at: {default_config_path}")
            return

    def verify_integrity(self) -> bool:
        '''
        This section goes over the required keywords needed for a successful database connection.
        It does this by enumerating the config file and checking integrity.
        '''

        required = [
            "username",
            "password",
            "database",
            "hostname",
            "port",
        ]

        for kw in required:
            if kw in self.config[default_config_section]:

                if not self.config[default_config_section][kw]:
                    print(f"Section: {kw} exists but is not filled. Exiting...")
                    return False

            else:
                print(f"Section: {kw} - absent, exiting...")
                return False

            # Success round.
        return True

    def build_connstr(self) -> str:
        cnf = self.config[default_config_section]
        
        base_exp = f"postgresql://{cnf['username']}:{cnf['password']}@{cnf['hostname']}:{cnf['port']}/{cnf['database']}"

        return base_exp


