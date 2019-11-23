def parse_args(*args):
    if len(args) > 1:
        err_msg = "Code series must be of the same type"
        assert all([isinstance(arg, str) for arg in args]), err_msg
        assert all([isinstance(arg, int) for arg in args]), err_msg
    elif isinstance(args[0], dict):
        return args[0].values(), args[0].keys()
    return args, args
