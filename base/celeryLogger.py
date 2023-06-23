from celery import Task
from celery.signals import after_setup_logger
import os
from pathlib import Path
import logging

class LoggingTask(Task):
    def init(self) -> None:
        self.logger = logging.getLogger(__name__)

    
    @after_setup_logger.connect
    def setup_loggers(self, logger, *args, **kwargs):
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        APP_DIR = Path(__file__).resolve().parent
        handler = logging.FileHandler(os.path.join(APP_DIR, 'celery.log'))
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.propagate = False

    
    def on_success(self, retval, task_id, args, kwargs):
        info = f'Task success: {self.name} [{task_id}]'
        self.logger.info(info)

    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        error = f'Task failure: {self.name} [{task_id}] - Error: {exc}'
        self.logger.error(error)

    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        warning = f'Task retry: {self.name} [{task_id}] - Error: {exc}'
        self.logger.warning(warning)

    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        debug = f'Task return: {self.name} [{task_id}] - {status}'
        self.logger.debug(debug)

    
    def on_start(self, task_id, args, kwargs):
        debug = f'Task start: {self.name} [{task_id}]'
        self.logger.debug(debug)