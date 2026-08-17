from pathlib import Path

path = "tests/step2/valid.json"


def is_number(num: str):
    try:
        float(num)
        return True
    except ValueError:
        return False


class Parser:
    def __init__(self) -> None:
        self.tokenized_list = []
        self.expected_token = ["LEFTBRACE", "RIGHTBRACE"]
        self.index = 0

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
                    return "{}"
                return json_contents

    def tokenize_json(self, path):
        """
        Tokenize the Jason
        """

        json_contents = self.open_json(path)
        in_string = False
        current_string = ""
        for token in json_contents:
            # print(token)
            if token == "{":
                self.tokenized_list.append({"LEFT_BRACE": None})
            elif token == "}":
                self.tokenized_list.append({"RIGHT_BRACE": None})
            elif token == "[":
                self.tokenized_list.append({"LEFT_BRACKET": None})
            elif token == "]":
                self.tokenized_list.append({"RIGHT_BRACKET": None})
            elif token == ":":
                self.tokenized_list.append({"COLON": None})
            elif token == ";":
                self.tokenized_list.append({"SEMI_COLON": None})
            elif token == ",":
                self.tokenized_list.append({"COMMA": None})
            elif token.lower() == "true":
                self.tokenized_list.append({"BOOLEAN": True})
            elif token.lower() == "false":
                self.tokenized_list.append({"BOOLEAN": False})
            elif is_number(token):
                self.tokenized_list.append({"INT": token})

            if token == '"' and not in_string:
                in_string = True
            elif token == '"' and in_string:
                in_string = False
                self.tokenized_list.append({"STRING": current_string})
                current_string = ""

            if in_string and token != '"':
                current_string += token

        # print(self.tokenized_list)
        return self.tokenized_list

    def parse_object(self):
        object_value = []
        object = {}
        for token in self.tokenized_list:
            print("parsed object token is ", token)
            matching_key = set(self.expected_token).intersection(token)
            if "STRING" in matching_key:
                print("token is a string")
                print(token)
                object_value.append(token["STRING"])
                # self.tokenized_list.remove(token)
                if len(object_value) == 2:
                    object[object_value[0]] = object_value[1]
                    object_value = []
                self.expected_token = ["COLON"]
            if "COLON" in matching_key:
                print(token)
                self.expected_token = [
                    "STRING",
                    "LEFT_BRACE",
                    "LEFT_BRACKET",
                    "NUMBER",
                    "BOOLEAN",
                ]
            elif "RIGHT_BRACE" in matching_key:
                print(token)
                return object

        return object

    def parse_array(self): ...

    def parse_value(self, parent=None):
        for token in self.tokenized_list:
            # print("token is: ")
            # print(token.keys())
            if "LEFT_BRACE" in token:
                print("found an object")
                self.tokenized_list.remove(token)
                self.expected_token = ["RIGHT_BRACE", "STRING"]
                object = self.parse_object()
                if parent is None:
                    parent = object

        return parent

    def parse_json(self, path=path):
        if len(self.tokenized_list) == 0:
            self.tokenize_json(path)
        print("Tokenized list")
        print(self.tokenized_list)

        parsed_json = self.parse_value()

        print("parsed json is a ", type(parsed_json))
        print(parsed_json)
        return parsed_json


if __name__ == "__main__":
    parser = Parser()
    parser.parse_json()
