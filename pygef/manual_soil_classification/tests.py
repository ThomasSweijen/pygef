import unittest
import pygef.manual_soil_classification.list_default_soil_types as default
import pygef.manual_soil_classification.manual_soil_classification as soil


class ManualSoilClassificationTest(unittest.TestCase):
    def testDefiningClassification(self):
        A = soil.ManualSoilClassification()
        A.define_soil_classification(soil_types=default.default_soil_types)

    def test_check_status_classification(self):
        A = soil.ManualSoilClassification()
        A.define_soil_classification()
        self.assertEqual(A.check_status_classification(), True)

    def test_check_status_classification(self):
        A = soil.ManualSoilClassification()
        A.define_soil_classification()
        self.assertEqual(A.check_status_classification(), True)

    def test_check_status_classification(self):
        A = soil.ManualSoilClassification()
        A.define_soil_classification()
        self.assertEqual(A.overlay_other_lithology[4], True)

    def test_get_bounding_values_soil_classification(self):
        A = soil.ManualSoilClassification()
        A.define_soil_classification()
        self.assertAlmostEqual(A.global_qc_max, 100.0)
        self.assertAlmostEqual(A.global_qc_min, 0.0)
        self.assertAlmostEqual(A.global_fn_max, 12.0)
        self.assertAlmostEqual(A.global_fn_min, 0.0)
        self.assertEqual(A.global_level_max, None)
        self.assertEqual(A.global_level_min, None)

    def test_plot_soil_classification_diagram(self):
        A = soil.ManualSoilClassification()
        A.define_soil_classification()
        B = A.plot_soil_classification_diagram()
        self.assertIsNotNone(B)
