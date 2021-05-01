package something;

@ShellComponent
@ShellCommandGroup("User commands")
public class UserCommands {

    @ShellMethod(value = "Create a user and returns its API key.")
    public Object createUser(
        @ShellOption(value = {"-n", "--name"}, help = "The name of the user to add.") String name,
        @ShellOption(value = {"-d", "--duration"}, help = "The number of days before the API key expires.", defaultValue = "365") int duration) {

        return null;
    }

    @ShellMethod(value = "Delete a user from the system knowing its API key.")
    public Object deleteUser(@ShellOption(value = {"--api-key"}, help = "The API key of the user to delete.") String apiKey) {
        return null;
    }

    @ShellMethod(key = "renew-user", value = "Add time to live to the API key of a specific user.")
    public Object renewUser(
        @ShellOption(value = {"--api-key"}, help = "The API key of the user to renew.") String apiKey,
        @ShellOption(value = {"-d", "--duration"}, help = "The number of days to live to add to this API key.", defaultValue = "365") int duration) {
        return null;
    }
}
