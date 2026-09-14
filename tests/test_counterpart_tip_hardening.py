from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SURFACES = {
    "public",
    "customer",
    "admin",
    "internal",
    "packaging",
    "recovery",
}
REQUIRED_ASSERTIONS = {"declared-behavior", "dual-environment", "evidence-gate"}


class CounterpartTipUpgradeHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.suite = json.loads((ROOT / "suite.json").read_text())

    def test_upgrade_contract_remains_versioned_and_owned(self) -> None:
        self.assertEqual(self.suite["version"], 1)
        self.assertEqual(self.suite["suite"], "upgrade-compatibility-tests")
        self.assertEqual(self.suite["owners"], ["ores-chat"])

    def test_all_upgrade_surfaces_remain_declared(self) -> None:
        self.assertEqual(set(self.suite["surfaces"]), REQUIRED_SURFACES)

    def test_main_and_test_orgs_share_the_same_contract(self) -> None:
        self.assertEqual(self.suite["environments"], ["main-org", "test-org"])
        assertion_ids = {item["id"] for item in self.suite["assertions"]}
        self.assertEqual(assertion_ids, REQUIRED_ASSERTIONS)

    def test_live_status_stays_fail_closed_without_retained_evidence(self) -> None:
        self.assertEqual(self.suite["status"], "contract-only")
        gate = next(item for item in self.suite["assertions"] if item["id"] == "evidence-gate")
        self.assertIn("Live status is forbidden", gate["description"])
        self.assertEqual(gate["evidence"], "contract")


if __name__ == "__main__":
    unittest.main()
