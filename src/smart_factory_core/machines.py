import logging
from dataclasses import dataclass

from smart_factory_core.errors import MachineDownError
from smart_factory_core.models import Job

logger = logging.getLogger(__name__)

@dataclass
class AssemblyProcessor:
    station_type: str
    task_name = "裝貨作業"

    def process(self, machine_id: str, job: str) -> None:
      logger.info("%s(%s站)正在組裝%s",machine_id,self.station_type,job)


@dataclass
class PaintProcessor:
    color: str
    task_name = "噴漆作業"

    def process(self, machine_id: str, job: str) -> None:
       logger.info("%s正在以%s為%s噴漆",machine_id,self.color,job)

@dataclass
class Machine:
    machine_id: str
    processor: PaintProcessor | AssemblyProcessor
    current_job: Job | None = None
    status: str = "stopped"

    def start(self) -> None:
        self.status = "running"
        logger.info("%s已開機",self.machine_id)

    def stop(self) -> None:
        self.status = "stopped"
        logger.info("%s已關機",self.machine_id)


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
        self.current_job = job
        job.status = "running"
        logger.info("%s 開始處理 %s", self.machine_id, job)
        self.processor.process(self.machine_id, job.job_id)