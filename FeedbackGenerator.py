class FeedbackGenerator:
    def generate_feedback(self, type_, invalid_verse, invalid_item=None, previous_feedback=None):
        # Generate feedback for an invalid Wazn or Qafiya
        return f"Feedback for {type_}: {invalid_item} is invalid. Try again."