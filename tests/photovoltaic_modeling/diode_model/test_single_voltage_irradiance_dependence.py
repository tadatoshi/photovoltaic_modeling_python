import unittest
from photovoltaic_modeling.diode_model.single_voltage_irradiance_dependence import SingleVoltageIrradianceDependence

class TestSingleVoltageIrradianceDependence(unittest.TestCase):

    def setUp(self):
        self.open_circuit_voltage = 42.1 # [V]
        self.photo_current = 3.506 # [A] Value for operating_temperature = 35 + 273 [K] and actual_irradiance = 900[W/m^2]
        self.nominal_saturation_current = 1.680e-07 # [A]
        # self.saturation_current = 4.00e-07 # [A]
        self.shunt_resistance = 1862 # [Ω]
        self.number_of_cells_in_series = 72
        self.nominal_thermal_voltage = 0.0345
        # self.operating_thermal_voltage = 0.0356

        self.single_voltage_irradiance_dependence = SingleVoltageIrradianceDependence(self.photo_current, 
                                                                                      self.nominal_saturation_current, 
                                                                                      self.shunt_resistance, 
                                                                                      self.number_of_cells_in_series, 
                                                                                      self.nominal_thermal_voltage)

    def test_calculate_irradiance_dependent_voltage(self):

        voltage_estimation = self.open_circuit_voltage

        irradiance_dependent_voltage = self.single_voltage_irradiance_dependence.calculate(voltage_estimation)

        # Since the given parameters are for the actual irradiance (900[W/m^2]) lower than the irradiance in Standard Test Condition (1000[W/m^2]), voltage should be less:
        self.assertLessEqual(irradiance_dependent_voltage, self.open_circuit_voltage)

        # Since the result consistently gives 41.848808741740136 [V], use it as a assertion if the code is broken in the future modification:
        self.assertAlmostEqual(irradiance_dependent_voltage, 41.849, delta = 0.001)        
