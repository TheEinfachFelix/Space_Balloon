from __future__ import annotations

import streamlit as st


def render() -> None:
    """Zeigt den aktuellen Status des Ballons an."""
    with st.container(border=True):
        st.subheader('Logs')

        st.text('Hier werden die aktuellen Logs des Ballons angezeigt.')

        st.success('Telemetrieverbindung aktiv')
