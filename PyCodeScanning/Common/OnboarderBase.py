import urllib3
import logging


class OnboarderBase():
    def __init__(self, config={}):
        self._config = config 

        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())

        self._verify_ssl = self._config.get('verify_ssl', True)
        if (not self._verify_ssl):
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.log.warn('SSL verification is disabled and warnings silenced')

        self.df = None

    # Entry point
    def run(self):

        # Run the task set
        self._pre_task_runner()
        self.result = self._task_runner()
        self._post_task_runner()

        # Process the results
        self._pre_processing()
        self._processing()
        self._post_processing()

        # Report on the results
        self._pre_task_set_reporting()
        self._task_set_reporting()
        self._post_task_set_reporting()

        return 0


    # Task runners
    def _pre_task_runner(self):
        return None

    def _task_runner(self):
        return None

    def _post_task_runner(self):
        return None

    def _task(self, *args, **kargs):
        return None


    # Result processing
    def _pre_processing(self):
        return None

    def _processing(self):
        return None

    def _post_processing(self):
        return None


    # Reporting
    def _pre_task_set_reporting(self):
        return None

    def _task_set_reporting(self):
        return None

    def _post_task_set_reporting(self):
        return None
