"""
Container entrypoint: start the Prometheus metrics server immediately, then run
Streamlit in the same process. This way Prometheus can scrape port 8001 as soon
as the container starts, before anyone has opened the UI.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from metrics import start_metrics_server

start_metrics_server()

from streamlit.web import cli as stcli

if __name__ == "__main__":
    app = os.path.join(os.path.dirname(os.path.abspath(__file__)), "streamlit_app.py")
    sys.argv = [
        "streamlit", "run", app,
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
    ]
    sys.exit(stcli.main())
