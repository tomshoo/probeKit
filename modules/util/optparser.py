import sys
from typing import Any
from modules.util.extra import string
from rich import traceback

traceback.install()


class OptionsParser:
    """
    Parse the dictionary read from `config.json`
    Assign desired values to the value key for each value
    """

    def __init__(self, option_dict: dict[str, Any]) -> None:
        self.option_dict = option_dict

    def __typeset(self, dtype: str):
        """
        Return the type object required as per the `dtype` key found in the scheme
        """
        dtype = dtype.lower()
        if dtype == "str":
            return str
        elif dtype == "int":
            return int
        elif dtype == "float":
            return float
        elif dtype == "bool":
            return bool
        else:
            raise Exception(f"Invalid dtype value '{dtype}'")

    def __dictparser(self, data: str) -> None:
        """
        Parse the value where type of value is specified as a dictionary
        If type is mentioned as dictionary, the value is a dictionary containing two values:
         - value: containing the value that needs to be sent to module
         - type: the type of value,
           - This key would not hold the data-type of the value,
           - It hold the type mentioned in the module, for example:
             module: probe, option: tport, (value: 1/8000, type: range)/(value: 1,8000, type: group)
        """
        option_dict: dict = self.option_dict
        data_value: dict = option_dict[data]["value"]
        data_rules: dict = option_dict[data]["typerules"]
        if type(data_value["value"]) is str:
            for scheme in data_rules:
                rule: dict = data_rules.get(scheme)
                identifier: str = rule.get("identifier")
                if identifier:
                    if identifier in data_value["value"]:
                        if rule.get("type") == "list":
                            data_value["type"] = scheme
                            if rule.get("delimeter"):
                                data_value["value"] = data_value["value"].split(
                                    rule.get("delimeter")
                                )
                                break
                            else:
                                print("Err: no delimeter found... cannot split.")
                        else:
                            dtype = rule.get("dtype")
                            dtype = self.__typeset(dtype)
                            data_value["value"] = dtype(data_value["value"])
                            data_value["type"] = scheme
                            break
                else:
                    dtype = self.__typeset(rule.get("dtype"))
                    data_value["value"] = (
                        ""
                        if not data_value.get("value")
                        and type(data_value.get("value")) is str
                        else dtype(data_value.get("value"))
                    )
                    data_value["type"] = scheme
        self.option_dict = option_dict

    def parse(self) -> dict:
        """
        Parse the option dictionary assigning appropriate values for the options
        """
        option_dict = self.option_dict
        for data in option_dict:
            if option_dict[data].get("value") is None:
                if option_dict[data].get("type") == "dict":
                    option_dict[data]["value"] = {"value": "", "type": ""}
                else:
                    option_dict[data]["value"] = ""

            if option_dict[data].get("type"):
                if option_dict[data]["type"] == "dict":
                    if not option_dict[data].get("typerules"):
                        print("Err: No type rule found... skipping value")
                    else:
                        if type(option_dict[data]["typerules"]) is not dict:
                            print("Invalid type rule scheme... skipping value")
                        else:
                            try:
                                self.__dictparser(data)
                            except TypeError as e:
                                print(f"Something went wrong... => {e}")
                    pass

                elif option_dict[data]["type"] == "int":
                    if type(option_dict[data]["value"]) is not int:
                        if option_dict[data]["value"].isdecimal():
                            option_dict[data]["value"] = int(option_dict[data]["value"])
                        else:
                            option_dict[data]["value"] = ""
                    else:
                        pass

                elif option_dict[data]["type"] == "float":
                    if type(option_dict[data]["value"]) is not float:
                        if string(option_dict[data]["value"]).isfloat():
                            option_dict[data]["value"] = float(
                                option_dict[data]["value"]
                            )
                        else:
                            option_dict[data]["value"] = ""
                    else:
                        pass

                elif option_dict[data]["type"] == "bool":
                    if type(option_dict[data]["value"]) is not bool:
                        if option_dict[data]["value"].lower() in ["true", "false"]:
                            if option_dict[data]["value"].lower() == "true":
                                option_dict[data]["value"] = True
                            else:
                                option_dict[data]["value"] = False
                        else:
                            option_dict[data]["value"] = ""
                    else:
                        pass

                elif option_dict[data]["type"] == "str":
                    pass

                else:
                    _type = option_dict[data]["type"]
                    print(f"Error: Invalid type: {_type}")
                    del _type
                    sys.exit(1)

        return option_dict
