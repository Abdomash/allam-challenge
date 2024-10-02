class Extractor:
    @staticmethod
    def extract(shatr):
        # Logic to extract Qafiya type and Wazn type from the generated shatr
        qafiya_type = Extractor.extract_qafiya(shatr)
        wazn_type = Extractor.extract_wazn(shatr)
        return qafiya_type, wazn_type

    @staticmethod
    def extract_qafiya(shatr):
        # Mock logic to extract Qafiya type
        return "qafiya_type"

    @staticmethod
    def extract_wazn(shatr):
        # Mock logic to extract Wazn type
        return "wazn_type"