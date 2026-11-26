import pytest

from smart_factory_core.factory import Factory
from smart_factory_core.machines import AssemblyProcessor, Machine, PaintProcessor
from smart_factory_core.models import Job


@pytest.fixture
def factory() -> Factory:
    f = Factory()
    f.add_machine(Machine("ASM-01", AssemblyProcessor("螺絲鎖附")))
    f.add_machine(Machine("PNT-01", PaintProcessor("blue")))
    return f


def test_add_machine_rejects_duplicate_id(factory):
    with pytest.raises(ValueError):
        factory.add_machine(Machine("ASM-01", AssemblyProcessor("x")))


def test_submit_keeps_order(factory):
    factory.submit(Job("J1", 1))
    factory.submit(Job("J2", 2))
    assert [j.job_id for j in factory.queue] == ["J1", "J2"]


def test_dispatch_skips_stopped_machines(factory):
    factory.submit(Job("J1", 1))
    factory.dispatch()
    assert len(factory.queue) == 1


def test_dispatch_gives_first_job_to_idle_machine(factory):
    factory.submit(Job("J1", 1))
    factory.submit(Job("J2", 2))
    factory.machines["ASM-01"].start()
    factory.dispatch()
    assert factory.machines["ASM-01"].current_job.job_id == "J1"
    assert [j.job_id for j in factory.queue] == ["J2"]


def test_busy_machine_does_not_get_second_job(factory):
    for i in range(1, 4):
        factory.submit(Job(f"J{i}", i))
    factory.machines["ASM-01"].start()
    factory.dispatch()
    factory.dispatch()
    assert len(factory.queue) == 2


def test_finish_makes_machine_idle_again(factory):
    factory.submit(Job("J1", 1))
    machine = factory.machines["ASM-01"]
    machine.start()
    factory.dispatch()
    machine.finish()
    assert machine.is_idle is True


def test_status_count(factory):
    factory.machines["ASM-01"].start()
    assert factory.status_count() == {"running": 1, "stopped": 1}


def test_machines_by_type(factory):
    groups = factory.machines_by_type()
    assert [m.machine_id for m in groups["AssemblyProcessor"]] == ["ASM-01"]
    assert [m.machine_id for m in groups["PaintProcessor"]] == ["PNT-01"]


def test_report_prints_queue_length(factory, capsys):
    factory.submit(Job("J1", 1))
    factory.report()
    out = capsys.readouterr().out
    assert "等待中工單：1" in out