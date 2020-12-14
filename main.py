from tool.case import Case
import matplotlib.pyplot as plt


validation_cases = ('validation-12_95', 'validation-13_34', 'validation-13_71',
                    'validation-14_33', 'validation-14_78')
validation_results = (23.75, 25.5, 27.25, 29.25, 30.75)

sensitivity_dimensions = {'quadcopter': (.1, .2, .3, .4, .5),
                          'helipack': (.4, .5, .6, .7, .8),
                          'icecream': (.5, .7, .9, 1.1, 1.3)
                          }
scaled_dimensions = {'quadcopter': 'Body Radius',
                     'helipack': 'Battery Width',
                     'icecream': 'Cabin Radius'
                     }


def validation_plotter(velocities, results, percent_errors, percent_errors2):
    plt.subplots(figsize=(8, 3), dpi=150)
    # Results vs validation data
    ax1 = plt.subplot(121)

    ax1.plot(results, velocities, marker="o", label="Tool output")
    ax1.plot(validation_results, velocities, marker="^", label="Validation data")

    y = list(0.142 * velocity ** 2 for velocity in velocities)
    ax1.plot(y, velocities, marker="v", label="Validation fit curve")

    ax1.set_xlabel("D [N]")
    ax1.set_ylabel("$V_{flow} [m/s]$")
    ax1.legend()

    # Errors vs validation data
    ax3 = plt.subplot(122, sharey=ax1)
    ax3.plot(min(percent_errors), min(velocities), marker=None, color=None)

    ax3.plot(percent_errors, velocities, marker="^", label="$\Delta$ from data")
    ax3.plot(percent_errors2, velocities, marker="v", label="$\Delta$ from fit curve")

    plt.setp(ax3.get_yticklabels(), visible=False)
    ax3.set_xlabel("$\Delta D [\%]$")
    ax3.legend()

    plt.subplots_adjust(left=.09, bottom=.15, right=.99, top=.99, wspace=.02, hspace=.2)
    plt.show()


def sensitivity_plotter(results):
    plt.subplots(figsize=(8, 3), dpi=180)
    for index, concept in enumerate(('quadcopter', 'helipack', 'icecream')):
        ax = plt.subplot(1, 3, index + 1)
        ax.plot(sensitivity_dimensions[concept], results[concept], marker='o')
        ax.set_xlabel(f'{scaled_dimensions[concept]} $[m]$')
        if not index:
            plt.ylabel('$S_{ref}\ C_D [m^2]$')

    plt.subplots_adjust(left=.075, bottom=.155, right=.99, top=.99, wspace=.3, hspace=.2)
    plt.show()


if __name__ == '__main__':
    case = input('Enter the case name: ')

    if case == 'validation' or case == 'v':
        velocities = []
        results = []
        drag_errors = []
        drag_percent_errors = []
        drag_error2s = []
        drag_percent_error2s = []

        for index, validation_case in enumerate(validation_cases):
            runner = Case("validation/" + validation_case)
            velocity, result = runner.run_case()

            velocities.append(velocity)
            results.append(result[0])

            drag_error = round(result[0] - validation_results[index], 3)
            drag_percent_error = round(drag_error / validation_results[index] * 100, 1)
            drag_errors.append(drag_error)
            drag_percent_errors.append(drag_percent_error)

            acd_error = round(result[1] - validation_results[index] /
                              (0.5 * 1.225 * velocity ** 2), 3)
            acd_percent_error = round(acd_error / (validation_results[index] /
                                      (0.5 * 1.225 * velocity ** 2)) * 100, 1)

            drag_error2 = round(result[0] - 0.143 * velocity ** 2, 3)
            drag_percent_error2 = round(drag_error2 / (0.143 * velocity ** 2) * 100, 1)
            drag_error2s.append(drag_error2)
            drag_percent_error2s.append(drag_percent_error2)

            print(f"Drag at {velocity} m/s: {round(result[0], 3)} N, {round(result[1], 3)}")
            print(f"Drag Error from exact experiment: {drag_error} N "
                  f"({drag_percent_error} %)")
            print(f"AC_d Error from exact experiment: {acd_error} [-] "
                  f"({acd_percent_error} %)")
            print(f"Drag Error from experimental fit curve: {drag_error2} N "
                  f"({drag_percent_error2} %)\n")

            runner.write_to_file()

        validation_plotter(velocities, results, drag_percent_errors, drag_percent_error2s)

    elif case == 'slowdown':
        Case('template_case').plot_slowdown()

    elif case == 'all' or case == 'a':
        for case in ('quadcopter', 'helipack', 'icecream'):
            runner = Case(case)
            runner.run_case()
            runner.write_to_file()

    elif case == 'sensitivity' or case == 's':
        results = {}
        for name in ('quadcopter', 'helipack', 'icecream'):
            results[name] = []

            for index in range(5):
                runner = Case(f'sensitivity_analysis/{name}_{index}')
                velocity, result = runner.run_case()
                runner.write_to_file()

                results[name].append(result[1])

        sensitivity_plotter(results)

    elif case == 'q':
        exit()

    else:
        runner = Case(case)
        runner.run_case()
        runner.write_to_file()
