# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>

# contains syntax illegal before PEP525 "Asynchronous Generators"

from makefun import wraps
from .fixture_core1_unions import is_used_request, NOT_USED


def _ignore_unused_asyncgen_pep525(fixture_func, new_sig, func_needs_request):
    @wraps(fixture_func, new_sig=new_sig)
    async def wrapped_fixture_func(*args, **kwargs):
        request = kwargs['request'] if func_needs_request else kwargs.pop('request')
        if is_used_request(request):
            async for res in fixture_func(*args, **kwargs):
                yield res
        else:
            yield NOT_USED

    return wrapped_fixture_func

def _decorate_fixture_plus_asyncgen_pep525(fixture_func, new_sig, map_arguments):
    @wraps(fixture_func, new_sig=new_sig)
    async def wrapped_fixture_func(*_args, **_kwargs):
        if not is_used_request(_kwargs['request']):
            yield NOT_USED
        else:
            _args, _kwargs = map_arguments(*_args, **_kwargs)
            async for res in fixture_func(*_args, **_kwargs):
                yield res

    return wrapped_fixture_func
