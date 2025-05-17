import xml.etree.ElementTree as ET
import json
import statistics


def xml_to_json(xml_file):
    tr = ET.parse(xml_file)
    root = tr.getroot()
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

def compute_xml_averages(records):
    avg_change_percent = sum(r["change_percent"] for r in records) / len(records)
    avg_high = sum(r["high"] for r in records) / len(records)
    avg_low = sum(r["low"] for r in records) / len(records)
    return avg_change_percent, avg_high, avg_low

def compute_json_variances(records):
    changes = [r["change"] for r in records if r["change"] >= 0]
    changes_percent = [r["change_percent"] for r in records if r["change_percent"] >= 0]
    var_change = statistics.variance(changes) if len(changes) > 1 else 0
    var_change_percent = statistics.variance(changes_percent) if len(changes_percent) > 1 else 0
    return var_change, var_change_percent

print(xml_to_json("data.xml"))

def main():
    records = xml_to_json("data.xml")

    avg_change_percent, avg_high, avg_low = compute_xml_averages(records)
    print("Średnia zmiana procentowa (z XML):", round(avg_change_percent, 3))
    print("Średnia cena HIGH (z XML):", round(avg_high, 3))
    print("Średnia cena LOW (z XML):", round(avg_low, 3))

    json_data = json.dumps(records, indent=2)

    parsed_json = json.loads(json_data)
    var_change, var_change_percent = compute_json_variances(parsed_json)

    print("\n[JSON] Wariancja zmian (change):", round(var_change, 3))
    print("[JSON] Wariancja zmian procentowych (change%):", round(var_change_percent, 3))

if __name__ == "__main__":
    main()