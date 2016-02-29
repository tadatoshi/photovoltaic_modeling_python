def write_result_to_csv_file(model, model_name):
    import csv

    file_name = generate_result_file_name(model_name, 'csv')
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['voltage', 'current', 'power'])
        for i in range(len(model.voltages)):
            writer.writerow([model.voltages[i], model.currents[i], model.powers[i]])

def plot_result(model):
    import matplotlib.pyplot as pyplot

    pyplot.plot(model.voltages, model.currents)
    pyplot.xlabel('Voltage [V]')
    pyplot.ylabel('Current [A]')
    pyplot.title('I-V curve')
    pyplot.show(block=False)

    pyplot.figure()
    pyplot.plot(model.voltages, model.powers)
    pyplot.xlabel('Voltage [V]')
    pyplot.ylabel('Power [W]')
    pyplot.title('P-V curve')
    pyplot.show()

def generate_result_file_name(model_name, file_extension):
    from datetime import datetime
    return model_name + '_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.' + file_extension