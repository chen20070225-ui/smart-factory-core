import pytest

from smart_factory_core.errors import MachineDownError


def test_machine_starts_stopped(machine):
    assert machine.status == "stopped"


def test_start_changes_status_to_running(machine):
    machine.start()
    assert machine.status == "running"


def test_stop_changes_status_to_stopped(machine):
    machine.start()
    machine.stop()
    assert machine.status == "stopped"


def test_process_makes_machine_busy(machine, job):
    machine.start()
    machine.process(job)
    assert machine.current_job is job
    assert machine.is_idle is False


def test_process_on_stopped_machine_raises(machine, job):
    with pytest.raises(MachineDownError):
        machine.process(job)
    assert machine.current_job is None