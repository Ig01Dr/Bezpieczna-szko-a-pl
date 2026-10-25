"""Allow `python -m safeschool`."""

from .app import app
from .config import get_settings

if __name__ == "__main__":
    s = get_settings()
    app.run(host=s.host, port=s.port, debug=s.debug)
