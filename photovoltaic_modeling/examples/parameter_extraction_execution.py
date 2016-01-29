from root_finding.parameter_extraction import ParameterExtraction

parameter_extraction = ParameterExtraction(args.short_circuit_current, args.open_circuit_voltage, 
                                           args.maximum_power_point_current, args.maximum_power_point_voltage, None, 
                                           None, None, 
                                           number_of_cells_in_series = args.number_of_cells_in_series)

parameter_estimates = [args.series_resistance_estimate, args.shunt_resistance_estimate, args.diode_quality_factor_estimate]
parameter_extraction.calculate(parameter_estimates)

print('series_resistance=', parameter_extraction.series_resistance)
print('shunt_resistance=', parameter_extraction.shunt_resistance)
print('diode_quality_factor=', parameter_extraction.diode_quality_factor)