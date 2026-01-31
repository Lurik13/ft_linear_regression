from prompt_toolkit.completion import Completer, Completion  # type: ignore


def normalize(value):
    if isinstance(value, str):
        return value.lower()
    else:
        new_array = []
        for i in range(len(value)):
            new_array.append(value[i].lower())
        return new_array


class AccentInsensitiveCompleter(Completer):
    def __init__(self, names):
        self.names = names

    def get_completions(self, document, complete_event):
        normalized_input = normalize(document.text_before_cursor)
        for name in self.names:
            if normalize(name).startswith(normalized_input):
                yield Completion(
                    name,
                    start_position=-len(document.text_before_cursor)
                )
