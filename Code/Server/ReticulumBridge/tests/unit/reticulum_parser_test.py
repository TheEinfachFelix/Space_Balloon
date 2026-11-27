from __future__ import annotations

import json

import pytest
from pydantic import ValidationError
from reticulumbridge.core.reticulum_parser import compress
from reticulumbridge.core.reticulum_parser import decompress
from reticulumbridge.core.reticulum_parser import typeify
from reticulumbridge.models import CommandData
from reticulumbridge.models import ResponseData
from reticulumbridge.models import TelemetryData


@pytest.mark.parametrize(
    ('model', 'message_type'),
    [
        (
            CommandData(timestamp='now', id=12, node_name='balloon'),
            'command',
        ),
        (
            ResponseData(timestamp='now', id=12, node_name='balloon'),
            'response',
        ),
        (
            TelemetryData(
                timestamp='now',
                id=12,
                node_name='balloon',
                test_field_1=12.5,
            ),
            'telemetry',
        ),
    ],
)
def test_typeify_returns_model_for_message_type(model, message_type):
    message = json.dumps({
        'type': message_type,
        'data': model.model_dump(mode='json'),
    })

    result = typeify(message)

    assert type(result) is type(model)
    assert result == model


@pytest.mark.parametrize(
    'model',
    [
        CommandData(timestamp='now', id=12, node_name='balloon'),
        ResponseData(timestamp='now', id=12, node_name='balloon'),
        TelemetryData(
            timestamp='now',
            id=12,
            node_name='balloon',
            test_field_1=12.5,
        ),
    ],
)
def test_compress_and_decompress_round_trip(model):
    assert decompress(compress(model)) == model


def test_typeify_rejects_unknown_message_type():
    with pytest.raises(ValidationError):
        typeify('{"type": "unknown", "data": {}}')


def test_typeify_rejects_non_object_data():
    with pytest.raises(ValidationError):
        typeify('{"type": "command", "data": []}')


def test_typeify_validates_model_fields():
    with pytest.raises(ValidationError):
        typeify('{"type": "command", "data": {"timestamp": "now"}}')


def test_compress_serializes_typed_envelope():
    command = CommandData(timestamp='now', id=12, node_name='balloon')

    assert json.loads(compress(command)) == {
        'type': 'command',
        'data': {
            'timestamp': 'now',
            'id': 12,
            'node_name': 'balloon',
            'command': 'ping',
            'parameters': {},
        },
    }
