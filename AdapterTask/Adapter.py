import xml.etree.ElementTree as ET
import json
import statistics
from abc import ABC, abstractmethod

class DataProvider(ABC):
    @abstractmethod
    def get_data(self):
        pass

class XMLDataProvider:
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def load_xml_data(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        records = []
        for q in root.findall("quote"):
            try:
                record = {
                    "name": q.get("f25"),
                    "price": float(q.get("f6")),
                    "change": float(q.get("f14")),
                    "change_percent": float(q.get("f15")),
                    "high": float(q.get("f2")),
                    "low": float(q.get("f3"))
                }
                records.append(record)
            except (TypeError, ValueError):
                continue
        return records

class XMLtoJSONAdapter(DataProvider):
    def __init__(self, xml_data_provider: XMLDataProvider):
        self.xml_data_provider = xml_data_provider

    def get_data(self):
        return self.xml_data_provider.load_xml_data()

class DataAnalyzer:
    def __init__(self, provider: DataProvider):
        self.provider = provider

    def analyze(self):
        records = self.provider.get_data()
        avg_change_percent = sum(r["change_percent"] for r in records) / len(records)
        avg_high = sum(r["high"] for r in records) / len(records)
        avg_low = sum(r["low"] for r in records) / len(records)

        print("Średnia zmiana procentowa (z XML):", round(avg_change_percent, 3))
        print("Średnia cena HIGH (z XML):", round(avg_high, 3))
        print("Średnia cena LOW (z XML):", round(avg_low, 3))
        json_data = json.dumps(records, indent=2)
        parsed_json = json.loads(json_data)

        changes = [r["change"] for r in parsed_json if r["change"] >= 0]
        changes_percent = [r["change_percent"] for r in parsed_json if r["change_percent"] >= 0]

        var_change = statistics.variance(changes) if len(changes) > 1 else 0
        var_change_percent = statistics.variance(changes_percent) if len(changes_percent) > 1 else 0

        print("\n[JSON] Wariancja zmian (change):", round(var_change, 3))
        print("[JSON] Wariancja zmian procentowych (change%):", round(var_change_percent, 3))

def main():
    xml_service = XMLDataProvider("data.xml")
    adapter = XMLtoJSONAdapter(xml_service)
    analyzer = DataAnalyzer(adapter)
    analyzer.analyze()

if __name__ == "__main__":
    main()
