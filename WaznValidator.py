class WaznValidator:
    def __init__(self, feedback_generator):
        self.feedback_generator = feedback_generator

    def validate_wazn(self, current_wazn, previous_wazn=None):
        # Validation logic for Wazn type
        if current_wazn == "valid_wazn":  # Replace with actual validation logic
            return True
        else:
            feedback = self.feedback_generator.generate_feedback("wazn", current_wazn)
            return False, feedback