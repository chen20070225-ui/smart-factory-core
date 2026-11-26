import pytest

from smart_factory_core.models import Job


def test_job_creation(job):
    assert job.job_id == "A01"
    assert job.priority == 3
    assert job.status == "waiting"


def test_job_str(job):
    assert str(job) == "工單 A01（優先級 3）"


def test_job_priority_must_be_positive():
    with pytest.raises(ValueError):
        Job("A01", 0)


def test_job_priority_error_message():
    with pytest.raises(ValueError, match="priority"):
        Job("A01", -1)