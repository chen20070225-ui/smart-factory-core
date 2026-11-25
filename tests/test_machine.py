from smart_factory_core.machines import AssemblyProcessor, Machine
from smart_factory_core.models import Job

def make_machine():
    return Machine("ASM-01",AssemblyProcessor("螺絲鎖附"))

def test_machine_starts_stopped():
    machine = make_machine()
    assert machine.status =="stopped"

def test_start_changes_status_to_running():
    machine = make_machine()
    machine.start()
    assert machine.status == "running"

def test_process_makes_machine_busy():
    machine = make_machine()
    machine.start()
    job = Job("A01",3)
    machine.process(job)
    assert machine.current_job is job
    assert machine.is_idle is False

def test_stop_changes_status_to_stopped():
    machine = make_machine()
    machine.start()
    machine.stop()
    assert machine.status == "stopped"