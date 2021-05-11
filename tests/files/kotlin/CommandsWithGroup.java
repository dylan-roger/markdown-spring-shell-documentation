package com.droger.browser.s3;

import java.lang.System;

@kotlin.Metadata(mv = {1, 4, 2}, bv = {1, 0, 3}, k = 1, d1 = {"\u0000\u001a\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0003\b\u0017\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J&\u0010\u0003\u001a\u00020\u00042\b\b\u0001\u0010\u0005\u001a\u00020\u00062\b\b\u0001\u0010\u0007\u001a\u00020\u00062\b\b\u0001\u0010\b\u001a\u00020\u0006H\u0017\u00a8\u0006\t"}, d2 = {"Lcom/droger/browser/s3/CommandsWithGroup;", "", "()V", "add", "", "name", "", "value", "otherValue", "s3"})
@org.springframework.shell.standard.ShellCommandGroup(value = "Group")
@com.github.fonimus.ssh.shell.commands.SshShellComponent()
public class CommandsWithGroup {

    @org.springframework.shell.standard.ShellMethod(key = {"user-add"})
    public void add(@org.jetbrains.annotations.NotNull()
    @org.springframework.shell.standard.ShellOption(help = "The name of the user")
    java.lang.String name, @org.jetbrains.annotations.NotNull()
    @org.springframework.shell.standard.ShellOption(defaultValue = "__NULL__")
    java.lang.String value, @org.jetbrains.annotations.NotNull()
    @org.springframework.shell.standard.ShellOption(defaultValue = "__NULL__")
    java.lang.String otherValue) {
    }
    
    public CommandsWithGroup() {
        super();
    }
}