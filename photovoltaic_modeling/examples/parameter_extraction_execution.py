from photovoltaic_modeling.parameter.parameter_extraction import ParameterExtraction

short_circuit_current = 3.87 
open_circuit_voltage = 42.1 
maximum_power_point_current = 3.56 
maximum_power_point_voltage = 33.7 
number_of_cells_in_series = 72

parameter_extraction = ParameterExtraction(short_circuit_current, open_circuit_voltage, 
                                           maximum_power_point_current, maximum_power_point_voltage, 
                                           number_of_cells_in_series = number_of_cells_in_series)

series_resistance_estimate = 1
shunt_resistance_estimate = 1000
diode_quality_factor_estimate = 1

parameter_estimates = [series_resistance_estimate, shunt_resistance_estimate, diode_quality_factor_estimate]
parameter_extraction.calculate(parameter_estimates)

print('series_resistance=', parameter_extraction.series_resistance)
print('shunt_resistance=', parameter_extraction.shunt_resistance)
print('diode_quality_factor=', parameter_extraction.diode_quality_factor)