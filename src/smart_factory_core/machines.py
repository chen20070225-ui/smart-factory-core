from dataclasses import dataclass

from smart_factory_core.errors import MachineDownError
from smart_factory_core.models import Job


@dataclass
class AssemblyProcessor:
    station_type: str
    task_name = "裝貨作業"

    def process(self, machine_id: str, job: str) -> None:
        print(f"[裝貨作業]機器{machine_id}({self.station_type}站)正在組裝工件{job}")


@dataclass
class PaintProcessor:
    color: str
    task_name = "噴漆作業"

    def process(self, machine_id: str, job: str) -> None:
        print(f"[噴漆作業]機器{machine_id}正在以{self.color}為{job}工件噴漆")


@dataclass
class Machine:
    machine_id: str
    processor: PaintProcessor | AssemblyProcessor
    current_job: Job | None = None
    status: str = "stopped"

    def start(self) -> None:
        self.status = "running"
        print(f"[系統訊息]{self.machine_id}機器已開機")

    def stop(self) -> None:
        self.status = "stopped"
        print(f"[系統訊息]{self.machine_id}機器已關機")

    @property
    def is_idle(self) -> bool:
        return self.status == "running" and self.current_job is None

    def finish(self) -> None:
        if self.current_job is not None:
            self.current_job.status = "done"
            self.current_job = None
    

    @property
    def is_idle(self) -> bool:
        return self.status == "running" and self.current_job is None

    def finish(self) -> None:
        if self.current_job is not None:
            self.current_job.status = "done"
            self.current_job = None

    def process(self, job: Job) -> None:
        if self.status != "running":
                       raise MachineDownError(
                f"{self.machine_id}尚未開機，無法進行{self.processor.task_name}"
            )
        job.status = "running"
        print(f"[系統訊息]{self.machine_id}開始處理{job}")
        self.processor.process(self.machine_id,job.job_id)