# markdown-spring-shell-documentation
A markdown extension that creates a documentation from Java classes using Spring Shell or [ssh-shell-spring-boot](https://github.com/fonimus/ssh-shell-spring-boot).

## Installation

## Usage

### Mkdocs configuration

Update your ``mkdocs.yml`` to add this extension :

````yaml
markdown_extensions:
  - markdown_spring_shell_documentation.extension:
      base_path: './'    # (Optional) Default location from which to evaluate relative paths for the files to parse.
      encoding: 'utf-8'  # (Optional) Encoding of the files to parse.
````

### Markdown syntax

To include content generated from your ShellComponents, you can add the following line in your Markdown files :

[//]: # (TODO specify it is only the directory)

````
(!./path/to/the/directory1, ./path/to/the/directory2, ./path/to/the/directory3!)
````

## Examples

Given a shell component like this one :

````java
@ShellComponent(group = "My admin commands")
public class AdminCommands {

    @ShellMethod(key = "create-user", value = "Command to add a user.")
    public void create(
        @ShellOption(value = {"--name"}, defaultValue = "John Doe", help = "The name of the user.") String name) {
    
    }
}
````

you can include this in your documentation by using the specific include syntax:

````markdown
# Commands

(!./path/to/the/directory!)

...the rest of the documentation...
````

and this will output something like this :

````markdown
# Commands

## My admin commands

### create-user

Command to add a user.

| Name       | Required | Default value | Description
|------------|:--------:|:-------------:|---------
| -a, --age  | true     |               | The age of the user. Must be a positive integer
| --name     | false    | John Doe      | The name of the user.

...the rest of the documentation... 
````

and is rendered in HTML like in the next part :

### Commands

#### My admin commands

##### create-user

Command to add a user.

| Name       | Required | Default value | Description
|------------|:--------:|:-------------:|---------
| -a, --age  | true     |               | The age of the user. Must be a positive integer
| --name     | false    | John Doe      | The name of the user. 

...the rest of the documentation...

## Limitations

* Can only be used to parse Java code. If you want to parse Kotlin code, you can still reference the ``kapt`` output directory

* Cannot resolve constants with operations 

    ````java
    String FULL_NAME = FIRST_NAME + LAST_NAME;  // Won't work  
    String FULL_NAME = FIRST_NAME + "Doe";  // Won't work  
    String FULL_NAME = "John Doe";  // OK
    
    @ShellMethod(key = FULL_NAME)
    public void foo() {
    }  
    ````

* Cannot resolve constants from outside the working directory (ie: the directory passed in ``(!here!)``). In such cases, the constant is returned