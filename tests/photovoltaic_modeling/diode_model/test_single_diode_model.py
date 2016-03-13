import unittest
from photovoltaic_modeling.diode_model.single_diode_model import SingleDiodeModel
import matplotlib.pyplot as pyplot
import operator

class TestSingleDiodeModel(unittest.TestCase):

    def setUp(self):
        self.short_circuit_current = 3.87 # [A]
        self.open_circuit_voltage = 42.1 # [V]
        self.temperature_voltage_coefficient = -0.080 # [V/ºC]
        self.temperature_current_coefficient = (0.065 / 100) * self.short_circuit_current # ([%/ºC] / [100%]) * [A] = [A/ºC]
        series_resistance = 0.56
        shunt_resistance = 1862 
        diode_quality_factor = 1.343

        number_of_cells_in_series = 72

        number_of_voltage_decimal_digits = 1

        self.single_diode_model = SingleDiodeModel(self.short_circuit_current, 
                                                   self.open_circuit_voltage, 
                                                   number_of_cells_in_series, 
                                                   number_of_voltage_decimal_digits = number_of_voltage_decimal_digits, 
                                                   temperature_voltage_coefficient = self.temperature_voltage_coefficient, 
                                                   temperature_current_coefficient = self.temperature_current_coefficient, 
                                                   series_resistance = series_resistance, 
                                                   shunt_resistance = shunt_resistance, 
                                                   diode_quality_factor = diode_quality_factor)

    def test_calculate_i_v_values(self):

        # maximum_power_point_current = 3.56 # [A]
        # maximum_power_point_voltage = 33.7 # [V]

        operating_temperature = 35 + 273
        actual_irradiance = 900

        self.single_diode_model.calculate(operating_temperature, actual_irradiance)
        # self.single_diode_model.calculate(operating_temperature, actual_irradiance, maximum_power_point_current, maximum_power_point_voltage)

        voltages = self.single_diode_model.voltages
        currents = self.single_diode_model.currents
        powers = self.single_diode_model.powers

        self.assertEqual(len(voltages), 411)
        self.assertEqual(voltages[0], 0)
        self.assertEqual(voltages[410], 41.0)
        self.assertAlmostEqual(currents[0], 3.506, delta = 0.001)
        self.assertEqual(currents[410], 0)
        self.assertEqual(powers[0], 0)
        self.assertEqual(powers[410], 0)

        # pyplot.plot(voltages, currents)
        # pyplot.xlabel('Voltage [V]')
        # pyplot.ylabel('Current [A]')
        # pyplot.title('I-V curve')
        # pyplot.show(block=False)

        # pyplot.figure()
        # pyplot.plot(voltages, powers)
        # pyplot.xlabel('Voltage [V]')
        # pyplot.ylabel('Power [W]')
        # pyplot.title('P-V curve')
        # pyplot.show()       

if __name__ == '__main__':
    unittest.main() 