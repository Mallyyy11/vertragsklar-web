# app/middleware_embed.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os

# Erlaubte Eltern-Seiten (die Seite, die unser iFrame enthält)
# Für den Start reicht Squarespace. Wenn du später eine eigene Domain nutzt, ergänzen:
#   https://deinedomain.com  https://www.deinedomain.com
ALLOWED_PARENTS = [
    "https://*.squarespace.com",
]

class FrameAncestorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        csp_sources = " ".join(ALLOWED_PARENTS)
        response.headers["Content-Security-Policy"] = f"default-src 'self'; frame-ancestors {csp_sources};"
        # X-Frame-Options absichtlich NICHT auf DENY setzen
        return response
