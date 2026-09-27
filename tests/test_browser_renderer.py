from pathlib import Path


ROOT = Path(__file__).parents[1]
RENDERER = (ROOT / "web" / "renderer.html").read_text(encoding="utf-8")


def test_renderer_uses_browser_isolation_and_timeout():
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")

    assert 'sandbox="allow-scripts"' in app_source
    assert "new Worker" in RENDERER
    assert "LOAD_TIMEOUT_MS = 45000" in RENDERER
    assert "TIMEOUT_MS = 10000" in RENDERER
    assert "activeWorker.terminate()" in RENDERER


def test_renderer_blocks_server_and_active_output_access():
    assert "default-src 'none'" in RENDERER
    assert "script-src 'unsafe-inline' 'wasm-unsafe-eval'" in RENDERER
    assert "form-action 'none'" in RENDERER
    assert 'format="png"' in RENDERER
    assert "data:image/png;base64" in RENDERER


def test_renderer_validates_generated_python():
    assert "ast.parse" in RENDERER
    assert '"open"' in RENDERER
    assert '"exec"' in RENDERER
    assert '"__import__"' in RENDERER
    assert "ALLOWED_MODULES" in RENDERER
