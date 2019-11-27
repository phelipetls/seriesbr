def expect_type(*args):
    for arg in args:
        if isinstance(arg, dict):
            return arg.values(), arg.keys()
    return args, args
