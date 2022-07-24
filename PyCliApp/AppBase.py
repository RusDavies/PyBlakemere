from pathlib import Path
import logging
import logging.config
from benedict import benedict

class AppBase:
    def __init__(self, *args):
        self._app  = args[0]
        self._args = args[1:]
        self._config = None
        self._access_token = None

        self._get_config()
        self._get_creds()
        self._config_logging()
        self._get_access_token()

        self._verify_ssl = self._config.get('general.verify_ssl', True)


    def usage(self):
        app_basename = Path(self._app).name
        print('\nUsage: [python] {} <config.yml>\n'.format(app_basename))
        return 0


    def _get_config(self):
        if (len(self._args) != 1):
            self.usage()
            raise ValueError('ERROR: Expected 1 argument but {} were given'.format(len(self._args)))

        if ( Path(self._args[0]).exists() == False):
            raise ValueError("ERROR: The file '{}' does not exist".format(self._args[0]))

        self._config = benedict.from_yaml(self._args[0])

        if (self._config == None):
            raise ValueError("Failed to import config file '{}'".format(self._args[0]))

        self._check_config()

        return 0


    def _get_creds(self):
        creds_file = self._config.get('security.creds_file', None)
        
        if (creds_file is not None):       
            creds_file = Path(creds_file).expanduser()
            if (not creds_file.exists()):
                raise ValueError("'security.creds_file' was set as '{}', which does not exist.".format(creds_file))

            with open(creds_file) as f:
                self._creds = "".join(f.readlines())
        
        return 0


    def _check_config(self):
        config_errors = []
        if (self._config == None):
            raise ValueError("The config was unexpectedly None")

        mandatory_items = ['logging']

        for item in mandatory_items:
            if (self._config.get(item, None) == None):
                config_errors.append(item)
        
        if (len(config_errors) > 0):
            msg = "The following mandatory items are missing from the configuration: '{}'."
            raise ValueError(msg.format(config_errors))

        return 0


    def _config_logging(self):
        log_config_file = self._config.get('logging.log_config_file', None)
        
        if ( log_config_file != None ):
            # in this case, we're passed a config file for logging, which we'll use
            logging.config.dictConfig(benedict.from_yaml(log_config_file))
        else:
            # In this case, there is no separate config file, so we expect the logging 
            # config to be directly in the main config file under 'logging'. 
            logging.config.dictConfig(self._config.get('logging'))
        
        self.log = logging.getLogger()
    
        return 0

   
    def run(self):
        return 0