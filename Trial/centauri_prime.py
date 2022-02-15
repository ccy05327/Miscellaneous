# TODO: Complete the get_ruler function
def get_ruler(kingdom):
    ruler = ''
    # TODO: Add logic to determine the ruler of the kingdom
    vowels = ['a', 'e', 'i', 'o', 'u']
    if kingdom[-1] in vowels:
        ruler = 'Alice'
    if kingdom[-1] not in vowels and kingdom[-1] != 'y':
        ruler = 'Bob'
    if kingdom[-1] == 'y':
        ruler = 'nobody'
    # It should be either 'Alice', 'Bob' or 'nobody'.
    return ruler


def main():
    # Get the number of test cases
    T = int(input())
    for t in range(T):
        # Get the kingdom
        kingdom = input()
        print('Case #%d: %s is ruled by %s.' %
              (t + 1, kingdom, get_ruler(kingdom)))
        print(len(kingdom))


if __name__ == '__main__':
    main()
