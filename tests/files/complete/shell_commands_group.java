package something;

@ShellComponent
@ShellCommandGroup("System Commands commands")
public class SystemCommand {

    public static final String GROUP = "System Commands group";

    private static final String COMMAND_SYSTEM_ENV = "system-env";

    @ShellMethod(key = "key", value = "List system environment.")
    public Object jvmEnv() {
        return null;
    }
}
