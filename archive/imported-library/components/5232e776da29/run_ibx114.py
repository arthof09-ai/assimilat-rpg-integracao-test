"""One-command portable runner. Run `python run_ibx114.py` from any directory.

Removes the Coordinator's observed manual PYTHONPATH requirement without
changing baseline modules, tests or algorithm.
"""
from pathlib import Path
import sys
import unittest

BASE = Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
sys.path.insert(0,str(BASE/'baseline'/'code'))

if __name__=='__main__':
    tests=unittest.TestLoader().discover(str(BASE),pattern='test*.py',top_level_dir=str(BASE))
    result=unittest.TextTestRunner(verbosity=1).run(tests)
    print(f'IBX114_PORTABLE_TESTS_RUN={result.testsRun}; ERRORS={len(result.errors)}; FAILURES={len(result.failures)}')
    if not result.wasSuccessful(): sys.exit(1)
