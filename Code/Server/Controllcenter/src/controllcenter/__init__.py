from __future__ import annotations

import os
import sys

from controllcenter.dependencies import get_settings
from controllcenter.utils import setup_logging
from loguru import logger
from streamlit.web import cli


def main():
    setup_logging(get_settings())
    logger.info('Starting Controllcenter...')
    logger.debug('Setting up Streamlit CLI arguments...')
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'main.py')

    sys.argv = [
        'streamlit',
        'run',
        filename,
        '--server.headless=true',
    ]
    logger.debug(f"Streamlit CLI arguments: {sys.argv}")
    logger.info('Running Streamlit application...')
    raise SystemExit(cli.main())
