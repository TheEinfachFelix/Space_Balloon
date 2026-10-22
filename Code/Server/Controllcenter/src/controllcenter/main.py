from __future__ import annotations

import streamlit as st
from controllcenter.components import render_log_view
from loguru import logger

logger.info('Starting Controll Center...')

st.set_page_config(
    page_title='Ballon Control Center',
    page_icon='🎈',
    layout='wide',
)

st.title('Ballon Control Center')

render_log_view()

st.divider()

render_log_view()
