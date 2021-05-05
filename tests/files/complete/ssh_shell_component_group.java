package something;

@SshShellComponent(group = GROUP)
public class SystemCommand {

    private static final String COMMAND_SYSTEM_ENV = "system-env";

    @ShellMethod(key = COMMAND_SYSTEM_ENV, value = "List system environment.")
    public Object jvmEnv() {
        return null;
    }
}
