import hashlib
import inspect
import functools
import types

def anaphoric(**anaphors):
    """Decorator for making bindings defined in **anaphors available in a decorated function.
    
    Example:
    
    @anaphoric(x=1, y=2, z=3)
    def foo():
        return x, y, z

    foo() # -> (1, 2, 3)

    For anaphoric references see https://en.wikipedia.org/wiki/Anaphoric_macro.
    """
    def _decor(f):

        @functools.wraps(f)
        def _wrapper(*args, **kwargs):

            _f = types.FunctionType(
                code=f.__code__,
                # merge anaphors and f's global name
                globals={**anaphors, **f.__globals__}
            )

            return _f(*args, **kwargs)
        return _wrapper
    return _decor


def genhash(string: str) -> str:
    """Hash generator for language encoding.
    """
    # _hash = hashlib.md5(string.encode("UTF-8"))
    _hash = hashlib.sha1(string.encode("UTF-8"))
    return _hash.hexdigest()[:8]
