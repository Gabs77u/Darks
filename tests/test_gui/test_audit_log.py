import pytest
from gui.audit_log import AuditLog


def test_audit_log_creation():
    log = AuditLog()
    assert log is not None
