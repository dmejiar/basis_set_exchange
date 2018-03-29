"""
Tests for BSE metadata
"""

import os
import bse
import json
from bse import curate

data_dir = bse.default_data_dir

def test_get_metadata():
    bse.get_metadata()


def test_metadata_uptodate():
    old_metadata = os.path.join(data_dir, 'METADATA.json')
    new_metadata = os.path.join(data_dir, 'METADATA.json.new')
    curate.create_metadata_file(new_metadata, data_dir)

    with open(old_metadata, 'r') as f:
        old_data = json.load(f)
    with open(new_metadata, 'r') as f:
        new_data = json.load(f)

    os.remove(new_metadata)

    if old_data != new_data:
        raise RuntimeError("Metadata does not appear to be up to date")