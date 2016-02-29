from math import exp
from scipy import optimize

'''
References
-----------

[1] D. Sera, R. Teodorescu, and P. Rodriguez, "PV panel model based on datasheet values," in Industrial Electronics, 2007. ISIE 2007. IEEE International Symposium on, 2007, pp. 2392-2396.
'''
class ParameterExtraction(object):

    boltzmann_constant = 1.38065e-23
    charge_of_electron = 1.602e-19
    nominal_temperature = 25 + 273    

    def __init__(self, short_circuit_current, open_circuit_voltage, 
                 maximum_power_point_current, maximum_power_point_voltage, 
                 number_of_cells_in_series = 1, 
                 **optional_keyword_arguments):
        self.__short_circuit_current = short_circuit_current
        self.__open_circuit_voltage = open_circuit_voltage
        self.__maximum_power_point_current = maximum_power_point_current
        self.__maximum_power_point_voltage = maximum_power_point_voltage
        self.__number_of_cells_in_series = number_of_cells_in_series

        self.number_of_iterations = optional_keyword_arguments.get('number_of_iterations', None)

    #
    # Alias methods in order to make long equations readable:
    #
    def isc(self):
        return self.__short_circuit_current

    def voc(self):
        return self.__open_circuit_voltage

    def impp(self):
        return self.__maximum_power_point_current

    def vmpp(self):
        return self.__maximum_power_point_voltage

    def ns(self):
        return self.__number_of_cells_in_series
    #
    # End of alias methods definition
    #

    # parameter_estimates: [series_resistance, shunt_resistance, diode_quality_factor]
    # Note: The third element of parameter_estimates is not thermal_voltage but thermal_voltage is used as the third unknown parameter for the calculation. 
    def calculate(self, parameter_estimates = [1, 1, 1]):

        thermal_voltage_estimate = self.__thermal_voltage_estimate(parameter_estimates[2])

        if self.number_of_iterations == None:
          solution = optimize.root(self.__function_of_three_equations, [parameter_estimates[0], parameter_estimates[1], thermal_voltage_estimate])
        else:
          solution = optimize.root(self.__function_of_three_equations, [parameter_estimates[0], parameter_estimates[1], thermal_voltage_estimate], options={'maxfev': self.number_of_iterations})

        self.series_resistance = solution.x[0]
        self.shunt_resistance = solution.x[1]
        self.thermal_voltage = solution.x[2]

        self.diode_quality_factor = self.__diode_quality_factor()

    def __diode_quality_factor(self):
        return (self.thermal_voltage * self.charge_of_electron) / (self.boltzmann_constant * self.nominal_temperature)

    def __thermal_voltage_estimate(self, diode_quality_factor_estimate):
        return (diode_quality_factor_estimate * self.boltzmann_constant * self.nominal_temperature) / self.charge_of_electron  

    # unknown_parameters_vector = [series_resistance, shunt_resistance, thermal_voltage]
    def __function_of_three_equations(self, unknown_parameters_vector):

        # return [equation_1, equation_2, equation_3]
        # First element: Equation (12) of [1] with Impp moved to the right hand side to make the equation with the form "0 = ....".
        # Second element: Equation (18) of [1] with dP/dV (at I = Impp) = 0 since at Maximum Power Point, dP/dV = 0.
        # Third element: Equation (19) of [1] with -1/Rsh moved to the right hand side to make the equation with the form "0 = ....". 
        # return [self.__short_circuit_current - ((self.__maximum_power_point_voltage + self.__maximum_power_point_current * unknown_parameters_vector[0] - self.__short_circuit_current * unknown_parameters_vector[0]) / unknown_parameters_vector[1]) \
        #         -(self.__short_circuit_current - ((self.__open_circuit_voltage - self.__short_circuit_current * unknown_parameters_vector[0]) / unknown_parameters_vector[1])) \
        #         * exp((self.__maximum_power_point_voltage + self.__maximum_power_point_current * unknown_parameters_vector[0] - self.__open_circuit_voltage) / (self.__number_of_cells_in_series * unknown_parameters_vector[2])) \
        #         - self.__maximum_power_point_current, 
        #         self.__maximum_power_point_current + self.__maximum_power_point_voltage * \
        #         ((-(((self.__short_circuit_current * unknown_parameters_vector[1] - self.__open_circuit_voltage + self.__short_circuit_current * unknown_parameters_vector[0]) * exp((self.__maximum_power_point_voltage + self.__maximum_power_point_current * unknown_parameters_vector[0] - self.__open_circuit_voltage) / (self.__number_of_cells_in_series * unknown_parameters_vector[2]))) / (self.__number_of_cells_in_series * unknown_parameters_vector[2] * unknown_parameters_vector[1])) - (1 / unknown_parameters_vector[1])) \
        #         / (1 + (((self.__short_circuit_current * unknown_parameters_vector[1] - self.__open_circuit_voltage + self.__short_circuit_current * unknown_parameters_vector[0]) * exp((self.__maximum_power_point_voltage + self.__maximum_power_point_current * unknown_parameters_vector[0] - self.__open_circuit_voltage) / (self.__number_of_cells_in_series * unknown_parameters_vector[2]))) / (self.__number_of_cells_in_series * unknown_parameters_vector[2] * unknown_parameters_vector[1])) + (unknown_parameters_vector[0] / unknown_parameters_vector[1]))), 
        #         ((-(((self.__short_circuit_current * unknown_parameters_vector[1] - self.__open_circuit_voltage + self.__short_circuit_current * unknown_parameters_vector[0]) * exp((self.__short_circuit_current * unknown_parameters_vector[0] - self.__open_circuit_voltage) / (self.__number_of_cells_in_series * unknown_parameters_vector[2]))) / (self.__number_of_cells_in_series * unknown_parameters_vector[2] * unknown_parameters_vector[1])) - (1 / unknown_parameters_vector[1])) \
        #         / (1 + (((self.__short_circuit_current * unknown_parameters_vector[1] - self.__open_circuit_voltage + self.__short_circuit_current * unknown_parameters_vector[0]) * exp((self.__short_circuit_current * unknown_parameters_vector[0] - self.__open_circuit_voltage) / (self.__number_of_cells_in_series * unknown_parameters_vector[2]))) / (self.__number_of_cells_in_series * unknown_parameters_vector[2] * unknown_parameters_vector[1])) + (unknown_parameters_vector[0] / unknown_parameters_vector[1]))) \
        #         + (1 / unknown_parameters_vector[1])]
        return [self.isc() \
                - ((self.vmpp() + self.impp() * unknown_parameters_vector[0] - self.isc() * unknown_parameters_vector[0]) / unknown_parameters_vector[1]) \
                -(self.isc() - ((self.voc() - self.isc() * unknown_parameters_vector[0]) / unknown_parameters_vector[1])) \
                * exp((self.vmpp() + self.impp() * unknown_parameters_vector[0] - self.voc()) / (self.ns() * unknown_parameters_vector[2])) \
                - self.impp(), 
                self.impp() \
                + self.vmpp() * \
                    ( \
                        ( \
                            -( \
                                ( (self.isc() * unknown_parameters_vector[1] - self.voc() + self.isc() * unknown_parameters_vector[0]) \
                                    * exp((self.vmpp() + self.impp() * unknown_parameters_vector[0] - self.voc()) / (self.ns() * unknown_parameters_vector[2])) \
                                ) \
                                / (self.ns() * unknown_parameters_vector[2] * unknown_parameters_vector[1]) \
                            ) \
                            - (1 / unknown_parameters_vector[1]) \
                        ) / \
                        ( \
                            1 + \
                            ( \
                                ( (self.isc() * unknown_parameters_vector[1] - self.voc() + self.isc() * unknown_parameters_vector[0]) \
                                    * exp((self.vmpp() + self.impp() * unknown_parameters_vector[0] - self.voc()) / (self.ns() * unknown_parameters_vector[2]))) \
                                / (self.ns() * unknown_parameters_vector[2] * unknown_parameters_vector[1]) \
                            ) \
                            + (unknown_parameters_vector[0] / unknown_parameters_vector[1]) \
                        ) \
                    ), 
                ( \
                    ( \
                        -( \
                            ( (self.isc() * unknown_parameters_vector[1] - self.voc() + self.isc() * unknown_parameters_vector[0]) \
                                * exp((self.isc() * unknown_parameters_vector[0] - self.voc()) / (self.ns() * unknown_parameters_vector[2])) \
                            ) \
                            / (self.ns() * unknown_parameters_vector[2] * unknown_parameters_vector[1])) \
                        - (1 / unknown_parameters_vector[1]) \
                    ) / \
                    ( \
                        1 + \
                        ( \
                            ( (self.isc() * unknown_parameters_vector[1] - self.voc() + self.isc() * unknown_parameters_vector[0]) \
                                * exp((self.isc() * unknown_parameters_vector[0] - self.voc()) / (self.ns() * unknown_parameters_vector[2])) \
                            ) / (self.ns() * unknown_parameters_vector[2] * unknown_parameters_vector[1]) 
                        ) \
                        + (unknown_parameters_vector[0] / unknown_parameters_vector[1]) \
                    ) \
                ) \
                + (1 / unknown_parameters_vector[1])]                

    # Note: Decided to rely on the numerical estimate of root function instead of calculating it. 
    #       But partically-done calculation is left here for the future reference just in case:
    # unknown_parameters_vector = [series_resistance, shunt_resistance, thermal_voltage]
    # def __jacobian_of_function_of_three_equations(self, unknown_parameters_vector):
    #     series_resistance = unknown_parameters_vector[0]
    #     shunt_resistance = unknown_parameters_vector[1]
    #     thermal_voltage = unknown_parameters_vector[1]

    #     exponential_factor_1 = self.__exponential_factor_1(series_resistance, thermal_voltage)

    #     element_1_1 = -((self.__maximum_power_point_current - self.__short_circuit_current) / shunt_resistance) \
    #                   - (self.__short_circuit_current / shunt_resistance) * exp(exponential_factor_1) \
    #                   - (self.__short_circuit_current - ((self.__open_circuit_voltage - self.__short_circuit_current * series_resistance) / shunt_resistance)) * exponential_factor_1 * exp(self.__maximum_power_point_current / (self.__number_of_cells_in_series * thermal_voltage))
    #     element_1_2 = (self.__maximum_power_point_voltage + self.__maximum_power_point_current * series_resistance - self.__short_circuit_current * series_resistance) / (shunt_resistance**2) \
    #                   - (self.__open_circuit_voltage - self.__short_circuit_current * series_resistance) * exp(exponential_factor_1) / (shunt_resistance**2)
    #     element_1_3 = (self.__short_circuit_current - ((self.__open_circuit_voltage - self.__short_circuit_current * series_resistance) / shunt_resistance)) * exponential_factor_1 * exp(exponential_factor_1) * ((self.__maximum_power_point_voltage + self.__maximum_power_point_current * series_resistance - self.__open_circuit_voltage) / (thermal_voltage**2))

    #     # element_2_1 = 

        

        





