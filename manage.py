#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from pathlib import Path
import sys

def main():
    """Run administrative tasks."""
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(os.path.join(BASE_DIR, '.environ'))
    is_server = bool(os.getenv('IS_SERVER').lower() == 'true')
    if is_server:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development_settings')
        
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
