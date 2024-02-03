import msvcrt


def wait_for_key():
    msvcrt.getch()
    # while True:
    #     if msvcrt.kbhit():
    #         return msvcrt.getch()
