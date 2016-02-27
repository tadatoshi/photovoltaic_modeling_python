from math import exp
import numpy

class SingleDiodeModel(object):

    boltzmann_constant = 1.38065e-23
    charge_of_electron = 1.602e-19
    nominal_temperature = 25 + 273
    nominal_irradiance = 1000
    band_gap = 1.12 # Silicon at 25 degrees celcius

    def __init__(self, 
                 short_circuit_current, 
                 open_circuit_voltage, 
                 number_of_cells_in_series, 
                 number_of_voltage_decimal_digits = 1,
                 temperature_current_coefficient = 0.0032, 
                 series_resistance = 0.221, 
                 shunt_resistance = 415.405, 
                 diode_quality_factor = 1.3):
        self.number_of_voltage_decimal_digits = number_of_voltage_decimal_digits

        self.short_circuit_current = short_circuit_current
        # Make sure that the voltage has the specified number of decimal digits:
        self.open_circuit_voltage = round(open_circuit_voltage, number_of_voltage_decimal_digits)
        self.number_of_cells_in_series = number_of_cells_in_series
        self.temperature_current_coefficient = temperature_current_coefficient
        self.series_resistance = series_resistance
        self.shunt_resistance = shunt_resistance
        self.diode_quality_factor = diode_quality_factor

    def calculate(self, operating_temperature, actual_irradiance):
        nominal_thermal_voltage = self.__thermal_voltage(self.nominal_temperature)
        nominal_saturation_current = self.__nominal_saturation_current(nominal_thermal_voltage)
        saturation_current = self.__saturation_current(nominal_saturation_current, operating_temperature)

        nominal_photo_current = self.short_circuit_current
        
        photo_current = self.__photo_current(actual_irradiance, nominal_photo_current, operating_temperature)

        operating_thermal_voltage = self.__thermal_voltage(operating_temperature)

        # Make sure to take number of decimal digits into account:
        number_of_elements = int(self.open_circuit_voltage * 10**self.number_of_voltage_decimal_digits) + 1

        self.voltages = numpy.linspace(0., float(self.open_circuit_voltage), number_of_elements)
        self.currents = numpy.zeros((1, number_of_elements)).flatten()
        self.powers = numpy.zeros((1, number_of_elements)).flatten()

        # Assumes that short circuit current changes proportionally with actual irradiance (i.e. not taking into account the temperature for now)
        self.currents[0] = self.short_circuit_current * (actual_irradiance / self.nominal_irradiance)
        
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

    def __thermal_voltage(self, temperature):
        return (self.number_of_cells_in_series * self.boltzmann_constant * temperature) / self.charge_of_electron

    def __nominal_saturation_current(self, thermal_voltage):
        return self.short_circuit_current / (exp(self.open_circuit_voltage / (self.diode_quality_factor * thermal_voltage)) - 1)

    def __saturation_current(self, nominal_saturation_current, operating_temperature):
        return nominal_saturation_current * ((operating_temperature / self.nominal_temperature)**3) * exp(((self.charge_of_electron * self.band_gap) / (self.diode_quality_factor * self.boltzmann_constant)) * ((1/self.nominal_temperature) - (1/operating_temperature)))

    def __photo_current(self, actual_irradiance, nominal_photo_current, operating_temperature):
        return (actual_irradiance / self.nominal_irradiance) * (nominal_photo_current + self.temperature_current_coefficient * (operating_temperature - self.nominal_temperature))

    def __current(self, voltage, current, photo_current, saturation_current, operating_thermal_voltage):
        return photo_current - saturation_current * (exp((voltage + current * self.series_resistance) / (self.diode_quality_factor * operating_thermal_voltage)) - 1) - ((voltage + current * self.series_resistance) / self.shunt_resistance)

