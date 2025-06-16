import pytest


@pytest.fixture(autouse=True)
def mock_backend(monkeypatch):
    # Mocka endpoints críticos para rodar Playwright sem backend real
    monkeypatch.setenv("MOCK_BACKEND", "1")
    yield


@pytest.fixture(scope="session")
def playwright_server():
    # Inicia um servidor HTTP fake para Playwright
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import threading
    import os

    os.chdir("gui")  # Serve arquivos da interface
    server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    thread.join()
