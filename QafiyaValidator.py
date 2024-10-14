class QafiyaValidator:
    def __init__(self):
        pass

    def validate_qafiya(self, current_qafiya, previous_qafiya=None):
        return True
        # TODO: implement validation
        # if previous_qafiya is None:
        #     return True        
        # if current_qafiya == previous_qafiya:
        #     return True
        # else:
        #     return False
        if previous_qafiya is None:
            return True
        return (current_qafiya == previous_qafiya)
