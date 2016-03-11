import unittest
from photovoltaic_modeling.diode_model.multiple_modules_single_diode_model import MultipleModulesSingleDiodeModel
import matplotlib.pyplot as pyplot

class TestMultipleModulesSingleDiodeModel(unittest.TestCase):

    def test_calculate_i_v_values_with_one_module_50_percent_shaded(self):

        # Values for BP MSX120:
        short_circuit_current = 3.87
        open_circuit_voltage = 42.1
        temperature_voltage_coefficient = -0.08
        temperature_current_coefficient = 0.065
        series_resistance = 0.581350667
        shunt_resistance = 1398.292572
        diode_quality_factor = 1.317954479

        number_of_cells_in_series = 72

        number_of_voltage_decimal_digits = 1

        number_of_modules_in_series = 2

        multiple_modules_single_diode_model = MultipleModulesSingleDiodeModel(short_circuit_current, 
                                                                              open_circuit_voltage, 
                                                                              number_of_cells_in_series, 
                                                                              number_of_voltage_decimal_digits = number_of_voltage_decimal_digits, 
                                                                              temperature_voltage_coefficient = temperature_voltage_coefficient, 
                                                                              temperature_current_coefficient = temperature_current_coefficient, 
                                                                              series_resistance = series_resistance, 
                                                                              shunt_resistance = shunt_resistance, 
                                                                              diode_quality_factor = diode_quality_factor, 
                                                                              number_of_modules_in_series = number_of_modules_in_series)

        operating_temperature = 25 + 273
        actual_irradiance = 1000

        shaded_module_index = 1
        partial_shading_ratio = 0.5

        multiple_modules_single_diode_model.calculate(operating_temperature, 
                                                      actual_irradiance, 
                                                      partial_shading_ratios = [{'pv_module_index': shaded_module_index, 'partial_shading_ratio': partial_shading_ratio}])

        voltages = multiple_modules_single_diode_model.voltages
        currents = multiple_modules_single_diode_model.currents
        powers = multiple_modules_single_diode_model.powers

        self.assertEqual(len(voltages), 797)
        self.assertEqual(len(currents), 797)
        self.assertEqual(len(powers), 797)
        self.assertEqual(voltages[0], 0)
        self.assertEqual(currents[0], short_circuit_current)
        self.assertEqual(currents[796], 0)
        self.assertEqual(powers[0], 0)
        self.assertEqual(powers[796], 0)

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