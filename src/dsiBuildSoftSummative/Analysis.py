from typing import Any, Optional, Final
import matplotlib.pyplot as plt
import yaml
import requests
import datetime
import logging


class Analysis():

    INIT_LOG_FILE_NAME_PREFIX: Final = 'dsiBuildSoftSummative'
    DATA_URL: Final = 'https://osdr.nasa.gov/osdr/data/osd/files/201'
    rawData = None

    def __init__(self, analysis_config: str) -> None:

        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}
        # load each config file and update the config dictionary
        for path in paths:
            try:
                with open(path, 'r') as f:
                    this_config = yaml.safe_load(f)
                    config.update(this_config)   
            except FileNotFoundError as e:    
                e.add_note(f'The file {path} cannot be found')
                raise e
            except Exception as e:
                e.add_note(f'Error while loading configuration files')
                raise e             
        self.config = config

        # Init logging
        try:
            logging_level = logging.DEBUG if config['verbose_log'] else logging.WARNING
            # Initialize logging module
            now = datetime.datetime.now()
            logFileName = f'{self.INIT_LOG_FILE_NAME_PREFIX}_{now.strftime("%Y_%m_%d_%H%M")}.log'
            logging.basicConfig(
                level=logging_level,
                handlers=[logging.StreamHandler(),
                          logging.FileHandler(logFileName)])
        except Exception as e:
            e.add_note(f'Error initializing log file')
            raise e   

    def load_data(self) -> None:
        try:
            self.rawData = requests.get(url=f'{self.DATA_URL}?api_key={self.config['api_key']}')
        except Exception as e:
            e.add_note(f'Error Loading Data from API {self.DATA_URL}')
            raise e   

    def compute_analysis(self) -> Any:
        pass

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        pass

    def notify_done(self, message: str) -> None:
        pass