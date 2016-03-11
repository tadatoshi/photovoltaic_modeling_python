import unittest
from photovoltaic_modeling.diode_model.single_voltage_irradiance_dependence import SingleVoltageIrradianceDependence

class TestSingleVoltageIrradianceDependence(unittest.TestCase):

    def setUp(self):
        self.open_circuit_voltage = 42.1 # [V]
        # self.photo_current = 3.87 # [A] Value for operating_temperature = 35 + 273
        self.photo_current = 3.895 # [A] Value for operating_temperature = 35 + 273
        self.saturation_current = 4.00e-07 # [A]
        self.shunt_resistance = 1862 # [Ω]
        self.number_of_cells_in_series = 72
        # self.operating_thermal_voltage = 1.911 # [V] Value for operating_temperature = 35 + 273
        # self.operating_thermal_voltage = 0.0356 # [V] Value for operating_temperature = 35 + 273
        self.nominal_thermal_voltage = 0.0345

        self.single_voltage_irradiance_dependence = SingleVoltageIrradianceDependence(self.photo_current, 
                                                                                      self.saturation_current, 
                                                                                      self.shunt_resistance, 
                                                                                      self.number_of_cells_in_series, 
                                                                                      self.nominal_thermal_voltage)

    def test_calculate_irradiance_dependent_voltage(self):

        voltage_estimation = self.open_circuit_voltage

        irradiance_dependent_voltage = self.single_voltage_irradiance_dependence.calculate(voltage_estimation)

        # Since the given parameters are for the operating temperature higher than the temperature in Standard Test Condition, voltage should be less:
        self.assertLessEqual(irradiance_dependent_voltage, self.open_circuit_voltage)

        # Since the result consistently gives 39.957550080953816 [V], use it as a assertion if the code is broken in the future modification:
        self.assertAlmostEqual(irradiance_dependent_voltage, 39.958, delta = 0.001)        
