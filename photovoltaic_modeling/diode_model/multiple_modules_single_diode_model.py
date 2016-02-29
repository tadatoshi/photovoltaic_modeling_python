from photovoltaic_modeling.diode_model.single_diode_model import SingleDiodeModel

class MultipleModulesSingleDiodeModel(object):

    def __init__(self, 
                 short_circuit_current, 
                 open_circuit_voltage, 
                 number_of_cells_in_series, 
                 number_of_voltage_decimal_digits = 1, 
                 temperature_voltage_coefficient = -0.123, 
                 temperature_current_coefficient = 0.0032, 
                 series_resistance = 0.221, 
                 shunt_resistance = 415.405, 
                 diode_quality_factor = 1.3, 
                 number_of_modules_in_series = 1):

        self.short_circuit_current = short_circuit_current
        self.open_circuit_voltage = round(open_circuit_voltage, number_of_voltage_decimal_digits)
        self.number_of_cells_in_series = number_of_cells_in_series
        self.number_of_voltage_decimal_digits = number_of_voltage_decimal_digits
        self.temperature_voltage_coefficient = temperature_voltage_coefficient
        self.temperature_current_coefficient = temperature_current_coefficient

        self.series_resistance = series_resistance
        self.shunt_resistance = shunt_resistance
        self.diode_quality_factor = diode_quality_factor

        self.number_of_modules_in_series = number_of_modules_in_series

    # Format of partial_shading_ratios: [{'pv_module_index': shaded_module_index, 'partial_shading_ratio': partial_shading_ratio}]
    def calculate(self, operating_temperature, actual_irradiance, partial_shading_ratios = None):

        number_of_unshaded_modules = self.number_of_modules_in_series

        partial_shading_ratio_number_of_modules_dictionary = {}

        if partial_shading_ratios != None:

            number_of_unshaded_modules = self.number_of_modules_in_series - len(partial_shading_ratios)

            # Generating the partial_shading_ratio_number_of_modules_dictionary like e.g. { 0.1: [1,2], 0.5: [3, 5], 0.8: [4] }
            partial_shading_ratio_number_of_modules_dictionary = self.__get_partial_shading_ratio_number_of_modules_dictionary(partial_shading_ratios)

        partial_shading_ratio_single_diode_model_dictionary = self.__get_partial_shading_ratio_single_diode_model_dictionary(operating_temperature, actual_irradiance, number_of_unshaded_modules, partial_shading_ratio_number_of_modules_dictionary)

        self.__consolidate_calculated_values(partial_shading_ratio_single_diode_model_dictionary)

    # Generating the partial_shading_ratio_number_of_modules_dictionary like e.g. { 0.1: [1,2], 0.5: [3, 5], 0.8: [4] }
    def __get_partial_shading_ratio_number_of_modules_dictionary(self, partial_shading_ratios):

        partial_shading_ratio_number_of_modules_dictionary = {}

        for partial_shading_ratio_dictionary in partial_shading_ratios:

            partial_shading_ratio_value = partial_shading_ratio_dictionary['partial_shading_ratio']
            pv_module_index = partial_shading_ratio_dictionary['pv_module_index']

            if partial_shading_ratio_value in partial_shading_ratio_dictionary:
                partial_shading_ratio_number_of_modules_dictionary[partial_shading_ratio_value].append(pv_module_index)
            else:
                partial_shading_ratio_number_of_modules_dictionary[partial_shading_ratio_value] = [pv_module_index] 

        return partial_shading_ratio_number_of_modules_dictionary 

    def __get_partial_shading_ratio_single_diode_model_dictionary(self, operating_temperature, actual_irradiance, number_of_unshaded_modules, partial_shading_ratio_number_of_modules_dictionary):

        partial_shading_ratio_single_diode_model_dictionary = {}

        # For unshaded modules:
        single_diode_model_for_unshaded_modules = self.__get_single_diode_model_and_calculate(operating_temperature, actual_irradiance, 1.0, number_of_unshaded_modules)       
        partial_shading_ratio_single_diode_model_dictionary[1.0] = single_diode_model_for_unshaded_modules

        # For shaded modules:
        for partial_shading_ratio, modules in partial_shading_ratio_number_of_modules_dictionary.items():
            single_diode_model_for_shaded_modules = self.__get_single_diode_model_and_calculate(operating_temperature, actual_irradiance, partial_shading_ratio, len(modules))
            partial_shading_ratio_single_diode_model_dictionary[partial_shading_ratio] = single_diode_model_for_shaded_modules

        return partial_shading_ratio_single_diode_model_dictionary        

    # TODO: In the following code, series_resistance, shunt_resistance, and diode_quality_factor for one module are used for one unit of multiple modules.
    #       Modify the call root_finding to get more precise series_resistance, shunt_resistance, and diode_quality_factor for the entire unit of of multiple modules.
    def __get_single_diode_model_and_calculate(self, operating_temperature, actual_irradiance, partial_shading_ratio, number_of_corresponding_modules):

        overall_number_of_cells_in_series = self.number_of_cells_in_series * number_of_corresponding_modules

        overall_open_circuit_voltage = self.open_circuit_voltage * number_of_corresponding_modules

        single_diode_model = SingleDiodeModel(self.short_circuit_current, 
                                              overall_open_circuit_voltage, 
                                              overall_number_of_cells_in_series, 
                                              number_of_voltage_decimal_digits = self.number_of_voltage_decimal_digits, 
                                              temperature_voltage_coefficient = self.temperature_voltage_coefficient, 
                                              temperature_current_coefficient = self.temperature_current_coefficient, 
                                              series_resistance = self.series_resistance, 
                                              shunt_resistance = self.shunt_resistance, 
                                              diode_quality_factor = self.diode_quality_factor) 

        actual_irradiance_for_the_group_of_modules = actual_irradiance * partial_shading_ratio

        single_diode_model.calculate(operating_temperature, actual_irradiance_for_the_group_of_modules)

        return single_diode_model

    def __consolidate_calculated_values(self, partial_shading_ratio_single_diode_model_dictionary):

        self.voltages = []
        self.currents = []
        self.powers = []

        sorted_partial_shading_ratios = self.__sorted_keys_in_reverse(partial_shading_ratio_single_diode_model_dictionary)
        
        partial_shading_ratio_crossover_point_index_dictionary = self.__partial_shading_ratio_crossover_point_index_dictionary(partial_shading_ratio_single_diode_model_dictionary, sorted_partial_shading_ratios)

        for partial_shading_ratio in sorted_partial_shading_ratios:
            single_diode_model = partial_shading_ratio_single_diode_model_dictionary[partial_shading_ratio]

            if partial_shading_ratio in partial_shading_ratio_crossover_point_index_dictionary:

                crossover_point_index = partial_shading_ratio_crossover_point_index_dictionary[partial_shading_ratio]
                # Note: Since the second parameter for sublist is the length, value at the crossover_point_index is not included. 
                #       Value at the crossover_point_index is added as the first element of the list in the next single_diode_model. 
                self.__perform_voltage_addition_and_extend_voltage_array(single_diode_model.voltages[0:crossover_point_index])
                self.currents.extend(single_diode_model.currents[0:crossover_point_index])
 
            else: # Last single_diode_model
                self.__perform_voltage_addition_and_extend_voltage_array(single_diode_model.voltages)
                self.currents.extend(single_diode_model.currents)

            self.__calculate_powers()                    

    def __sorted_keys_in_reverse(self, dictionary):
        sorted_keys = list(dictionary.keys())
        sorted_keys.sort(reverse=True)

        return sorted_keys

    def __partial_shading_ratio_crossover_point_index_dictionary(self, partial_shading_ratio_single_diode_model_dictionary, sorted_partial_shading_ratios):

        partial_shading_ratio_crossover_point_index_dictionary = {}

        for index, partial_shading_ratio in enumerate(sorted_partial_shading_ratios):
           
            # Since use two consecutive single_diode_models:
            if index == len(sorted_partial_shading_ratios) - 1:
                break            

            first_single_diode_model = partial_shading_ratio_single_diode_model_dictionary[partial_shading_ratio]
            second_single_diode_model = partial_shading_ratio_single_diode_model_dictionary[sorted_partial_shading_ratios[index + 1]]

            short_circuit_current_of_second_module = second_single_diode_model.currents[0]           

            matching_current_value_in_first_module = min(first_single_diode_model.currents, key=lambda current:abs(current - short_circuit_current_of_second_module))

            crossover_point_index = self.__get_current_index_of_ndarray(matching_current_value_in_first_module, first_single_diode_model.currents)

            partial_shading_ratio_crossover_point_index_dictionary[partial_shading_ratio] = crossover_point_index

        return partial_shading_ratio_crossover_point_index_dictionary 

    def __get_current_index_of_ndarray(self, ndarray_current_value, current_ndarray):

        # 'item()' function from Numpy converts 'numpy.float64' to corresponding Python type float.
        float_current_value = ndarray_current_value.item()

        float_current_values = [current.item() for current in current_ndarray]

        current_index = float_current_values.index(float_current_value)

        return current_index 

    def __perform_voltage_addition_and_extend_voltage_array(self, adding_voltages):

        if len(self.voltages) == 0.0:
            largest_voltage_in_voltage_array = 0.0
        else:
            # Last element holds the largest value:
            # Note: Since it's Numpy array, the following syntax doesn't work:
            # largest_voltage_in_voltage_array = self.voltages[-1]
            largest_voltage_in_voltage_array = self.voltages[len(self.voltages) - 1]

        voltages_after_addition = [largest_voltage_in_voltage_array + voltage for voltage in adding_voltages]

        self.voltages.extend(voltages_after_addition)

    def __calculate_powers(self):

        self.powers = []

        for index in range(len(self.voltages)):
            self.powers.append(self.voltages[index] * self.currents[index])

