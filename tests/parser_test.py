#  Copyright 2021, Dylan Roger
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without
#  limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from markdown_spring_shell_documentation.parser import Parser


class ParserTestCase(unittest.TestCase):
    # install locally : python -m pip install .
    def test_no_classes(self):
        Verifier(self).verify(Parser("files/empty").parse())

    def test_complete(self):
        Verifier(self) \
            .withClass(Class("System Command")  # No group
                       .withMethod(Method("system-env", "Constant in another file")
                                   .withParameter(Parameter(["--simple-view"], "", "false", False)))
                       .withMethod(Method("no-key", "No key in ShellMethod"))
                       .withMethod(Method("no-description", ""))) \
            .withClass(Class("System Commands commands")  # Shell commands group
                       .withMethod(Method("no-shell-option", "description")
                                   .withParameter(Parameter(["--value"], "", "", True)))
                       .withMethod(Method("default-value", "description")
                                   .withParameter(Parameter(["--value"], "", "abc", False)))
                       .withMethod(Method("only-one-value", "description")
                                   .withParameter(Parameter(["-v"], "", "abc", False)))
                       .withMethod(Method("multiple-values", "description")
                                   .withParameter(Parameter(["-v", "--value"], "", "abc", False)))
                       .withMethod(Method("system-env", "")
                                   .withParameter(Parameter(["--value"], "system-env", "", True)))) \
            .withClass(Class("System Commands group")  # Shell component group
                       .withMethod(Method("system-env", "List system environment."))) \
            .withClass(Class("System Commands group")  # Ssh Shell component group
                       .withMethod(Method("system-env", "List system environment."))) \
            .verify(Parser("files/complete").parse())

    def test_file_path(self):
        Verifier(self) \
            .withClass(Class("System Command")  # No group
                       .withMethod(Method("COMMAND_SYSTEM_ENV", "Constant in another file")
                                   .withParameter(Parameter(["--simple-view"], "", "false", False)))
                       .withMethod(Method("no-key", "No key in ShellMethod"))
                       .withMethod(Method("no-description", ""))) \
            .verify(Parser("files/complete/no_group.java").parse())

    def test_kotlin(self):
        Verifier(self) \
            .withClass(Class("Commands")  # No group
                       .withMethod(Method("user-add", "")
                                   .withParameter(Parameter(["--name"], "The name of the user", "", True)))
                       .withMethod(Method("user-remove", "")
                                   .withParameter(Parameter(["--name"], "The name of the user", "", True)))
                       .withMethod(Method("user-update", "")
                                   .withParameter(Parameter(["--new-name"], "The new name of the user", "", True))
                                   .withParameter(Parameter(["--old-name"], "The old name of the user", "", True)))) \
            .verify(Parser("files/kotlin/generated.java").parse())


class Verifier:
    def __init__(self, validator):
        super().__init__()
        self.validator = validator
        self.classes = []

    def withClass(self, clazz):
        self.classes.append(clazz)
        return self

    def verify(self, classes):
        self.validator.assertEqual(len(self.classes), len(classes))
        for clazz in classes:
            try:
                matching_class = next(x for x in self.classes if x.group_name == clazz.group_name)
                self.validator.assertEqual(len(matching_class.methods), len(clazz.methods))
                for method in clazz.methods:
                    matching_method = next(x for x in matching_class.methods if x.name == method.name)
                    self.validator.assertEqual(matching_method.description, method.description)
                    self.validator.assertEqual(len(matching_method.parameters), len(method.parameters))
                    for parameter in method.parameters:
                        matching_parameter = next(x for x in matching_method.parameters if x.value == parameter.value)
                        self.validator.assertEqual(matching_parameter.help, parameter.help)
                        self.validator.assertEqual(matching_parameter.required, parameter.required)
                        self.validator.assertEqual(matching_parameter.default_value, parameter.default_value)
            except StopIteration:
                self.validator.fail("Failed in class : %s" % clazz.group_name)
        return True


class Class:
    def __init__(self, group_name):
        self.group_name = group_name
        self.methods = []

    def withMethod(self, method):
        self.methods.append(method)
        return self


class Method:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.parameters = []

    def withParameter(self, parameter):
        self.parameters.append(parameter)
        return self


class Parameter:
    def __init__(self, value, help, default_value, required):
        self.value = value
        self.help = help
        self.default_value = default_value
        self.required = required


if __name__ == '__main__':
    unittest.main()
