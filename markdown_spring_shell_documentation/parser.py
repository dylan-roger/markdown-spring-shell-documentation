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

#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without
#  limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#
import os
import re

import javalang

SSH_SHELL_COMPONENT = "SshShellComponent"
SHELL_COMPONENT = "ShellComponent"
SHELL_COMMAND_GROUP = "ShellCommandGroup"
SHELL_METHOD = "ShellMethod"
SHELL_OPTION = "ShellOption"


def find_annotation(node, annotation_names):
    if not isinstance(annotation_names, list):
        annotation_names = [annotation_names]
    for annotation_name in annotation_names:
        for annotation in node.annotations:
            if annotation.name == annotation_name:
                return annotation
    return


def camel_to_kebab(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', name).lower()


def trim_quotes(string):
    return string.strip("\"")


def resolve_constant(variable, constants):
    # TODO manage the case where multiple constants have the same name : use the package to differentiate them
    if isinstance(variable, javalang.tree.Literal):
        return trim_quotes(variable.value)
    elif isinstance(variable, javalang.tree.MemberReference):
        if variable.member in constants:
            return constants[variable.member]
        else:
            return variable.member
    else:
        return variable


class ParameterDetails:
    value = None
    help = ""
    default_value = None
    required = False

    def __init__(self, parameter, shell_option_annotation):
        # Parse the ShellOption first
        if shell_option_annotation is not None:
            for element in shell_option_annotation.element:
                if element.name == "value":
                    self.value = [trim_quotes(v.value) for v in element.value.values]
                elif element.name == "help":
                    self.help = element.value
                elif element.name == "defaultValue":
                    if isinstance(element.value, javalang.tree.MemberReference) and element.value.member == "NULL":
                        self.default_value = ""
                    else:
                        self.default_value = element.value
        # If there is no annotation, or some fields are missing
        if self.value is None:
            self.value = ["--" + camel_to_kebab(parameter.name)]
        if parameter.type.name == "boolean":
            self.required = False
            if self.default_value is None:
                self.default_value = "false"
        elif self.default_value is None:
            self.default_value = ""
            self.required = True

    def resolve_constants(self, constants):
        self.value = resolve_constant(self.value, constants)
        self.help = resolve_constant(self.help, constants)
        self.default_value = resolve_constant(self.default_value, constants)


class MethodDetails:
    name = None
    description = ""

    def __init__(self, method, shell_method_annotation):
        # Find the name of the shell method and its description
        for element in shell_method_annotation.element:
            if element.name == "key":
                self.name = element.value
            if element.name == "value":
                self.description = element.value

        if self.name is None:
            self.name = camel_to_kebab(method.name)

        self.parameters = []
        # Find the parameters
        for parameter in method.parameters:
            if len(parameter.annotations) != 0:
                shell_option_annotation = find_annotation(parameter, SHELL_OPTION)
                self.parameters.append(ParameterDetails(parameter, shell_option_annotation))
            else:
                self.parameters.append(ParameterDetails(parameter, None))

    def resolve_constants(self, constants):
        self.name = resolve_constant(self.name, constants)
        self.description = resolve_constant(self.description, constants)
        for parameter in self.parameters:
            parameter.resolve_constants(constants)


class ClassDetails:
    def __init__(self, group_name, methods):
        self.group_name = group_name
        self.methods = methods

    def resolve_constants(self, constants):
        self.group_name = resolve_constant(self.group_name, constants)
        for method in self.methods:
            method.resolve_constants(constants)


class Parser:
    supported_constants_type = ["String"]

    def __init__(self, path):
        self.path = path.strip()

    def __add_constants(self, constants, clazz):
        for field in clazz.fields:
            if field.type.name in self.supported_constants_type:
                name = field.declarators[0].name
                value = trim_quotes(field.declarators[0].initializer.value)
                constants[name] = value

    @staticmethod
    def __find_group_name(clazz):
        shell_annotation = find_annotation(clazz, [SSH_SHELL_COMPONENT, SHELL_COMPONENT])
        if shell_annotation.element is not None:
            for element in shell_annotation.element:
                if element.name == "group":
                    return element.value
        command_group_annotation = find_annotation(clazz, SHELL_COMMAND_GROUP)
        if command_group_annotation is not None:
            return command_group_annotation.element
        return re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", clazz.name)

    def __internal_parse(self, file_path, classes, constants):
        with open(file_path) as f:
            tree = javalang.parse.parse("".join(f.readlines()))
            for _, clazz in tree.filter(javalang.tree.ClassDeclaration):
                self.__add_constants(constants, clazz)
                if find_annotation(clazz, [SSH_SHELL_COMPONENT, SHELL_COMPONENT]) is not None:
                    group_name = self.__find_group_name(clazz)
                    # Find the shell methods in this component
                    methods = []
                    for method in clazz.methods:
                        shell_method_annotation = find_annotation(method, SHELL_METHOD)
                        if shell_method_annotation is not None:
                            methods.append(MethodDetails(method, shell_method_annotation))
                    if len(methods) != 0:
                        classes.append(ClassDetails(group_name, methods))

    def parse(self):
        classes = []
        # Keep the constants found during the parsing to replace them with their actual value at the end
        constants = {}
        if os.path.isfile(self.path) and self.path.endswith(".java"):
            self.__internal_parse(self.path, classes, constants)
        else:
            for file in os.listdir(self.path):
                if not file.endswith(".java"):
                    continue
                self.__internal_parse(os.path.join(self.path, file), classes, constants)
        for clazz in classes:
            clazz.resolve_constants(constants)
        return classes
