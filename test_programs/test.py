"""Test program for profiling.

With vprof: vprof -c cpmh test_programs/iterations_py2.py

This does now work with py3 as by default range behaves as xrange, and there's
no xrange.
"""
# ATM vprof doesn't work fine in py2, needs more debugging, not now.
import logging
import argparse


def log_list_of_nums(num):
  squares_list = []
  for n in range(num):
    logging.debug(n)
    squares_list.append(n * n)


def log_inside_iterator(num):
  for n in xrange(num):
    logging.debug(n)
    yield n * n




if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--num', help='Number to iterate to.', default=int(1e7), type=int)

  parser.add_argument(
      '--start', '-s', help='Starting number.', default=0, type=int)

  parser.add_argument(
      '--method', '-m', choices=('list', 'iter', 'both'), default='both')

  arguments = parser.parse_args()
  num = arguments.num

  if arguments.method == 'iter':
    for n in log_inside_iterator(num):
      pass
  if arguments.method == 'list':
    log_list_of_nums(num)
  log_list_of_nums(num)
  for n in log_inside_iterator(num):
    pass
