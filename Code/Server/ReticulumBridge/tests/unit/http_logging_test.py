from __future__ import annotations

from fastapi.testclient import TestClient
from loguru import logger
from pydantic import BaseModel
from reticulumbridge import create_app


class RequestPayload(BaseModel):
    count: int


def test_http_responses_are_logged_with_status_codes():
    app = create_app()

    @app.post('/validation')
    def validate_payload(payload: RequestPayload):
        return payload

    messages = []
    sink_id = logger.add(
        lambda message: messages.append(str(message)),
        format='{message}',
        level='INFO',
    )
    try:
        client = TestClient(app)
        assert client.get('/api/health').status_code == 200
        assert client.post(
            '/validation', json={'count': 'not-an-integer'},
        ).status_code == 422
    finally:
        logger.remove(sink_id)

    assert any(
        'HTTP GET /api/health -> 200' in
        message for message in messages
    )
    assert any(
        'HTTP POST /validation -> 422' in
        message for message in messages
    )
