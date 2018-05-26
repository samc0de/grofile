"""Test program for profiling.

With vprof: vprof -c cpmh test_programs/iterations_py2.py

This does now work with py3 as by default range behaves as xrange, and there's
no xrange.
Also keep in mind that functions decorated with such decorators will not return
what they seem to, they will be replaced with wrappers, so do not call these
functions. Maybe move the functionality to some other function, and call that
in another function which is decorated, as a solution.
"""
# ATM vprof doesn't work fine in py2, needs more debugging, not now.
import logging
import argparse
import os

# Works only from grofile dir.
from context import grofiler


@grofiler.grofile()
def list_in_mem(num):
  squares_list = []
  for n in list(range(num)):
    squares_list.append(n * n)


def iterator(num):
  for n in range(num):
    yield n * n


@grofiler.grofile()
def iterator_consumer(num):
  for n in iterator(num):
    pass

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
    for n in iterator(num):
      pass
  if arguments.method == 'list':
    list_in_mem(num)

  list_in_mem(num)
  iterator_consumer(num)
