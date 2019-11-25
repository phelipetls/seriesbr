def check_cods(*args):
    if len(args) > 1:
        err_msg = "Codes must be str or int and of the same type."
        str_cond = check_types(args, str)
        int_cond = check_types(args, int)
        assert str_cond or int_cond, err_msg
    elif isinstance(args[0], dict):
        return args[0].values(), args[0].keys()
    return args, args


def check_types(args, arg_type):
    return all([isinstance(arg, arg_type) for arg in args])
