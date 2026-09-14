import tomllib
import unittest
from pathlib import Path
from deep_tests.upgrade_model import IncompatibleChange, assert_non_destructive_required_change, negotiate, read_with_version
class CounterpartTipUpgradeHardeningTests(unittest.TestCase):
    def test_version_negotiation_is_order_independent(self):
        supported=([1,2,3],[3,2,1],[2,3,1])
        for left in supported:
            for right in supported: self.assertEqual(negotiate(left,right),3)
    def test_old_reader_projects_new_writer_without_future_field_leakage(self):
        record={"version":3,"id":"edge-1","display_name":"current","metadata":{"labels":["a"],"future_nested":{"ignored":True}},"status":"active","future_field":[1,2,3]}; self.assertEqual(read_with_version(record,1),{"id":"edge-1","name":"current"})
    def test_every_required_field_removal_fails_closed(self):
        required={"id","display_name","status"}
        for removed in required:
            with self.assertRaises(IncompatibleChange): assert_non_destructive_required_change(required,required-{removed})
        assert_non_destructive_required_change(required,required|{"metadata"})
    def test_zed_pkg_runner_keeps_suite_and_verifier_coupled(self):
        script=tomllib.loads(Path(".zpkg.toml").read_text())["scripts"]["test"]; self.assertIn("unittest discover",script); self.assertIn("scripts/verify_repository.py",script)
if __name__ == "__main__": unittest.main()
