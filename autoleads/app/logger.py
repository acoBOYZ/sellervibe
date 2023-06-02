import os
import json

class Logger:
    def __init__(self, debug=False, error_file='err.log.json'):
        self.debug = debug
        self.error_file = error_file

        if os.path.exists(error_file):
            os.remove(error_file)

        if not os.path.isfile(error_file):
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps({}))

    def debug_log(self, *values: object):
        if self.debug:
            print('SCRAP_LOG:', *values)

    def write_error(self, func_name, error):
        with open(self.error_file, 'r+', encoding='utf-8') as f:
            try:
                errors = json.load(f)
            except json.JSONDecodeError:
                self.debug_log('Invalid JSON data in file, creating a new empty dict')
                errors = {}

            errors[func_name] = str(error)
            f.seek(0)
            json.dump(errors, f)
            f.truncate()
    
    def log_and_write_error(self, description, error):
        if error is not None:
            self.debug_log(f'{description}: {error}')
            self.write_error(description, error)