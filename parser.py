from pathlib import Path
import time

path = "tests/step1/valid.json"


def is_number(num: str):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_letter(char: str):
    return char.isalpha()


class Parser:
    def __init__(self) -> None:
        self.tokenized_list = []
        self.parser_index = 0
        self.lexer_index = 0

    def expect(self, Required_token_type):
        print(self.tokenized_list[self.parser_index])
        if Required_token_type in self.tokenized_list[self.parser_index]:
            self.parser_index += 1
            return 0
        return 1

    def open_json(self, path: str):
        """
        Opens the json
        """
        if path is not None:
            with open(path, "rt") as f:
                json_contents = f.read()
                total_char = len(json_contents)
                # print(json_contents)
                # print(total_char)
                if total_char == 0:
                    raise SyntaxError("Invalid JSON")
                print("total char is", total_char)
                return json_contents

    def tokenize_json(self, path):
        """
        Tokenize the json
        """
        json_contents = self.open_json(path)

        print(json_contents)

        while True:
            print("Token was ", json_contents[self.lexer_index - 1])
            print("lexer index is ", self.lexer_index)
            if self.lexer_index > len(json_contents) - 1:
                print("json length is ", len(json_contents))
                print("Done tokenizing")
                break
            elif json_contents[self.lexer_index] == "{":
                self.tokenized_list.append({"LEFT_BRACE": None})
                self.lexer_index += 1
            elif json_contents[self.lexer_index] == "}":
                self.tokenized_list.append({"RIGHT_BRACE": None})
                self.lexer_index += 1
            elif json_contents[self.lexer_index] == "[":
                self.tokenized_list.append({"LEFT_BRACKET": None})
                self.lexer_index += 1
            elif json_contents[self.lexer_index] == "]":
                self.tokenized_list.append({"RIGHT_BRACKET": None})
                self.lexer_index += 1
            elif json_contents[self.lexer_index] == ":":
                self.tokenized_list.append({"COLON": None})
                self.lexer_index += 1
            elif json_contents[self.lexer_index] == ";":
                self.tokenized_list.append({"SEMI_COLON": None})
                self.lexer_index += 1
            elif json_contents[self.lexer_index] == ",":
                self.tokenized_list.append({"COMMA": None})
                self.lexer_index += 1
            elif json_contents[self.lexer_index] == '"':
                self.lexer_index += 1
                string = ""
                while True:
                    if json_contents[self.lexer_index] == '"':
                        self.tokenized_list.append({"STRING": string})
                        self.lexer_index += 1
                        break
                    else:
                        string += json_contents[self.lexer_index]
                        self.lexer_index += 1
            elif is_letter(json_contents[self.lexer_index]):
                string = ""
                while is_letter(json_contents[self.lexer_index]):
                    string += json_contents[self.lexer_index]
                    self.lexer_index += 1
                if string == "true":
                    self.tokenized_list.append({"BOOLEAN": True})
                elif string == "false":
                    self.tokenized_list.append({"BOOLEAN": False})
                elif string == "null":
                    self.tokenized_list.append({"NONETYPE": None})
            elif is_number(json_contents[self.lexer_index]):
                print("is a number")
                num = ""
                if json_contents[self.lexer_index - 1] != " ":
                    print("INVALID JSON")
                    return 1
                while is_number(json_contents[self.lexer_index]):
                    num += json_contents[self.lexer_index]
                    self.lexer_index += 1
                self.tokenized_list.append({"FLOAT": float(num)})
            elif (
                json_contents[self.lexer_index] == " "
                or json_contents[self.lexer_index] == "\n"
                or json_contents[self.lexer_index] == "\t"
                or json_contents[self.lexer_index] == "\r"
            ):
                self.lexer_index += 1
            else:
                print(self.lexer_index)
                print(json_contents[self.lexer_index], "IS AN INVALID CHARACTER")
                self.tokenized_list = []
                raise SyntaxError("Invalid JSON")

        # print("lexer index is ", self.lexer_index)
        print(self.tokenized_list)
        return self.tokenized_list

    def parse_object(self):
        value = None
        key = None
        object = {}
        comma_ending = False

        while True:
            if self.expect("STRING") == 0:
                print("current token is ", self.tokenized_list[self.parser_index - 1])
                key = self.tokenized_list[self.parser_index - 1]["STRING"]
            elif self.expect("RIGHT_BRACE") == 0 and not comma_ending:
                return object
            else:
                raise SyntaxError("Invalid JSON")
            if self.expect("COLON") == 0:
                print("current token is ", self.tokenized_list[self.parser_index - 1])
            else:
                raise SyntaxError("Invalid JSON")
            if self.expect("STRING") == 0:
                value = self.tokenized_list[self.parser_index - 1]["STRING"]
                object[key] = value
            elif self.expect("BOOLEAN") == 0:
                value = self.tokenized_list[self.parser_index - 1]["BOOLEAN"]
                object[key] = value
            elif self.expect("FLOAT") == 0:
                value = self.tokenized_list[self.parser_index - 1]["FLOAT"]
                object[key] = value
            elif self.expect("NONETYPE") == 0:
                value = self.tokenized_list[self.parser_index - 1]["NONETYPE"]
                object[key] = value
            elif self.expect("LEFT_BRACE") == 0 or self.expect("LEFT_BRACKET") == 0:
                self.parser_index -= 1
                value = self.parse_value()
                object[key] = value
            else:
                raise SyntaxError("Invalid JSON")
            if self.expect("RIGHT_BRACE") == 0:
                return object
            elif self.expect("COMMA") == 0:
                value = None
                key = None
                comma_ending = True
            else:
                raise SyntaxError("Invalid JSON")

        return object

    def parse_array(self):
        array = []

        while True:
            if self.expect("RIGHT_BRACKET") == 0:
                return array
            elif self.expect("STRING") == 0:
                array.append(self.tokenized_list[self.parser_index])
            else:
                raise SyntaxError("Invalid JSON")

        return array

    def parse_value(self, parent=None):
        if "LEFT_BRACE" in self.tokenized_list[self.parser_index]:
            self.parser_index += 1
            return self.parse_object()
        elif "LEFT_BRACKET" in self.tokenized_list[self.parser_index]:
            self.parser_index += 1
            return self.parse_array()
        elif "NONETYPE" in self.tokenized_list[self.parser_index]:
            return self.tokenized_list[self.parser_index]
        return parent

    def parse_json(self, path=path):
        if len(self.tokenized_list) == 0:
            success = self.tokenize_json(path)
            if success == 1:
                print("ERROR INVALID JSON")
                raise SyntaxError("Invalid JSON")
        print("Tokenized list")
        print(self.tokenized_list)

        parsed_json = self.parse_value()

        if parsed_json == 1:
            print("ERROR INVALID JSON")
            return

        print("parsed json is a ", type(parsed_json))
        print(parsed_json)
        return parsed_json


if __name__ == "__main__":
    parser = Parser()
    parser.parse_json()
