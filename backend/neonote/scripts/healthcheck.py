import httpx
import sys
import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

try:
    if (
        httpx.get(
            f"http://localhost:{8000 if ENVIRONMENT == 'dev' else 1717}/api/utils/health",
            timeout=5,
        ).status_code
        == 200
    ):
        sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
