# tests/test_ci_env.py
from tests.utils import fake_http_call,FakeResponse    # ⬅️ le helper ci‑dessus

def test_fake_response_headers_and_json():
    resp = fake_http_call("http://x/login")
    assert resp.status == 404
    assert hasattr(resp, "headers")
    import asyncio
    assert asyncio.run(resp.json()) == {'status': 'KO', 'error': 'Service not implemented', 'error_description': 'No Mock found'}

def test_fake_response_headers_json():
    resp = FakeResponse(200, {})
    assert resp.headers["Content-Type"] == "application/json"
