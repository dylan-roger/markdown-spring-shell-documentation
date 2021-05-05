package something;

@SshShellComponent
public class SystemCommand {

    @ShellMethod(key = COMMAND_SYSTEM_ENV, value = "Constant in another file")
    public Object constantInAnotherFile(boolean simpleView) {
        return null;
    }

    @ShellMethod(value = "No key in ShellMethod")
    public Object noKey() {
        return null;
    }

    @ShellMethod(key = "no-description")
    public Object noDescription() {
        return null;
    }
}
