from celery import Task

class LoggingTask(Task):
    def __init__(self, logger) -> None:
        self.logger = logger

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