#!/usr/bin/env python3
"""로컬 개발 서버.

Claude Design에서 내보낸 .dc.html 을 그대로 브라우저에 띄운다.
.dc.html 은 support.js 런타임이 필요하고, 그 런타임이 React/Babel 을
CDN에서 받아오므로 file:// 이 아니라 http:// 로 열어야 한다.

    python3 serve.py            # http://localhost:5173
    python3 serve.py 8080       # 포트 지정
"""

import functools
import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).parent
SITE_DIR = ROOT / "AWS Student Builder 웹사이트"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5173


def find_entry(site_dir):
    """디렉터리 안의 .dc.html 진입점을 찾는다 (파일명이 바뀌어도 동작하도록)."""
    candidates = sorted(site_dir.glob("*.dc.html")) or sorted(site_dir.glob("*.html"))
    if not candidates:
        sys.exit(f"[error] {site_dir} 안에 html 파일이 없습니다.")
    return candidates[0].name


class Handler(http.server.SimpleHTTPRequestHandler):
    entry = None

    def translate_path(self, path):
        # "/" 요청을 실제 진입점 파일로 넘긴다.
        if path.split("?")[0].split("#")[0] in ("/", "/index.html"):
            path = "/" + self.entry
        return super().translate_path(path)

    def end_headers(self):
        # 매번 최신 파일을 보도록 캐시를 끈다 (재내보내기 후 새로고침만 하면 반영됨).
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "404" in (fmt % args):
            super().log_message(fmt, *args)


def main():
    if not SITE_DIR.is_dir():
        sys.exit(f"[error] 사이트 폴더를 찾을 수 없습니다: {SITE_DIR}")

    Handler.entry = find_entry(SITE_DIR)
    handler = functools.partial(Handler, directory=str(SITE_DIR))
    socketserver.TCPServer.allow_reuse_address = True

    url = f"http://localhost:{PORT}"
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"  entry : {Handler.entry}")
        print(f"  serve : {url}")
        print("  중지  : Ctrl+C\n")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료했습니다.")


if __name__ == "__main__":
    main()
