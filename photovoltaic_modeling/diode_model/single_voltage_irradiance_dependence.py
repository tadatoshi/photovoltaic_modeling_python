from math import log
from scipy import optimize

'''
References
-----------

[1] D. Sera, R. Teodorescu, and P. Rodriguez, "PV panel model based on datasheet values," in Industrial Electronics, 2007. ISIE 2007. IEEE International Symposium on, 2007, pp. 2392-2396.
'''
class SingleVoltageIrradianceDependence(object):

    def __init__(self, 
                 photo_current, 
                 nominal_saturation_current, 
                 shunt_resistance, 
                 number_of_cells_in_series, 
                 nominal_thermal_voltage, 
                 **optional_keyword_arguments):

        self.__photo_current = photo_current
        self.__nominal_saturation_current = nominal_saturation_current
        self.__shunt_resistance = shunt_resistance
        self.__number_of_cells_in_series = number_of_cells_in_series
        self.__nominal_thermal_voltage = nominal_thermal_voltage

        self.__number_of_iterations = optional_keyword_arguments.get('number_of_iterations', None)

    #
    # Alias methods in order to make long equation readable:
    #
    def iph(self):
        return self.__photo_current

    def io(self):
        return self.__nominal_saturation_current

    def rsh(self):
        return self.__shunt_resistance

    def ns(self):
        return self.__number_of_cells_in_series   

    def vt(self):
        return self.__nominal_thermal_voltage             

    def calculate(self, voltage_estimation):

        if self.__number_of_iterations == None:
            solution = optimize.newton(self.__function, voltage_estimation)
          # solution = optimize.fsolve(self.__function, voltage_estimation)
        else:
            solution = optimize.newton(self.__function, voltage_estimation, maxiter = self.__number_of_iterations)
          # solution = optimize.fsolve(self.__function, voltage_estimation, maxfev = self.__number_of_iterations)

        return solution

    def __function(self, unknown_voltage):

        x = unknown_voltage

        # Based on equation (23) of [1]:
        # In the form "... = 0"
        # meth.log is natural logarithm:
        return log((self.iph() * self.rsh() - x) / (self.io() * self.rsh())) * self.ns() * self.vt() - x
