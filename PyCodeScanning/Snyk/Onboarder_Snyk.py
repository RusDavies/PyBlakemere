from PyBlakemere.PyCodeScanning.Common.OnboarderBase import OnboarderBase
import snyk
import pandas as pd
from pathlib import Path


class Onboarder_Snyk(OnboarderBase):
    def __init__(self, config={}):
        super().__init__(config=config)
        self._extract_config()
        self.df = None
        #---

    def _extract_config(self):
        self._credentials           = self._config.get('security.creds',          None)
        self._organization          = self._config.get('jobspec.org',             None)
        self._repo_regex            = self._config.get('jobspec.repo_regex',      None)
        self._report_basename       = self._config.get('jobspec.report_basename', None)
        self._report_path           = self._config.get('jobspec.report_path',     './')
        self._log_to_screen         = self._config.get('logging.log_to_screen',   True)
        self._log_to_file           = self._config.get('logging.log_to_file',     True)

    #
    # Initializers
    def __init_path(self):
        # Make sure path exits, before we spend hours only to fail
        if (self._basename != None):
            Path(self._path).mkdir(parents=True, exist_ok=True)


    def __init_tracking_data(self):
        # Load the input data file
        self._data = None
        return


    def __init_gitHub(self):
        # Set up the GitHub object and rate limiter
        if(not self._creds):
            raise ValueError('An API Token must be provided to use the GitHub API')
        self._gh = Github(login_or_token=self._credentials, verify=self._verify_ssl)

        if (self._organization != None):
            self._gh = self._gh.get_organization(self._organization)

        self._rateLimiter = GitHubRateLimiter(self._gh, self._calls_min)

        # Fitler the repos list using the repo_regex
        self._repos = self._gh.get_repos()
        if(self._repo_regex):
            pass # TODO! 

        return 


    #
    # Task runners
    def _pre_task_runner(self):
        self.__init_path()
        self.__init_tracking_data()
        self.__init_gitHub()
        return


    def _task_runner(self):
        for repo in self._repos:
            self._rateLimiter.run(self, '_task', repo)

       
    def _task(self, repo):
        
        # Check whether the repo already has a ghas file
        # If exists
            # Mark it as already in place (May need review to determing that it's on a cron)
        # Else 
            # Create a file from template
            # Push the file into location via the API 

        return None



    #
    # Result processing 

    def _pre_processing(self, *args, **kargs):
        # Convert the data gathered to a data frame
        self.df = pd.DataFrame( self._task_runner_result ).transpose(); 


    # 
    # Reporting

    def _task_set_reporting(self, *args, **kargs):
        # If we're given a basename, then write out to file now
        if (self._basename != None):
            self.writeToFile(basename=self._basename, path=self._path)
        
        return 0


