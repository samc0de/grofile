import logging
import argparse
import os
import sys
import psutil
import json
from ipdb import set_trace

import vprof
from vprof.__main__ import __version__ as vprof_version
from vprof import runner

# Take process RSS in order to compute profiler memory overhead.
try:
    import __builtin__ as builtins
except ImportError:  # __builtin__ was renamed to builtins in Python 3.
    import builtins
builtins.initial_rss_size = psutil.Process(os.getpid()).memory_info().rss
#-------------

# How about functools.wraps?
# Will appending file add up stats of diff fuctions? Can this work in order to
# keep stats from multiple funcs in a single file? Don't think so, it's json,
# so something like 'func': {
# 1: ...,
# 2: ...,
# } and
# 'func': {3:...}
# should add 1, 2, 3 in the final json. File append won't do this. probably
# json addition? if it's not there, then implememt yourself?

CONFIG = 'cmph'
MODE = 'w'

root_logger = logging.getLogger()
# root_logger.setLevel(int(os.environ.get('LOGLEVEL')) or 2)

def _profile(func, config, *arguments, **kwargs):
  context_tuple = (func, arguments, kwargs)
  logging.info('Now running the actual function....')
  try:
    stats = runner.run_profilers(context_tuple, config, verbose=True)
  except runner.AmbiguousConfigurationError:
    logging.error('Profiler configuration %s is ambiguous. Please, remove'
        'duplicates.' % config)
    sys.exit(_ERR_CODES['ambiguous_configuration'])
  except runner.BadOptionError as exc:
    logging.error(exc)
    sys.exit(_ERR_CODES['bad_option'])
  return stats


def grofile(out_file_prefix='profiling_report_for_func_', config='', mode=''):
  """A decorator for profiling (functions to start with)."""
  if os.environ.get('DEBUG'):
    set_trace()
  logging.debug('Wrapping the actual function with a profiling wrapper...')
  config = config or os.environ.get('PROFILE_CONFIG', CONFIG)
  logging.info('Config for profiling: %s', config)
  mode = mode or os.environ.get('MODE', MODE)
  # Provide a way to also show interactive graphs? Or vprof command is enough
  # for that? Maybe a very later addition.
  def deco(func):
    if os.environ.get('DEBUG'):
      set_trace()

    out_file = os.environ.get(
        'PROFILE_REPORT_FILE', out_file_prefix + func.__name__)

    def wrapped(*arguments, **kwargs):
      if os.environ.get('DEBUG'):
        set_trace()

      logging.info('Writing profiling info to: %s', out_file)
      stats = _profile(func, config, *arguments, **kwargs)
      stats['version'] = vprof_version
      # result = stats.pop('result')

      logging.info('Completed executation, writing profiling info to file...')
      with open(out_file, mode) as report:
        report.write(json.dumps(stats, indent=2))

      # Return actual return value of the original function.
      # return result
    return wrapped
  return deco
