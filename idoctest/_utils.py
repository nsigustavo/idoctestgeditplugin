
from StringIO import StringIO
from contextlib import contextmanager
import sys
@contextmanager
def stdout_redirected(new_stdout):
	  save_stdout = sys.stdout
	  sys.stdout = new_stdout
	  try:
	      yield None
	  finally:
	      sys.stdout = save_stdout
