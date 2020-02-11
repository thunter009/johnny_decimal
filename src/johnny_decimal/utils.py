from dataclasses import field

def default_field(obj: object, **kwargs):
    """
    returns field object that can handle default factory functions properly
    """
    return field(default_factory=lambda: obj, **kwargs)