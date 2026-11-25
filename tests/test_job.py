from smart_factory_core.models import Job


def test_job_creation():
    job = Job("A01",3)
    assert job.job_id == "A01"
    assert job.priority ==3
    assert job.status =="waiting"


def test_job_str():
    job = Job("A01", 3)
    assert str(job) == "工單 A01（優先級 3）"