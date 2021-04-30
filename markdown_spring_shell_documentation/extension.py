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
import traceback

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from markdown_spring_shell_documentation.parser import Parser

TITLE_PATTERN = re.compile(r"^(#+) ")
SHELL_SYNTAX = re.compile(r"\(!\s*(.+?)\s*!\)")


class MarkdownShell(Extension):

    def __init__(self, configs=None, **kwargs):
        super(MarkdownShell, self).__init__(**kwargs)
        if configs is None:
            configs = {}
        self.config = {
            'base_path': ['.', 'Default location from which to evaluate relative paths for the files to parse.'],
            'encoding': ['utf-8', 'Encoding of the files to parse.']
        }
        for key, value in configs.items():
            self.setConfig(key, value)
        print("Using ssh-shell-documentation with arguments config=%s" % self.getConfigs())

    def extendMarkdown(self, md):
        md.preprocessors.add('shell', ShellPreprocessor(md, self.getConfigs()), '_begin')


class ShellPreprocessor(Preprocessor):
    """Creates markdown documentation from java classes using ssh-shell-spring-boot"""

    def __init__(self, md, config):
        super(ShellPreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        new_lines = []
        try:
            for line in lines:
                m = SHELL_SYNTAX.search(line)
                if m:
                    level = self.__find_current_level(reversed(new_lines))
                    new_lines.extend(self.__process(level, m.group(1)))
                else:
                    new_lines.append(line)
        except Exception as e:
            print("Failed to create the documentation for ssh component. Error : %s" % e)
            traceback.print_exc()
            return lines
        return new_lines

    @staticmethod
    def __find_current_level(lines):
        for line in lines:
            m = TITLE_PATTERN.search(line)
            if m:
                return len(m.group(1))
        return 0

    @staticmethod
    def __table_row(name, required, default_value, description):
        return "| %s | %s | %s | %s" % (name, required, default_value, description)

    @staticmethod
    def __list_to_string(value_list):
        return ", ".join(value_list)

    def __process(self, current_level, directory):
        directory_path = os.path.expanduser(directory)
        if not os.path.isabs(directory_path):
            directory_path = os.path.normpath(os.path.join(self.base_path, directory_path))

        lines_to_add = []
        for clazz in Parser(directory_path).parse():
            lines_to_add.append("#" * (current_level + 1) + " " + clazz.group_name)
            for method in clazz.methods:
                lines_to_add.append("#" * (current_level + 2) + " " + method.name)
                lines_to_add.append(method.description)
                lines_to_add.append("")
                if len(method.parameters) != 0:
                    lines_to_add.append(self.__table_row("Name", "Required", "Default Value", "Description"))
                    lines_to_add.append(self.__table_row("---", ":---:", ":---:", "---"))
                    for parameter in sorted(method.parameters, key=lambda x: not x.required):
                        # TODO make row prettier
                        lines_to_add.append(self.__table_row(
                            self.__list_to_string(parameter.value),
                            str(parameter.required).lower(),
                            parameter.default_value,
                            parameter.help
                        ))
                    lines_to_add.append("")
        return lines_to_add


def makeExtension(**kwargs):
    return MarkdownShell(kwargs)
