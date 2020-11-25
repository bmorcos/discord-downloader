import datetime


# Helper functions to handle Nonetype args
def none_or_int(arg):
    if arg == "None":
        return None
    else:
        return int(arg)


def none_or_str(arg):
    if arg == "None":
        return None
    else:
        return str(arg)


def none_or_date(arg):
    if arg == "None":
        return None
    else:
        return datetime.datetime.strptime(arg, "%Y-%m-%d")


def none_or_list(arg):
    if arg == "None":
        return None
    else:
        arg_list = arg.split(",")
        # Check if single str or list
        if len(arg_list) > 1:
            return arg_list
        else:
            return arg
