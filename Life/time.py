'''
- [x] Write a program that outputs the whole cycle for the input hour-day (24-hour day vs. 26-hour day)
- [ ] Separate function for checking what time is equivalent to the other hour-day. (Convertion)

'''
RESET = "\033[0m"
RED = "\033[0;31m"


def hour_day(_user_define_hour, _hour=24):
    _user_define_hour_list = range(_user_define_hour)
    _hour_list = range(_hour)
    while True:
        day = int(input("    How many days do you want to output? "))
        # input validation
        if (day == 0):
            print(RED+"    Days cannot be zero"+RESET)
            continue
        if (day > _user_define_hour/2):
            print(RED+"    Too many days"+RESET)
            continue

        print("    What hour-day you want to base the day on you just entered? \
              \n    [1] {}-hour\n    [2] {}-hour".format(_user_define_hour, _hour))
        hour_base_index = input("    Your choice: ")
        try:
            hour_base_index = int(hour_base_index)
            # input validation
            if (hour_base_index != 1 and hour_base_index != 2):
                print(hour_base_index, type(hour_base_index))
                print(RED+"    Please enter one of the options"+RESET)
                continue
            # assign depend on option chose by user
            if (hour_base_index == 1):
                hour_base = _user_define_hour
            elif (hour_base_index == 2):
                hour_base = _hour
        except(ValueError):
            print(RED+ValueError.with_traceback+RESET)
            break

        # Actual printing
        print("\n  ⁘⁘⁘⁘ DAY 1 ⁘⁘⁘⁘")
        for i in range(hour_base*day):
            print("  {:>4}  »  {:<4}".format(
                _user_define_hour_list[i % _user_define_hour], _hour_list[i % _hour]))
            # print separater after each day ends
            if (i % hour_base == hour_base-1):
                # print END when reach the end
                if (i+1 == hour_base*day):
                    print("  ⁘⁘⁘⁘ END ⁘⁘⁘⁘")
                    break
                # separator including day number
                print("  ⁘⁘⁘⁘ DAY {} ⁘⁘⁘⁘".format(str(round(i / hour_base)+1)))
        break


def take_input():
    print("\n    This is an application for converting times between two different hour-worlds. \n")
    print("    Please enter two numbers (over 24) separated by a space,\n    if you want to convert between your choice and the 24-hour world,\n    you can eliminate typing 24.\n")
    
    while True:
        user_input = input("    Enter hour: ")
        try:
            user_input = user_input.split(' ')
            # input validation
            # Length 1 correct
            if (len(user_input) == 1):
                hour = int(user_input[0])
                # content validation - hours has to be within reason
                if (hour < 24):
                    print(RED+"    Can't be under 24 hours"+RESET)
                    continue
                if (hour == 24):
                    print(RED+"    The default is already 24, can't be the same number"+RESET)
                    continue
                hour_day(hour)
                break
            # Length 2 correct
            if (len(user_input) == 2):
                hour1 = int(user_input[0])
                hour2 = int(user_input[1])
                # content validation
                if (hour1 == hour2):
                    print(RED+"    Can't be the same number"+RESET)
                    continue
                if (hour1 < 24 or hour2 < 24):
                    print(RED+"    Can't be under 24 hours"+RESET)
                    continue
                hour_day(hour1, hour2)
                break
            # Length 3+ incorrect
            if (len(user_input) > 2):
                print(RED+"    Too much input"+RESET)
        except(ValueError):
            print(RED+ValueError.with_traceback+RESET)
            break


def main():
    take_input()


if __name__ == "__main__":
    main()
