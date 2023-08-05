def copy_docstring_of(original):
    def wrapper(target):
        if type(target.__doc__) == str:
            if "NOTE:" not in original.__doc__:
                target.__doc__ = original.__doc__ + "\n\n NOTE: \n" + target.__doc__
            else:
                target.__doc__ = original.__doc__ + "\n" + target.__doc__
        elif type(original.__doc__) == str:
            if "NOTE:" not in original.__doc__:
                target.__doc__ = original.__doc__ + "\n\n NOTE: \n N.A."
            else:
                target.__doc__ = original.__doc__
        else:
            target.__doc__ = original.__doc__
        return target

    return wrapper
