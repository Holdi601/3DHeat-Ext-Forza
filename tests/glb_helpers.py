"""Reading a written `.glb` back, for the tests (from 3DHeat GameFiles' tests/test_glb.py)."""

from __future__ import annotations

import json
import struct


def read_back(path):
    raw = path.read_bytes()
    magic, version, total = struct.unpack_from("<III", raw, 0)
    assert magic == 0x46546C67
    assert version == 2
    assert total == len(raw), "the declared length is not the file's"
    json_length, json_tag = struct.unpack_from("<II", raw, 12)
    assert json_tag == 0x4E4F534A
    document = json.loads(raw[20 : 20 + json_length])
    binary_length, binary_tag = struct.unpack_from("<II", raw, 20 + json_length)
    assert binary_tag == 0x004E4942
    binary = raw[28 + json_length : 28 + json_length + binary_length]
    return document, binary
