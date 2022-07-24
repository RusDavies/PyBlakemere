from PyBlakemere.PyCodeScanning.Common.OnboarderBase import OnboarderBase
from github import Github #, GithubException, RateLimitExceededException
from PyGitHubMapper.RateLimiter import GitHubRateLimiter
import pandas as pd
from pathlib import Path


class Onboarder_CodeQL(OnboarderBase):
    def __init__(self, config={}):
        super().__init__(config=config)
        self._extract_config()
        self.df = None
        #---

    def _extract_config(self):
        self._basename     = self._config.get('general.basename',     None)
        self._credentials  = self._config.get('security.creds',       None)
        self._organization = self._config.get('general.org',          None)
        self._path         = self._config.get('general.path',         './')
        self._repo_regex   = self._config.get('general.repo_regex',   None)
        self._calls_min    = self._config.get('general.calls_min',    10)

    #
    # Initializers
    def __init_path(self):
        # Make sure path exits, before we spend hours only to fail
        if (self._basename != None):
            self._path = Path(self._path)
            if(not self._path.exists()):
                self._path.mkdir(parents=True, exist_ok=True)


    def __init_input_data(self):
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
        self.__init_input_data()
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
        if (basename != None):
            self.writeToFile(basename=basename, path=path)
        
        return 0


