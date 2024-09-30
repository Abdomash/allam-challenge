class Extractor:
    @staticmethod
    def extract(verse):
        # Logic to extract Qafiya type and Wazn type from the generated verse
        qafiya_type = Extractor.extract_qafiya(verse)
        wazn_type = Extractor.extract_wazn(verse)
        return qafiya_type, wazn_type

    @staticmethod
    def extract_qafiya(verse):
        # Mock logic to extract Qafiya type
        return "qafiya_type"

    @staticmethod
    def extract_wazn(verse):
        # Mock logic to extract Wazn type
        return "wazn_type"