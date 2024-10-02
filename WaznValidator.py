class WaznValidator:
    def __init__(self, feedback_generator):
        pass

    def validate_wazn(self, current_wazn, previous_wazn=None):
        # Validation logic for Wazn type
        if current_wazn == previous_wazn:
            return True
        else:
            return False