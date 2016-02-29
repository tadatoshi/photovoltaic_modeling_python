import unittest
from photovoltaic_modeling.diode_model.single_diode_model import SingleDiodeModel
import matplotlib.pyplot as pyplot
import operator

class TestSingleDiodeModel(unittest.TestCase):

    def setUp(self):
        self.short_circuit_current = 8.21
        self.open_circuit_voltage = 32.9
        self.temperature_voltage_coefficient = -0.123
        self.temperature_current_coefficient = 0.0032
        series_resistance = 0.221
        shunt_resistance = 415.405
        diode_quality_factor = 1.3

        number_of_cells_in_series = 10

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

        operating_temperature = 35 + 273
        actual_irradiance = 1000

        self.single_diode_model.calculate(operating_temperature, actual_irradiance)

        voltages = self.single_diode_model.voltages
        currents = self.single_diode_model.currents
        powers = self.single_diode_model.powers

        self.assertEqual(len(voltages), 318)
        self.assertEqual(voltages[0], 0)
        self.assertEqual(voltages[317], 31.7)
        # self.assertAlmostEqual(voltages[317], 31.7, delta = 0.1)
        self.assertEqual(currents[0], 8.242)
        self.assertEqual(currents[317], 0)
        self.assertEqual(powers[0], 0)
        self.assertEqual(powers[317], 0)

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