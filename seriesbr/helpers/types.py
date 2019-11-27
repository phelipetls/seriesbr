def expect_type(*args):
    if len(args) > 1:
        err_msg = "Codes must be str or int and of the same type."
        str_cond = check_type(args, str)
        int_cond = check_type(args, int)
        assert str_cond or int_cond, err_msg
    elif isinstance(args[0], dict):
        return args[0].values(), args[0].keys()
    return args, args


def check_type(args, arg_type):
    return all([isinstance(arg, arg_type) for arg in args])
