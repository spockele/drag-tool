from tool.case import Case

validation_cases = ('validation-04_00', 'validation-12_95', 'validation-13_34', 'validation-13_71',
                    'validation-14_33', 'validation-14_78')
validation_results = (2.38, 23.75, 25.5, 27.25, 29.25, 30.75)


if __name__ == '__main__':
    case = input('Enter the case name: ')

    if case == 'validation':
        results = []
        for validation_case in validation_cases:
            runner = Case(validation_case)
            results.append(runner.run_case())

        for index, result in enumerate(results):
            error = round(result[1] - validation_results[index], 3)
            percent_error = round(error / validation_results[index] * 100, 1)

            print(f"Drag area at {result[0]} m/s: {round(result[2], 3)}")
            print(f"Error at {result[0]} m/s: {error} N ({percent_error} %)")
