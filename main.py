from tool.case import Case
import matplotlib.pyplot as plt


validation_cases = ('validation-12_95', 'validation-13_34', 'validation-13_71',
                    'validation-14_33', 'validation-14_78')
validation_results = (23.75, 25.5, 27.25, 29.25, 30.75)


def validation_plotter(velocities, results, percent_errors, percent_errors2):
    # Results vs validation data
    ax1 = plt.subplot(221)
    ax1.plot(velocities, results, marker="o", label="Tool output")
    ax1.plot(velocities, validation_results, marker="^", label="Validation data")
    ax1.set_ylabel("D [N]")
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.legend()

    # Results vs validation fit curve
    ax2 = plt.subplot(222, sharey=ax1)
    y = list(0.142 * velocity ** 2 for velocity in velocities)
    ax2.plot(velocities, results, marker="o", label="Tool output")
    ax2.plot(velocities, y, marker="^", label="Validation fit curve")
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    ax2.legend()

    # Errors vs validation data
    ax3 = plt.subplot(223)
    ax3.plot(velocities, percent_errors, marker="v", label="$\Delta$ from data", color="red")
    ax3.set_xlabel("$V_{flow} [m/s]$")
    ax3.set_ylabel("$\Delta D [\%]$")
    ax3.legend()

    ax4 = plt.subplot(224, sharey=ax3)
    ax4.plot(velocities, percent_errors2, marker="v", label="$\Delta$ from fit curve", color="red")
    ax4.set_xlabel("$V_{flow} [m/s]$")
    plt.setp(ax4.get_yticklabels(), visible=False)
    ax4.legend()

    plt.subplots_adjust(left=.085, bottom=.1, right=.986, top=.986, wspace=.04, hspace=.04)
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

    elif case == 'slowdown' or case == 's':
        Case('template_case').plot_slowdown()

    elif case == 'all' or case == 'a':
        for case in ('quadcopter', 'helipack', 'icecream'):
            runner = Case(case)
            runner.run_case()
            runner.write_to_file()

    elif case == 'q':
        exit()

    else:
        runner = Case(case)
        runner.run_case()
        runner.write_to_file()
