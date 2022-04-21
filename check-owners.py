#!/usr/bin/env python3
# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run lint checks on OWNERS files.

If no files are specified, all files will be checked.
"""

import logging
from pathlib import Path
import sys
from typing import List, Optional

DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(DIR.parent))

# pylint: disable=wrong-import-position
from chromite.lib import commandline
from chromite.lint.linters import owners
# pylint: enable=wrong-import-position


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


def check_data(path: Path, data: str) -> bool:
  """Validate the raw file."""
  ret = owners.lint_data(path, data)

  lines = data.splitlines()

  if lines and not lines[0].startswith('#'):
    ret = False
    logging.error('%s: file must begin with a comment explaining scope', path)

  for i, line in enumerate(lines):
    lstrip = line.lstrip()
    if lstrip.startswith('set '):
      ret = False
      logging.error('%s:%i: "set" directives not allowed: "%s"', path, i, line)

    # Allow per-file in plain "OWNERS" files since they should not be included
    # by external repos.
    if path.name != 'OWNERS' and lstrip.startswith('per-file '):
      ret = False
      logging.error('%s:%i: "per-file" not allowed: "%s"', path, i, line)

    if lstrip == '*':
      ret = False
      logging.error('%s:%i: "*" not allowed', path, i)

    if (lstrip and not lstrip.startswith('#') and
        not lstrip.startswith('include ') and
        not lstrip.startswith('per-file ')):
      if '@' not in line:
        ret = False
        logging.error('%s:%i: usernames-only are not allowed; full e-mail '
                      'addresses are required: "%s"', path, i, line)
      else:
        if line.split('@')[-1] not in ('chromium.org', 'google.com'):
          ret = False
          logging.error('%s:%i: only @chromium.org & @google.com are allowed: '
                        '"%s"', path, i, line)

  return ret


def check_path(path: Path) -> bool:
  """Validate the OWNERS file."""
  logging.debug('Checking %s', path)
  data = path.read_text()

  return check_data(path, data)


def main(argv: Optional[List[str]] = None) -> Optional[int]:
  """Main function."""
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument('files', nargs='*', type=Path)
  opts = parser.parse_args(argv)

  if not opts.files:
    opts.files = DIR.glob('**/OWNERS*')

  ret = 0
  for path in opts.files:
    if path.name.startswith('OWNERS'):
      if not check_path(path):
        ret = 1
  return ret


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
