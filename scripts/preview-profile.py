"""Preview the profile README locally: python scripts/preview-profile.py."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import mimetypes

import markdown


ROOT = Path(__file__).resolve().parents[1]
ASSETS = (ROOT / "assets").resolve()
STYLE = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; background: #f6f8fa; color: #1f2328;
  font: 16px/1.5 -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
article { max-width: 900px; margin: 24px auto; padding: 32px;
  background: #fff; border: 1px solid #d1d9e0; border-radius: 6px; }
h1 { font-size: 30px; padding-bottom: 8px; border-bottom: 1px solid #d1d9e0; }
h3 { margin-top: 24px; font-size: 20px; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
p { margin: 16px 0; }
img { max-width: 100%; height: auto; }
summary { cursor: pointer; }
li { margin: 6px 0; }
@media (max-width: 600px) { article { margin: 0; padding: 16px; border: 0; } }
"""


def render():
    source = (ROOT / "README.md").read_text(encoding="utf-8")
    # GitHub renders Markdown inside details; Python-Markdown needs this flag.
    source = source.replace("<details>", '<details markdown="1">')
    content = markdown.markdown(source, extensions=["extra", "sane_lists"])
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Enmao Diao — GitHub profile preview</title>'
        f"<style>{STYLE}</style></head><body><article>{content}</article></body></html>"
    ).encode("utf-8")


class PreviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path in ("/", "/index.html"):
            return self.send_data(render(), "text/html; charset=utf-8")
        if path.startswith("/assets/"):
            target = (ASSETS / path.removeprefix("/assets/")).resolve()
            if target.is_relative_to(ASSETS) and target.is_file():
                content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
                return self.send_data(target.read_bytes(), content_type)
        self.send_error(404)

    def send_data(self, body, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8766)
    arguments = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", arguments.port), PreviewHandler)
    print(f"Profile preview: http://127.0.0.1:{arguments.port}/", flush=True)
    print("Refresh after editing README.md. Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
