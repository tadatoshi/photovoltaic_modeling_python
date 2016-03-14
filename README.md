# PhotovoltaicModelingPython

Calculates the parameters that are not available in the datasheet of photovoltaic modules. In order to do so, equations derived from the diode model are used. Due to the complexity of the equations, numerical method is used to get the parameters. 

Also calculates the values for I-V curve and P-V curve based on single diode model. Can draw I-V curve and P-V curve graphs as well. 

## Installation

#### Required packages

* numpy

* scipy

Automatically installed when this package is installed. 

#### Installation instruction

Use ``pip3``:

```
pip3 install photovoltaic_modeling
```

## Supported Platforms

* Python 3.5. 

It's not tested on Python 2.6 or 2.7 yet. 

### Assumptions

* Unit of temperature voltage coefficient: [V/ºC] not [%/ºC]. 

    Different datasheets use different unit (either one of these units). If it's given in [%/ºC] in datasheet, make sure to convert it to [V/ºC]. 

* Unit of temperature current coefficient: [A/ºC] not [%/ºC]. 

    Different datasheets use different unit (either one of these units). If it's given in [%/ºC] in datasheet, make sure to convert it to [A/ºC].

* Definition of thermal voltage:

    ```
        Vt = (AkT) / q

        where, Vt: Thermal voltage, A: Diode quality factor, k: Boltzmann constant, T: Temperature at Standard Test Condition (STC),  q: charge of electron
    ```
    This is the definition from reference [1]

    Some literatures use 
    ```
        Vt = (nkT) / q

        where, n: number of cells in series
    ```
    For example, reference [2]

    But this project uses the first definition above and all the equations are adjusted accordingly.  

## Usage

### Code

1. Parameter Extraction

    Example:

    ```
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
    ```

2. Single diode model

    Note: Use series_resistance, shunt_resistance, and diode_quality_factor obtained by "1. Parameter Extraction" above. 

    Example:

    ```
    from photovoltaic_modeling.diode_model.single_diode_model import SingleDiodeModel
    import matplotlib.pyplot as pyplot
    import photovoltaic_modeling.diode_model.report_helper as report_helper
    
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
    
    operating_temperature = 35 + 273
    actual_irradiance = 1000
    
    single_diode_model.calculate(operating_temperature, 
                                 actual_irradiance)
    
    voltages = single_diode_model.voltages
    currents = single_diode_model.currents
    powers = single_diode_model.powers
    
    report_helper.write_result_to_csv_file(single_diode_model, 'single_diode_model_rng-100d_one_module_no_shading')
    report_helper.plot_result(single_diode_model)
    ```

### Command line execution

1. Parameter Extraction:

    Example:

    ```
    $ photovoltaic_modeling parameter_extraction --short_circuit_current 3.87 --open_circuit_voltage 42.1 --maximum_power_point_current 3.56 --maximum_power_point_voltage 33.7 --number_of_cells_in_series 72
    ```

## Development



## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/tadatoshi/photovoltaic_modeling_python. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](contributor-covenant.org) code of conduct.

## License

The project is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

## References

[1] D. Sera, R. Teodorescu, and P. Rodriguez, "PV panel model based on datasheet values," in Industrial Electronics, 2007. ISIE 2007. IEEE International Symposium on, 2007, pp. 2392-2396.

[2] M. G. Villalva and J. R. Gazoli, ”Comprehensive approach to modeling and simulation of photovoltaic arrays,” Power Electronics, IEEE Trans- actions on, vol. 24, pp. 1198-1208, 2009.

[3] A. Bellini, S. Bifaretti, V. Iacovone, and C. Cornaro, ”Simplified model of a photovoltaic module,” in Applied Electronics, 2009. AE 2009, 2009, pp. 47-51.
