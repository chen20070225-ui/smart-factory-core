from smart_factory_core.factory import Factory
from smart_factory_core.machines import AssemblyProcessor, Machine, PaintProcessor
from smart_factory_core.models import Job


def main() -> None:
    factory = Factory()
    factory.add_machine(Machine("ASM-01", AssemblyProcessor("螺絲鎖附")))
    factory.add_machine(Machine("PNT-01", PaintProcessor("blue")))
    factory.add_machine(Machine("PNT-02", PaintProcessor("red")))

    for i in range(1, 6):
        factory.submit(Job(f"J{i}", i))

    print("--- 1. 全部關機時 dispatch ---")
    factory.dispatch()
    factory.report()

    print("\n--- 2. 開兩台機器後 dispatch ---")
    factory.machines["ASM-01"].start()
    factory.machines["PNT-01"].start()
    factory.dispatch()
    factory.report()

    print("\n--- 3. ASM-01 完工後再 dispatch ---")
    factory.machines["ASM-01"].finish()
    factory.dispatch()
    factory.report()

    print("\n--- 4. 重複的機器編號 ---")
    # 取消下面這行的註解，會看到 ValueError
    # factory.add_machine(Machine("ASM-01", AssemblyProcessor("螺絲鎖附")))


if __name__ == "__main__":
    main()