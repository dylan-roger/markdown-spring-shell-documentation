package something;

@ShellComponent
@ShellCommandGroup("System Commands commands")
public class SystemCommand {

    public static final String GROUP = "System Commands group";

    private static final String COMMAND_SYSTEM_ENV = "system-env";

    @ShellMethod(key = "no-shell-option", value = "description")
    public void noShellOption(String value) {
    }

    @ShellMethod(key = "default-value", value = "description")
    public void defaultValue(@ShellOption(defaultValue = "abc") String value) {
    }

    // Only one value in ShellOption annotation
    @ShellMethod(key = "only-one-value", value = "description")
    public void onlyOneValue(@ShellOption(value = {"-v"}, defaultValue = "abc") String value) {
    }

    // Multiple values in ShellOption annotation
    @ShellMethod(key = "multiple-values", value = "description")
    public void multipleValues(@ShellOption(value = {"-v", "--value"}, defaultValue = "abc") String value) {
    }

    @ShellMethod(key = COMMAND_SYSTEM_ENV)
    public void usingConstant(@ShellOption(help = COMMAND_SYSTEM_ENV) String value) {
    }
}
