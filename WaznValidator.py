class WaznValidator:
    def __init__(self):
        pass

    def validate_wazn(self, current_wazn, current_wazn_name, previous_wazn=None): #returns index of mistake
        if previous_wazn is not None:
            if current_wazn_name != previous_wazn:
                return 0 #bahr is completely wrong, regenrate from the start
        
        #check error in the arood writing (R,G,B,Y)
        #G = correct, Y,B,R = wrong
        errors = [current_wazn.find("R"), current_wazn.find("B"), current_wazn.find("Y")]
        if max(errors) == -1:
            return -1 #no errors!
        else:
            while min(errors) == -1:
                errors[errors.index(min(errors))] = 9999
            return min(errors) // 2 #since there is 0G1G! divide by 2!


if __name__ == "__main__":
    w = WaznValidator()
    print(w.validate_wazn("G1G1G0G1G0G1G1G0G1G0G1G0G1G1G0G1G1G1G0G1G1G0", "w"))
    print(w.validate_wazn("G1G1G0G1B0G1G1G0G1G0G1G0G1G1G0G1G1G1G0G1G1G0", "r"))
    print(w.validate_wazn("G1G1G0G1G0G1G1G0G1G0G1G0G1G1G0G1G1G1G0G1G1R0", ""))
    print(w.validate_wazn("G1G1B0G1G0R1G1G0G1G0G1Y0G1G1G0G1G1G1R0G1G1G0", ""))

