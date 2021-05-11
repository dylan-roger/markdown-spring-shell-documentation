package com.droger.browser.s3;

import java.lang.System;

@kotlin.Metadata(mv = {1, 4, 2}, bv = {1, 0, 3}, k = 1, d1 = {"\u0000\u001a\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0005\b\u0017\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0012\u0010\u0003\u001a\u00020\u00042\b\b\u0001\u0010\u0005\u001a\u00020\u0006H\u0017J\u0012\u0010\u0007\u001a\u00020\u00042\b\b\u0001\u0010\u0005\u001a\u00020\u0006H\u0017J\u001c\u0010\b\u001a\u00020\u00042\b\b\u0001\u0010\t\u001a\u00020\u00062\b\b\u0001\u0010\n\u001a\u00020\u0006H\u0017\u00a8\u0006\u000b"}, d2 = {"Lcom/droger/browser/s3/Commands;", "", "()V", "add", "", "name", "", "remove", "update", "oldName", "newName", "s3"})
@com.github.fonimus.ssh.shell.commands.SshShellComponent()
public class Commands {
    
    @org.springframework.shell.standard.ShellMethod(key = {"user-add"})
    public void add(@org.jetbrains.annotations.NotNull()
    @org.springframework.shell.standard.ShellOption(help = "The name of the user")
    java.lang.String name) {
    }
    
    @org.springframework.shell.standard.ShellMethod(key = {"user-remove"})
    public void remove(@org.jetbrains.annotations.NotNull()
    @org.springframework.shell.standard.ShellOption(help = "The name of the user")
    java.lang.String name) {
    }
    
    @org.springframework.shell.standard.ShellMethod(key = {"user-update"})
    public void update(@org.jetbrains.annotations.NotNull()
    @org.springframework.shell.standard.ShellOption(help = "The old name of the user")
    java.lang.String oldName, @org.jetbrains.annotations.NotNull()
    @org.springframework.shell.standard.ShellOption(help = "The new name of the user")
    java.lang.String newName) {
    }
    
    public Commands() {
        super();
    }
}