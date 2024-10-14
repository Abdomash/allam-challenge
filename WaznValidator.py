class WaznValidator:
    def __init__(self):
        pass


if __name__ == "__main__":
    w = WaznValidator()
    print(w.validate_wazn("G1G1G0G1G0G1G1G0G1G0G1G0G1G1G0G1G1G1G0G1G1G0", "w"))
    print(w.validate_wazn("G1G1G0G1B0G1G1G0G1G0G1G0G1G1G0G1G1G1G0G1G1G0", "r"))
    print(w.validate_wazn("G1G1G0G1G0G1G1G0G1G0G1G0G1G1G0G1G1G1G0G1G1R0", ""))
    print(w.validate_wazn("G1G1B0G1G0R1G1G0G1G0G1Y0G1G1G0G1G1G1R0G1G1G0", ""))

