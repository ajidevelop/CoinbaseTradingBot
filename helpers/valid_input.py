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
                    assert (self.result in self.valid_result or len(self.valid_result) is 0)
                except (ValueError, AssertionError) as e:
                    self.result = ''
                    print('Please enter a valid number')
            elif self.type is ValidInputType.str:
                if self.result not in self.valid_result and len(self.valid_result) is not 0:
                    self.result = ''
                    print('Please enter a valid input')

        return self.result
