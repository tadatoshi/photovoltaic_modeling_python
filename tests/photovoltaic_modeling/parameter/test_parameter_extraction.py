import unittest
from photovoltaic_modeling.parameter.parameter_extraction import ParameterExtraction

class TestParameterExtraction(unittest.TestCase):

    def test_extract_series_resistance_parallel_resistance_and_diode_quality_factor(self):

        short_circuit_current = 3.87 # [A]
        open_circuit_voltage = 42.1 # [V]
        maximum_power_point_current = 3.56 # [A]
        maximum_power_point_voltage = 33.7 # [V]
        number_of_cells_in_series = 72

        parameter_extraction = ParameterExtraction(short_circuit_current, open_circuit_voltage, 
                                                   maximum_power_point_current, maximum_power_point_voltage, 
                                                   number_of_cells_in_series = number_of_cells_in_series)

        # series_resistance_estimate = 0.5
        # shunt_resistance_estimate = 1500
        # diode_quality_factor_estimate = 1.5
        series_resistance_estimate = 1
        shunt_resistance_estimate = 1
        diode_quality_factor_estimate = 1       
        parameter_estimates = [series_resistance_estimate, shunt_resistance_estimate, diode_quality_factor_estimate]

        parameter_extraction.calculate(parameter_estimates)

        # Note: Results:
        #   With series_resistance_estimate = 0.5, shunt_resistance_estimate = 1500, diode_quality_factor_estimate = 1.5:
        #        series_resistance = 0.56, shunt_resistance = 1862, diode_quality_factor = 1.343
        #   With series_resistance_estimate = 1, shunt_resistance_estimate = 1, diode_quality_factor_estimate = 1:
        #        (1 is chosen because the two latter parameters are used in the denominator of divisions and 0 cannot be used.)
        #        series_resistance = 0.58, shunt_resistance = 1398, diode_quality_factor = 1.318
        self.assertAlmostEqual(parameter_extraction.series_resistance, 0.47, delta = 0.2) # [Ohm]
        self.assertAlmostEqual(parameter_extraction.shunt_resistance, 1365, delta = 50) # [Ohm]
        self.assertAlmostEqual(parameter_extraction.diode_quality_factor, 1.397, delta = 0.08)

    def test_extract_series_resistance_parallel_resistance_and_diode_quality_factor_with_specified_number_of_iterations(self):

        short_circuit_current = 3.87 # [A]
        open_circuit_voltage = 42.1 # [V]
        maximum_power_point_current = 3.56 # [A]
        maximum_power_point_voltage = 33.7 # [V]
        number_of_cells_in_series = 72

        number_of_iterations = 1000

        parameter_extraction = ParameterExtraction(short_circuit_current, open_circuit_voltage, 
                                                   maximum_power_point_current, maximum_power_point_voltage, 
                                                   number_of_cells_in_series = number_of_cells_in_series, 
                                                   number_of_iterations = number_of_iterations)

        # series_resistance_estimate = 0.5
        # shunt_resistance_estimate = 1500
        # diode_quality_factor_estimate = 1.5
        series_resistance_estimate = 1
        shunt_resistance_estimate = 1
        diode_quality_factor_estimate = 1    
        # series_resistance_estimate = 1
        # shunt_resistance_estimate = 1000
        # diode_quality_factor_estimate = 1               
        parameter_estimates = [series_resistance_estimate, shunt_resistance_estimate, diode_quality_factor_estimate]

        parameter_extraction.calculate(parameter_estimates)

        # Note: Results:
        #   With series_resistance_estimate = 0.5, shunt_resistance_estimate = 1500, diode_quality_factor_estimate = 1.5:
        #        series_resistance = 0.56, shunt_resistance = 1862, diode_quality_factor = 1.343
        #   With series_resistance_estimate = 1, shunt_resistance_estimate = 1, diode_quality_factor_estimate = 1:
        #        (1 is chosen because the two latter parameters are used in the denominator of divisions and 0 cannot be used.)
        #        series_resistance = 0.577100619127, shunt_resistance = 1471.6762257, diode_quality_factor = 1.32304017483
        #   With series_resistance_estimate = 1, shunt_resistance_estimate = 1000, diode_quality_factor_estimate = 1:
        #        series_resistance = 0.56, shunt_resistance = 1862, diode_quality_factor = 1.343 
        self.assertAlmostEqual(parameter_extraction.series_resistance, 0.47, delta = 0.2) # [Ohm]
        self.assertAlmostEqual(parameter_extraction.shunt_resistance, 1365, delta = 110) # [Ohm]
        self.assertAlmostEqual(parameter_extraction.diode_quality_factor, 1.397, delta = 0.08)  
        # print("series_resistance=", parameter_extraction.series_resistance)
        # print("shunt_resistance=", parameter_extraction.shunt_resistance)
        # print("diode_quality_factor=", parameter_extraction.diode_quality_factor)   

    @unittest.skip("Investigate to get more proper values")
    def test_extract_series_resistance_parallel_resistance_and_diode_quality_factor_with_less_number_of_cells(self):

        short_circuit_current = 5.75 # [A]
        open_circuit_voltage = 22.5 # [V]
        maximum_power_point_current = 5.29 # [A]
        maximum_power_point_voltage = 18.9 # [V]
        # maximum_power_point_power = 100 # [W] Not used for the calculation. TODO: Remove this parameter. 
        # short_circuit_current_temperature_coefficient = None # Not used for the calculation. TODO: Remove this parameter.
        # power_temperature_coefficient = None # Not used for the calculation. TODO: Remove this parameter. 
        number_of_cells_in_series = 36

        # number_of_iterations = 1000

        # parameter_extraction = ParameterExtraction(short_circuit_current, open_circuit_voltage, 
        #                                            maximum_power_point_current, maximum_power_point_voltage, 
        #                                            number_of_cells_in_series = number_of_cells_in_series, 
        #                                            number_of_iterations = number_of_iterations)

        parameter_extraction = ParameterExtraction(short_circuit_current, open_circuit_voltage, 
                                                   maximum_power_point_current, maximum_power_point_voltage, 
                                                   number_of_cells_in_series = number_of_cells_in_series)        

        # series_resistance_estimate = 1.0
        # shunt_resistance_estimate = 900
        # diode_quality_factor_estimate = 1.5
        # series_resistance_estimate = 0.5
        # shunt_resistance_estimate = 1500
        # diode_quality_factor_estimate = 1.5
        series_resistance_estimate = 1
        shunt_resistance_estimate = 1
        diode_quality_factor_estimate = 1   
        # series_resistance_estimate = 1
        # shunt_resistance_estimate = 1000
        # diode_quality_factor_estimate = 1               
        parameter_estimates = [series_resistance_estimate, shunt_resistance_estimate, diode_quality_factor_estimate]

        parameter_extraction.calculate(parameter_estimates)

        # Note: Results:
        #   With number_of_iterations = 1000, series_resistance_estimate = 1.0, shunt_resistance_estimate = 900, diode_quality_factor_estimate = 1.5:
        #        series_resistance = 0.115493194076, shunt_resistance = 655596.982698, diode_quality_factor = 1.27995759761        
        #   With number_of_iterations = 1000, series_resistance_estimate = 0.5, shunt_resistance_estimate = 1500, diode_quality_factor_estimate = 1.5:
        #        series_resistance = 0.115493194076, shunt_resistance = 655596.982698, diode_quality_factor = 1.27995759761
        #   With number_of_iterations = 1000, series_resistance_estimate = 1, shunt_resistance_estimate = 1, diode_quality_factor_estimate = 1:
        #        (1 is chosen because the two latter parameters are used in the denominator of divisions and 0 cannot be used.)
        #        RuntimeWarning: The iteration is not making good progress, as measured by the improvement from the last ten iterations.
        #        series_resistance = -32.8604015489, shunt_resistance = 36.4430900554, diode_quality_factor = -177.346609341
        # self.assertAlmostEqual(parameter_extraction.series_resistance, 0.47, delta = 0.2) # [Ohm]
        # self.assertAlmostEqual(parameter_extraction.shunt_resistance, 1365, delta = 50) # [Ohm]
        # self.assertAlmostEqual(parameter_extraction.diode_quality_factor, 1.397, delta = 0.1)  
        print("series_resistance=", parameter_extraction.series_resistance)
        print("shunt_resistance=", parameter_extraction.shunt_resistance)
        print("diode_quality_factor=", parameter_extraction.diode_quality_factor)      


