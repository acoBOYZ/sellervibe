from celery import Task
import os
from pathlib import Path
import logging


class LoggingTask(Task):
    logger = None

    @classmethod
    def init(cls) -> None:
        cls.logger = logging.getLogger(__name__)

    @classmethod
    def setup_loggers(cls, logger, *args, **kwargs):
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        APP_DIR = Path(__file__).resolve().parent
        handler = logging.FileHandler(os.path.join(APP_DIR, 'celery.log'))
        handler.setFormatter(formatter)

        cls.logger.addHandler(handler)
        cls.logger.propagate = False
    
    @classmethod
    def on_success(cls, retval, task_id, args, kwargs):
        info = f'Task success: {cls.name} [{task_id}]'
        cls.logger.info(info)

    @classmethod
    def on_failure(cls, exc, task_id, args, kwargs, einfo):
        error = f'Task failure: {cls.name} [{task_id}] - Error: {exc}'
        cls.logger.error(error)
    
    @classmethod
    def on_retry(cls, exc, task_id, args, kwargs, einfo):
        warning = f'Task retry: {cls.name} [{task_id}] - Error: {exc}'
        cls.logger.warning(warning)
    
    @classmethod
    def after_return(cls, status, retval, task_id, args, kwargs, einfo):
        debug = f'Task return: {cls.name} [{task_id}] - {status}'
        cls.logger.debug(debug)

    @classmethod
    def on_start(cls, task_id, args, kwargs):
        debug = f'Task start: {cls.name} [{task_id}]'
        cls.logger.debug(debug)