from photovoltaic_modeling.diode_model.single_diode_model import SingleDiodeModel
import matplotlib.pyplot as pyplot
import photovoltaic_modeling.diode_model.report_helper as report_helper

# Values for RNG-100D:
short_circuit_current = 5.75
open_circuit_voltage = 22.5
temperature_current_coefficient = 0.04
series_resistance = 0.115820201147
shunt_resistance = 37173.5612907
diode_quality_factor = 1.27873896365

number_of_series_connected_cells = 36

number_of_voltage_decimal_digits = 1

single_diode_model = SingleDiodeModel(short_circuit_current, 
                                      open_circuit_voltage, 
                                      number_of_series_connected_cells, 
                                      number_of_voltage_decimal_digits = number_of_voltage_decimal_digits,
                                      temperature_current_coefficient = temperature_current_coefficient, 
                                      series_resistance = series_resistance, 
                                      shunt_resistance = shunt_resistance, 
                                      diode_quality_factor = diode_quality_factor)

# operating_temperature = 25 + 273
operating_temperature = 35 + 273
actual_irradiance = 1000

single_diode_model.calculate(operating_temperature, 
                             actual_irradiance)

# voltages = single_diode_model.voltages
# currents = single_diode_model.currents
# powers = single_diode_model.powers

report_helper.write_result_to_csv_file(single_diode_model, 'single_diode_model_rng-100d_one_module_no_shading')
report_helper.plot_result(single_diode_model)



