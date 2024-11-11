class RedisParser():
    def parse(self, data):
        self.index = 0
        self.data = data
        return self.root_parser()

    def root_parser(self):
        if self.data[self.index] == '*':
            return self.array_parser()
        if self.data[self.index] == '$':
            return self.bulk_string_parser()
        if self.data[self.index] == '+':
            return self.simple_string_parser()
        if self.data[self.index] == '-':
            return self.error_parser()
        if self.data[self.index] == ':':
            return self.integer_parser()
        raise ValueError("Unsupported RESP type")

    def simple_string_parser(self):
        end = self.data.find('\r\n', self.index)
        if end == -1:
            raise ValueError("Invalid Simple String")
        simple_str = self.data[self.index + 1:end]
        self.index = end + 2
        return simple_str

    def error_parser(self):
        message = self.simple_string_parser()
        return f"Error: {message}"

    def integer_parser(self):
        integer_str = self.simple_string_parser()
        return int(integer_str)

    def bulk_string_parser(self):
        end = self.data.find('\r\n', self.index)
        if end == -1:
            raise ValueError("Invalid Bulk String")
        str_length = int(self.data[self.index + 1:end])
        self.index = end + 2
        if str_length == -1:
            return None
        end = self.index + str_length
        string = self.data[self.index:end]
        self.index = end + 2
        return string

    def array_parser(self):
        end = self.data.find('\r\n', self.index)
        if end == -1:
            raise ValueError("Invalid Array")
        num_elements = int(self.data[self.index + 1:end])
        self.index = end + 2
        if num_elements == -1:
            return None
        return [self.root_parser() for _ in range(num_elements)]
    