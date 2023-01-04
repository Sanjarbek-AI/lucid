async def is_valid(number):
    if len(number) == 12 or len(number) == 9:
        try:
            int(number)
            return True
        except Exception as exc:
            print(exc)
            return False
    else:
        return False
