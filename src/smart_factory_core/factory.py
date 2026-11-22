from collections import Counter, defaultdict, deque

from smart_factory_core.machines import Machine
from smart_factory_core.models import Job


class Factory:
    def __init__(self) -> None:
        self.machines: dict[str, Machine] = {}
        self.queue: deque[Job] = deque()

    def add_machine(self, machine: Machine) -> None:
        if machine.machine_id in self.machines:
            raise ValueError(f"機器編號重複：{machine.machine_id}")
        self.machines[machine.machine_id] = machine

    def submit(self, job: Job) -> None:
        self.queue.append(job)

    def dispatch(self) -> None:
        for machine in self.machines.values():
            if not self.queue:
                break
            if machine.is_idle:
                machine.process(self.queue.popleft())

    def status_count(self) -> Counter[str]:
        return Counter(m.status for m in self.machines.values())

    def machines_by_type(self) -> defaultdict[str, list[Machine]]:
        groups: defaultdict[str, list[Machine]] = defaultdict(list)
        for m in self.machines.values():
            groups[type(m.processor).__name__].append(m)
        return groups

    def report(self) -> None:
        print(f"機器狀態：{dict(self.status_count())}，等待中工單：{len(self.queue)}")
        for kind, ms in self.machines_by_type().items():
            print(f"  {kind}：{[m.machine_id for m in ms]}")