"""Directly-wired mkdocs dev server.

Bypasses `mkdocs serve` CLI because its livereload registration doesn't
fire in this environment (watch() never gets called, observer never starts).
This wiring is equivalent to what `mkdocs.commands.serve.serve` does internally,
but calls `server.watch()` explicitly so the PollingObserver actually runs.

Usage:
    .venv/bin/python scripts/serve.py [-a HOST:PORT]
"""
from __future__ import annotations

import argparse
import logging
import tempfile
from urllib.parse import urlsplit

from mkdocs.commands.build import build
from mkdocs.config import load_config
from mkdocs.livereload import LiveReloadServer, _serve_url


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--dev-addr", default="0.0.0.0:8000")
    parser.add_argument("-f", "--config-file", default="mkdocs.yml")
    args = parser.parse_args()

    host, port_str = args.dev_addr.rsplit(":", 1)
    port = int(port_str)

    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")

    site_dir = tempfile.mkdtemp(prefix="mkdocs_")

    def get_config():
        return load_config(config_file=args.config_file, site_dir=site_dir)

    config = get_config()
    mount_path = urlsplit(config.site_url or "/").path
    config.site_url = serve_url = _serve_url(host, port, mount_path)

    def builder(config=None):
        logging.info("Building documentation...")
        if config is None:
            config = get_config()
            config.site_url = serve_url
        build(config, serve_url=serve_url)

    server = LiveReloadServer(
        builder=builder, host=host, port=port, root=site_dir, mount_path=mount_path
    )
    builder(config)
    server.watch(config.docs_dir)
    if config.config_file_path:
        server.watch(config.config_file_path)

    try:
        server.serve()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
