class FeedbackGenerator:
    def generate_feedback(self, type, invalid_item, expected_item, invalid_shatr):
        if type == "qafiya":
            return self.qafiya_feedback(invalid_item, expected_item, invalid_shatr)
        
        if type == "wazn":
            return self.wazn_feedback(invalid_item, expected_item, invalid_shatr)
    
    def qafiya_feedback(self, invalid_qafiya, expected_qafiya, invalid_shatr):
        # TODO

        text = ""
        text += f"الشطر المدخل {invalid_shatr} غير صحيح. "
        text += f"القافية المدخلة {invalid_qafiya} غير صحيحة. "
        text += f"القافية الصحيحة هي {expected_qafiya}. "
        
        return text

    def wazn_feedback(self, invalid_wazn, expected_wazn, invalid_shatr):
        # TODO

        text = ""
        text += f"الشطر المدخل {invalid_shatr} غير صحيح. "
        text += f"الوزن المدخل {invalid_wazn} غير صحيح. "
        text += f"الوزن الصحيح هو {expected_wazn}. "

        return text
