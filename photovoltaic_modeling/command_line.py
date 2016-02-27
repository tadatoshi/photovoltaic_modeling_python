import argparse

def main():

    '''
    Based on https://docs.python.org/3.5/library/argparse.html#sub-commands

    Examples
    -----------

    Parameter Extraction:
    $ photovoltaic_modeling parameter_extraction --short_circuit_current 3.87 --open_circuit_voltage 42.1 --maximum_power_point_current 3.56 --maximum_power_point_voltage 33.7 --number_of_cells_in_series 72
    '''

    parser = argparse.ArgumentParser(prog='Executes a specified root finding')

    # "dest": the name of the variable that holds the name of subparser.
    subparsers = parser.add_subparsers(title='name', dest='name')

    parser_parameter_extraction = subparsers.add_parser('parameter_extraction')
    parser_parameter_extraction.add_argument('--short_circuit_current', nargs='?', type=float, required=True)
    parser_parameter_extraction.add_argument('--open_circuit_voltage', nargs='?', type=float, required=True)
    parser_parameter_extraction.add_argument('--maximum_power_point_current', nargs='?', type=float, required=True)
    parser_parameter_extraction.add_argument('--maximum_power_point_voltage', nargs='?', type=float, required=True)
    parser_parameter_extraction.add_argument('--number_of_cells_in_series', nargs='?', type=float, required=True)
    parser_parameter_extraction.add_argument('--series_resistance_estimate', nargs='?', type=float, default=1)
    parser_parameter_extraction.add_argument('--shunt_resistance_estimate', nargs='?', type=float, default=1000)
    parser_parameter_extraction.add_argument('--diode_quality_factor_estimate', nargs='?', type=float, default=1)
    # Note: Calls execute_parameter_extraction function with the arguments:
    parser_parameter_extraction.set_defaults(func=execute_parameter_extraction)

    args = parser.parse_args()
    # Calls the function specified in "set_defaults" method:
    args.func(args)

def execute_parameter_extraction(args):
    from photovoltaic_modeling.parameter.parameter_extraction import ParameterExtraction
    parameter_extraction = ParameterExtraction(args.short_circuit_current, args.open_circuit_voltage, 
                                               args.maximum_power_point_current, args.maximum_power_point_voltage, 
                                               number_of_cells_in_series = args.number_of_cells_in_series)

    parameter_estimates = [args.series_resistance_estimate, args.shunt_resistance_estimate, args.diode_quality_factor_estimate]
    parameter_extraction.calculate(parameter_estimates)

    print('series_resistance=', parameter_extraction.series_resistance)
    print('shunt_resistance=', parameter_extraction.shunt_resistance)
    print('diode_quality_factor=', parameter_extraction.diode_quality_factor)

if __name__ == "__main__":
    main() 