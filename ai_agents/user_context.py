def collect_user_context():

    context = {}

    context["target_sound"] = input("Target sound style: ")

    context["daw"] = input("DAW used: ")

    plugins = input("Available plugins (comma separated): ")
    context["plugins"] = plugins.split(",")

    instruments = input("Instruments used: ")
    context["instruments"] = instruments.split(",")

    return context