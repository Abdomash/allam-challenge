class QafiyaValidator:
    def __init__(self, feedback_generator):
        self.feedback_generator = feedback_generator

    def validate_qafiya(self, qafiya):
        # Validation logic for Qafiya type
        if qafiya == "valid_qafiya":  # Replace with actual validation logic
            return True
        else:
            feedback = self.feedback_generator.generate_feedback("qafiya", qafiya)
            return False, feedback