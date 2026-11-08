class Job:
    """一張工單：priority 不能小於 1"""

    def __init__(self, job_id: str, priority: int, status: str = "waiting") -> None:
        self.job_id = job_id
        self.priority = priority  # 這行會走下面的 setter
        self.status = status

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        if value < 1:
            raise ValueError(f"priority 必須 >= 1，收到 {value}")
        self._priority = value

    def __repr__(self) -> str:
        return f"Job(job_id={self.job_id!r}, priority={self.priority}, status={self.status!r})"

    def __str__(self) -> str:
        return f"工單 {self.job_id}（優先級 {self.priority}）"