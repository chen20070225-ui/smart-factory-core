import pytest

from smart_factory_core.machines import AssemblyProcessor, Machine
from smart_factory_core.models import Job


@pytest.fixture
def machine() -> Machine:
    return Machine("ASM-01", AssemblyProcessor("螺絲鎖附"))


@pytest.fixture
def job() -> Job:
    return Job("A01", 3)