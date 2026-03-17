from typing import Union


def key_value_list(d: Union[dict, list], key=None):

    if not d:
        return []

    if not isinstance(d, dict) and not isinstance(d, list):
        return []

    key_values = []

    if isinstance(d, list):

        for entry in d:
            if isinstance(entry, dict):
                key_values.extend(key_value_list(entry))
            else:
                key_values.append((key, entry))

    else:

        for k, v in d.items():

            if k is None or v is None:
                continue

            if not isinstance(v, dict) and type(v) != list:
                key_values.append((k, v))

            elif isinstance(v, list):
                key_values.extend(key_value_list(v, k))

            else:
                key_values.extend(key_value_list(v))

    return key_values


def all_keys(d: Union[dict, list]):

    if not d:
        return []

    if d is None or not isinstance(d, dict) and not isinstance(d, list):
        return []

    keys = []

    if isinstance(d, list):

        for entry in d:
            keys.extend(all_keys(entry))

    else:

        for k, v in d.items():
            keys.append(k)
            keys.extend(all_keys(v))

    return keys


def all_values(d: Union[dict, list]):

    if not d:
        return []

    if not isinstance(d, dict) and not isinstance(d, list):
        return [d]

    values = []

    if isinstance(d, list):

        for entry in d:
            values.extend(all_values(entry))

    else:

        for k, v in d.items():
            values.extend(all_values(v))

    return values