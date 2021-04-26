import unittest

from markdown_spring_shell_documentation.parser import Parser


class ParserTestCase(unittest.TestCase):
    # install locally : python -m pip install .
    def test_no_classes(self):
        Verifier(self).verify(Parser("files/empty").parse())

    def test_complete(self):
        """
        TODO constants with the same name but different value
        TODO ShellComponent et SshShellComponent
        TODO unknown constant : if not in the constants, return the constant name
        Parameter
        * pas de shell option string
        * default value
        * shell option mais pas de value
        * une seule value ex: ["--value"]
        * pluieurs values ex: ["-v", "--value"]
        * constante dans un autre fichier
        """
        Verifier(self) \
            .withClass(Class("System Command")  # No group
                       .withMethod(Method("system-env", "Constant in another file")
                                   .withParameter(Parameter(["--simple-view"], "", "false", False)))
                       .withMethod(Method("no-key", "No key in ShellMethod"))
                       .withMethod(Method("no-description", ""))) \
            .withClass(Class("System Commands commands")  # Shell commands group
                       .withMethod(Method("key", "List system environment."))) \
            .withClass(Class("System Commands group")  # Shell component group
                       .withMethod(Method("system-env", "List system environment."))) \
            .verify(Parser("files/complete").parse())


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
