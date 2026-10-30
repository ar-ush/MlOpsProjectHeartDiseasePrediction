"""
Prometheus metrics shared by the Streamlit app and its launcher.

Defined in a plain module (not in the Streamlit script) so that the counter and
the metrics server are created once per *process*. Streamlit re-runs the app
script for every browser session, but imported modules are cached.
"""

from prometheus_client import Counter, start_http_server

METRICS_PORT = 8001

PREDICTION_COUNTER = Counter(
    "streamlit_predictions_total",
    "Total predictions made via Streamlit UI",
)

_started = False


def start_metrics_server(port: int = METRICS_PORT) -> None:
    """Start the /metrics HTTP server once; safe to call repeatedly."""
    global _started
    if _started:
        return
    try:
        start_http_server(port)
    except OSError:
        pass   # port already bound by another process
    _started = True
