import json
from pathlib import Path

import numpy as np
import pytest
from imageio import imread

from pymartini import Martini, decode_ele

TEST_CASES = []
TEST_PNG_FILES = [('fuji', 'mapbox'), ('terrarium', 'terrarium')]
for png_fname, encoding in TEST_PNG_FILES:
    for max_error in [5, 20, 50, 100, 500]:
        TEST_CASES.append([png_fname, max_error, encoding])

def this_dir():
    try:
        return Path(__file__).resolve().parents[0]
    except NameError:
        return Path('.').resolve()


@pytest.mark.parametrize("png_fname,encoding", TEST_PNG_FILES)
def test_terrain(png_fname, encoding):
    """Test output from decode_ele against JS output
    """
    # Generate terrain output in Python
    path = this_dir() / f'data/{png_fname}.png'
    png = imread(path)
    terrain = decode_ele(png, encoding=encoding)

    # Load JS terrain output
    path = this_dir() / f'data/{png_fname}_terrain'
    with open(path, 'rb') as f:
        exp_terrain = np.frombuffer(f.read(), dtype=np.float32)

    assert np.array_equal(terrain, exp_terrain), 'terrain not matching expected'


@pytest.mark.parametrize("png_fname,encoding", TEST_PNG_FILES)
def test_errors(png_fname, encoding):
    """Test errors output from martini.create_tile(terrain)
    """
    # Generate errors output in Python
    path = this_dir() / f'data/{png_fname}.png'
    png = imread(path)
    terrain = decode_ele(png, encoding=encoding)
    martini = Martini(png.shape[0] + 1)
    tile = martini.create_tile(terrain)
    errors = np.asarray(tile.errors_view, dtype=np.float32)

    # Load JS errors output
    path = this_dir() / f'data/{png_fname}_errors'
    with open(path, 'rb') as f:
        exp_errors = np.frombuffer(f.read(), dtype=np.float32)

    assert np.array_equal(errors, exp_errors), 'errors not matching expected'
