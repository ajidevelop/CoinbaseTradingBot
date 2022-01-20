import enum


class ValidInputType(enum.Enum):
    number = 1
    str = 2


class ValidInput:

    def __init__(self, valid_type, valid_result: list):
        self.result = ''
        self.type = ValidInputType[valid_type]
        self.valid_result = valid_result

    def input(self, msg: str):
        while self.result == '':
            self.result = input(msg)
            if self.type is ValidInputType.number:
                try:
                    self.result = float(self.result)
                    assert self.result in self.valid_result
                except (ValueError, AssertionError) as e:
                    self.result = ''
                    print('Please enter a valid number')
            elif self.type is ValidInputType.str:
                if self.result not in self.valid_result:
                    self.result = ''
                    print('Please enter a valid input')

        return self.result


print('Welcome to Coinbase Trading Bot')
user_input = ValidInput('number', [1, 2]).input('Would you like to:\n1. View SLTP orders\n2. Set SLTP orders: ')
