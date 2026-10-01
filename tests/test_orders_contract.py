from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "orders.yaml"


class TestOrdersContract(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with CONTRACT_PATH.open("r", encoding="utf-8") as file:
            cls.contract = yaml.safe_load(file)

    def test_required_sections(self):
        required = ["contract", "schema", "quality", "operations"]

        for section in required:
            with self.subTest(section=section):
                self.assertIn(section, self.contract)

    def test_primary_key(self):
        schema = self.contract["schema"]
        primary_key = schema["primary_key"]

        self.assertIn(primary_key, schema["fields"])

        self.assertFalse(
            schema["fields"][primary_key]["nullable"]
        )

    def test_quality_fields_exist(self):
        fields = self.contract["schema"]["fields"]

        for rule in ["unique", "not_null"]:
            for field in self.contract["quality"][rule]:
                with self.subTest(rule=rule, field=field):
                    self.assertIn(field, fields)


if __name__ == "__main__":
    unittest.main()