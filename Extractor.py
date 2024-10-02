class Extractor:
    def __init__(self):
        pass

    def extract(self, shatr):
        qafiya_type = self.extract_qafiya(shatr)
        wazn_type = self.extract_wazn(shatr)
        return qafiya_type, wazn_type

    def extract_qafiya(self, shatr):
        # TODO
        return None

    def extract_wazn(self, shatr):
        # TODO
        return None