import argparse

__author__ = 'aabulawi'


class PNCFormatter(argparse.ArgumentDefaultsHelpFormatter,
                   argparse.RawDescriptionHelpFormatter):
    def _expand_help(self, action):
        params = dict(vars(action), prog=self._prog)
        for name in list(params):
            if params[name] is argparse.SUPPRESS:
                del params[name]
        for name in list(params):
            if hasattr(params[name], '__name__'):
                params[name] = params[name].__name__
        if params.get('choices') is not None:
            choices_str = ', '.join([str(c) for c in params['choices']])
            params['choices'] = choices_str

        if 'default' in params:
            if params['default'] is None:
                params['default'] = 'null'
            else:
                params['default'] = repr(params['default'])

        return self._get_help_string(action) % params
