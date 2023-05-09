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

    For anaphors in programming see https://en.wikipedia.org/wiki/Anaphoric_macro.
    """

    def _decor(f):
        
        @functools.wraps(f)
        def _wrapper(**kwargs):
        
            _f = types.FunctionType(
                code=f.__code__,
                globals=anaphors
            )

            return _f(**kwargs)
        return _wrapper
    return _decor
