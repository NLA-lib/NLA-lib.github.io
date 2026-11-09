"""Serve a built Explorer locally at the same /explore/ mount as GitHub Pages."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class ExploreHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = Path(self.translate_path(self.path))
        compressed = Path(str(path) + '.gz')
        if 'gzip' in self.headers.get('Accept-Encoding', '') and compressed.is_file():
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(str(path)))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
            self.send_header('Content-Length', str(compressed.stat().st_size))
            if '?v=' in self.path:
                self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
            self.end_headers()
            return compressed.open('rb')
        return super().send_head()

    def translate_path(self, path):
        return super().translate_path(path if (Path(self.directory) / 'explore').is_dir()
                                      else path.removeprefix('/explore'))

    def do_GET(self):
        if self.path == '/' and not (Path(self.directory) / 'explore').is_dir():
            self.send_response(302)
            self.send_header('Location', '/explore/')
            self.end_headers()
            return
        super().do_GET()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent / '_site')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    if not (args.directory / 'index.html').is_file():
        parser.error('Build the site before starting a preview.')
    server = ThreadingHTTPServer(('127.0.0.1', args.port),
                                partial(ExploreHandler, directory=str(args.directory.resolve())))
    print(f'Local: http://127.0.0.1:{server.server_port}/explore/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
