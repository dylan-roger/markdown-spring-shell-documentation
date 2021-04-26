import os
import re

import javalang


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


def trim_slashes(string):
    return string.strip("\"")


def resolve_constant(variable, constants):
    # TODO manage the case where multiple constants have the same name : use the package to differentiate them
    if isinstance(variable, javalang.tree.Literal):
        return trim_slashes(variable.value)
    elif isinstance(variable, javalang.tree.MemberReference):
        # TODO if not in the constants, return the constant name
        return constants[variable.member]
    else:
        return variable


class ParameterDetails:
    value = None
    help = ""
    default_value = None
    required = False

    def __init__(self, parameter, shell_option_annotation):
        # Parse the annotation first
        if shell_option_annotation is not None:
            for element in shell_option_annotation.element:
                if element.name == "value":
                    self.value = [trim_slashes(v.value) for v in element.value.values]
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
                shell_option_annotation = find_annotation(parameter, "ShellOption")
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
    supported_constants = ["String", "int", "float", "long", "boolean"]

    def __init__(self, path):
        self.path = path

    def __add_constants(self, constants, clazz):
        for field in clazz.fields:
            if field.type.name in self.supported_constants:
                name = field.declarators[0].name
                value = trim_slashes(field.declarators[0].initializer.value)
                constants[name] = value

    @staticmethod
    def __find_group_name(clazz):
        shell_annotation = find_annotation(clazz, ["SshShellComponent", "ShellComponent"])
        if shell_annotation.element is not None:
            for element in shell_annotation.element:
                if element.name == "group":
                    return element.value
        command_group_annotation = find_annotation(clazz, "ShellCommandGroup")
        if command_group_annotation is not None:
            return command_group_annotation.element
        return re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", clazz.name)

    def parse(self):
        classes = []
        # Keep the constants found to replace them with their actual value
        constants = {}
        # TODO list recursively
        for file in os.listdir(self.path):
            if not file.endswith(".java"):
                continue
            with open(os.path.join(self.path, file)) as f:
                tree = javalang.parse.parse("".join(f.readlines()))
                for _, clazz in tree.filter(javalang.tree.ClassDeclaration):
                    self.__add_constants(constants, clazz)
                    if find_annotation(clazz, ["SshShellComponent", "ShellComponent"]) is not None:
                        group_name = self.__find_group_name(clazz)
                        # Find the shell methods in this component
                        methods = []
                        for method in clazz.methods:
                            shell_method_annotation = find_annotation(method, "ShellMethod")
                            if shell_method_annotation is not None:
                                methods.append(MethodDetails(method, shell_method_annotation))
                        classes.append(ClassDetails(group_name, methods))
        for clazz in classes:
            clazz.resolve_constants(constants)
        return classes
