package something;

@ShellComponent
@ShellCommandGroup(value = "Commands group key/value")
public class CommandKeyValue {

    @ShellMethod(key = "foo", value = "foo description")
    public void foo() {
    }
}
