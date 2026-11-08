from smart_factory_core.machines import AssemblyProcessor, Machine, PaintProcessor
from smart_factory_core.models import Job


def main() -> None:
    asm = Machine(machine_id="ASM-01", processor=AssemblyProcessor(station_type="螺絲鎖附"))
    abc = Machine(machine_id="AAA-01", processor=PaintProcessor(color="blue"))

    job1 = Job("A01", 3)
    job2 = Job("A02", 1)
    job3 = Job("A03", 2)

    print("--- 1. 沒開機會被擋下 ---")
    asm.process(job1)

    print("\n--- 2. 開機後處理 ---")
    asm.start()
    abc.start()
    asm.process(job1)
    abc.process(job2)

    print("\n--- 3. 執行中替換加工邏輯 ---")
    asm.processor = PaintProcessor(color="red")
    asm.process(job3)

    print("\n--- 4. __str__ 與 __repr__ ---")
    print(job1)
    print([job1])
    print(asm)

    # 5. 取消下面這行的註解，會看到 ValueError
    # Job("A04", 0)


if __name__ == "__main__":
    main()