from tool.case import Case

validation_cases = ('validation-04_00', 'validation-12_95', 'validation-13_34', 'validation-13_71',
                    'validation-14_33', 'validation-14_78')
validation_results = (2.38, 23.75, 25.5, 27.25, 29.25, 30.75)


if __name__ == '__main__':
    case = input('Enter the case name: ')

    if case == 'validation' or case == 'v':
        results = []
        for validation_case in validation_cases:
            runner = Case(validation_case)
            results.append(runner.run_case())

        for index, result in enumerate(results):
            drag_error = round(result[1] - validation_results[index], 3)
            drag_percent_error = round(drag_error / validation_results[index] * 100, 1)

            acd_error = round(result[2] - validation_results[index] /
                              (0.5 * 1.225 * result[0] ** 2), 3)
            acd_percent_error = round(acd_error / (validation_results[index] /
                                      (0.5 * 1.225 * result[0] ** 2)) * 100, 1)

            print(f"Drag at {result[0]} m/s: {round(result[1], 3)} N, {round(result[2], 3)}")
            print(f"Drag Error at {result[0]} m/s: {drag_error} N ({drag_percent_error} %)")
            print(f"AC_d Error at {result[0]} m/s: {acd_error} [-] ({acd_percent_error} %)\n")
