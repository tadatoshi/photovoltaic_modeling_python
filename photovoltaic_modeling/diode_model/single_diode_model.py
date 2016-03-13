from math import exp
import numpy
from photovoltaic_modeling.parameter.parameter_extraction import ParameterExtraction
from photovoltaic_modeling.diode_model.single_voltage_irradiance_dependence import SingleVoltageIrradianceDependence

'''
References
-----------

[1] D. Sera, R. Teodorescu, and P. Rodriguez, "PV panel model based on datasheet values," in Industrial Electronics, 2007. ISIE 2007. IEEE International Symposium on, 2007, pp. 2392-2396.
[2] M. G. Villalva and J. R. Gazoli, ”Comprehensive approach to modeling and simulation of photovoltaic arrays,” Power Electronics, IEEE Trans- actions on, vol. 24, pp. 1198-1208, 2009.
[3] A. Bellini, S. Bifaretti, V. Iacovone, and C. Cornaro, ”Simplified model of a photovoltaic module,” in Applied Electronics, 2009. AE 2009, 2009, pp. 47-51.
'''
class SingleDiodeModel(object):

    boltzmann_constant = 1.38065e-23
    charge_of_electron = 1.602e-19
    nominal_temperature = 25 + 273
    nominal_irradiance = 1000
    band_gap = 1.12 # Silicon at 25 degrees celcius

    '''
    temperature_voltage_coefficient [V/ºC] not [%/ºC]
    temperature_current_coefficient [A/ºC] not [%/ºC]
    '''
    def __init__(self, 
                 short_circuit_current, 
                 open_circuit_voltage, 
                 number_of_cells_in_series, 
                 number_of_voltage_decimal_digits = 1,
                 temperature_voltage_coefficient = -0.123,
                 temperature_current_coefficient = 0.0032, 
                 series_resistance = 0.221, 
                 shunt_resistance = 415.405, 
                 diode_quality_factor = 1.3):

        self.number_of_voltage_decimal_digits = number_of_voltage_decimal_digits

        self.short_circuit_current = self.__convert_to_float(short_circuit_current)
        # Make sure that the voltage has the specified number of decimal digits:
        self.open_circuit_voltage = round(self.__convert_to_float(open_circuit_voltage), self.number_of_voltage_decimal_digits)
        self.number_of_cells_in_series = number_of_cells_in_series
        self.temperature_voltage_coefficient = temperature_voltage_coefficient
        self.temperature_current_coefficient = temperature_current_coefficient
        self.series_resistance = series_resistance
        self.shunt_resistance = shunt_resistance
        self.diode_quality_factor = diode_quality_factor

    def calculate(self, operating_temperature, actual_irradiance):

        nominal_thermal_voltage = self.__thermal_voltage(self.nominal_temperature)
        operating_thermal_voltage = self.__thermal_voltage(operating_temperature)

        nominal_saturation_current = self.__saturation_current(self.nominal_temperature, nominal_thermal_voltage)
        saturation_current = self.__saturation_current(operating_temperature, operating_thermal_voltage)

        actual_short_circuit_current = self.__actual_current(self.short_circuit_current, operating_temperature, actual_irradiance)      

        photo_current = actual_short_circuit_current

        actual_open_circuit_voltage = round(self.__actual_voltage(photo_current, nominal_saturation_current, nominal_thermal_voltage, self.open_circuit_voltage, operating_temperature), self.number_of_voltage_decimal_digits)

        # Make sure to take number of decimal digits into account:
        number_of_elements = int(actual_open_circuit_voltage * 10**self.number_of_voltage_decimal_digits) + 1

        self.voltages = numpy.linspace(0., actual_open_circuit_voltage, number_of_elements)
        self.currents = numpy.zeros((1, number_of_elements)).flatten()
        self.powers = numpy.zeros((1, number_of_elements)).flatten()

        self.currents[0] = actual_short_circuit_current
        
        # The last current element doesn't become 0 based on the iterative calculation below. 
        # Hence, the for loop below is stopped at the element before the last element. 
        # Then, the value of the last current element stays 0[A] and also the last power element stays 0[W] 
        for i in range(1, number_of_elements - 1):
            calculated_current = self.__current(self.voltages[i], self.currents[i-1], photo_current, saturation_current, operating_thermal_voltage)
            # Note: The following is a quick fix for getting negative current in MultipleModulesSingleDiodeModel 
            #       when using series_resistance, shunt_resistance, and diode_quality_factor for nominal_irradiance in the case of partial shading. 
            # TODO: Modify to calculate those values based on irradiance under partial shading using root_finding. 
            if calculated_current < 0.0:
                calculated_current = 0.0
            self.currents[i] = calculated_current

            self.powers[i] = self.voltages[i] * self.currents[i]

    def __convert_to_float(self, value):
        if isinstance(value, float):
            return value
        else:
            return float(value)    

    def __thermal_voltage(self, temperature):
        # Based on equation (2) of [1], which includes diode_quality_factor and doesn't include number_of_cells_in_series:
        return (self.diode_quality_factor * self.boltzmann_constant * temperature) / self.charge_of_electron

    def __nominal_saturation_current(self, thermal_voltage):
        # The following is based on equation (6) of [2] but thermal_voltage is defined as equation (2) of [1], which includes diode_quality_factor and doesn't include number_of_cells_in_series, and thus the following equation is modified accordingly:
        return self.short_circuit_current / (exp(self.open_circuit_voltage / (self.number_of_cells_in_series * thermal_voltage)) - 1)

    def __saturation_current(self, operating_temperature, thermal_voltage):
        # The following is based on equation (7) of [2] but thermal_voltage is defined as equation (2) of [1], which includes diode_quality_factor and doesn't include number_of_cells_in_series, and thus the following equation is modified accordingly:
        return (self.short_circuit_current + self.temperature_current_coefficient * (operating_temperature - self.nominal_temperature)) / (exp((self.open_circuit_voltage + self.temperature_voltage_coefficient * (operating_temperature - self.nominal_temperature)) / (self.number_of_cells_in_series * thermal_voltage)) - 1)

    def __current(self, voltage, current, photo_current, saturation_current, operating_thermal_voltage):
        # Based on equation (1) of [1] (thermal_voltage is defined as equation (2) of [1], which includes diode_quality_factor and doesn't include number_of_cells_in_series):
        return photo_current - saturation_current * (exp((voltage + current * self.series_resistance) / (self.number_of_cells_in_series * operating_thermal_voltage)) - 1) - ((voltage + current * self.series_resistance) / self.shunt_resistance)

    def __actual_current(self, nominal_current, operating_temperature, actual_irradiance):
        # Based on equation (4) of [2], which uses [A/ºC] as the unit of temperature_current_coefficient (Note: Some datasheets use [%/ºC] as unit):
        return (actual_irradiance / self.nominal_irradiance) * (nominal_current + self.temperature_current_coefficient * (operating_temperature - self.nominal_temperature))

    def __actual_voltage(self, photo_current, saturation_current, nominal_thermal_voltage, nominal_voltage, operating_temperature):
        # TODO: I-V curve and P-V curve gets the sharp drop near open circuit voltage when irradiance dependence is taken into account 
        # Irradiance dependence:
        single_voltage_irradiance_dependence = SingleVoltageIrradianceDependence(photo_current, 
                                                                                 saturation_current, 
                                                                                 self.shunt_resistance, 
                                                                                 self.number_of_cells_in_series, 
                                                                                 nominal_thermal_voltage)
        irradiance_dependent_voltage = single_voltage_irradiance_dependence.calculate(nominal_voltage)

        # Temperature dependence:
        # Based on equation (24) of [1] but taking into account that the unit of temperature_voltage_coefficient is [V/ºC] instead of [%/ºC]. (Note: Different datasheets use either of these units):
        return irradiance_dependent_voltage + self.temperature_voltage_coefficient * (operating_temperature - self.nominal_temperature)
