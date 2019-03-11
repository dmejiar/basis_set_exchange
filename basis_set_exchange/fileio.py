"""
Functions for reading and writing the standard JSON-based
basis set format
"""

import codecs
import json
import bz2
import os

from .sort import sort_basis_dict, sort_references_dict


def _read_plain_json(file_path, check_bse):
    """
    Reads a JSON file

    A simple wrapper around json.load that only takes the file name
    If the file does not exist, an exception is thrown.

    If the file does exist, but there is a problem with the JSON formatting,
    the filename is added to the exception information.

    If check_bse is True, this function also make sure the 'molssi_bse_schema' key
    exists in the file.

    Parameters
    ----------
    file_path : str
        Full path to the file to read
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError('JSON file \'{}\' does not exist, is not '
                                'readable, or is not a file'.format(file_path))

    try:
        if file_path.endswith('.bz2'):
            with bz2.open(file_path, 'rt') as f:
                js = json.load(f)
        else:
            with open(file_path, 'r') as f:
                js = json.load(f)

    except json.decoder.JSONDecodeError as ex:
        raise RuntimeError("File {} contains JSON errors".format(file_path)) from ex

    if check_bse is True:
        # Check for molssi_bse_schema key
        if 'molssi_bse_schema' not in js:
            raise RuntimeError('File {} does not appear to be a BSE JSON file'.format(file_path))

    return js


def _write_plain_json(file_path, js):
    """
    Write information to a JSON file

    This makes sure files are created with the proper encoding and consistent indenting

    Parameters
    ----------
    file_path : str
        Full path to the file to write to. It will be overwritten if it exists
    js : dict
        JSON information to write
    """

    # Disable ascii in the json - this prevents the json writer
    # from escaping everything

    if file_path.endswith('.bz2'):
        with bz2.open(file_path, 'wt') as f:
            json.dump(js, f, indent=2, ensure_ascii=False)
    else:
        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(js, f, indent=2, ensure_ascii=False)


def read_json_basis(file_path):
    """
    Reads generic basis set information from a JSON file

    After reading, the MolSSI BSE schema information is searched for and if not
    found, an exception is raised.

    Parameters
    ----------
    file_path : str
        Full path to the file to read
    """

    return _read_plain_json(file_path, True)


def read_schema(file_path):
    """
    Reads a JSON schema file

    Parameters
    ----------
    file_path : str
        Full path to the file to read
    """

    return _read_plain_json(file_path, False)


def read_references(file_path):
    """
    Reads a references JSON file

    Parameters
    ----------
    file_path : str
        Full path to the file to read
    """

    return _read_plain_json(file_path, True)


def read_metadata(file_path):
    """
    Reads a file containing the metadata for all the basis sets

    Parameters
    ----------
    file_path : str
        Full path to the file to read
    """

    return _read_plain_json(file_path, False)


def write_json_basis(file_path, bs):
    """
    Write basis set information to a JSON file

    Parameters
    ----------
    file_path : str
        Full path to the file to write to. It will be overwritten if it exists
    bs : dict
        Basis set information to write
    """

    _write_plain_json(file_path, sort_basis_dict(bs))


def write_references(file_path, refs):
    """
    Write reference information to a JSON file

    Parameters
    ----------
    file_path : str
        Full path to the file to write to. It will be overwritten if it exists
    refs : dict
        Reference information to write
    """

    _write_plain_json(file_path, sort_references_dict(refs))


def get_all_filelist(data_dir):
    """
    Returns a tuple containing the following (as lists)

    0. All metadata files
    1. All table basis files
    2. All element basis files
    3. All component basis files

    The paths to all the files are returned as paths relative to data_dir
    """

    all_meta = []
    all_table = []
    all_element = []
    all_component = []

    special = ['METADATA.json', 'REFERENCES.json']

    for root, dirs, files in os.walk(data_dir):
        for basename in files:
            if basename in special:
                continue

            fpath = os.path.join(root, basename)
            fpath = os.path.relpath(fpath, data_dir)

            if basename.endswith('.metadata.json'):
                all_meta.append(fpath)
            elif basename.endswith('.table.json'):
                all_table.append(fpath)
            elif basename.endswith('.element.json'):
                all_element.append(fpath)
            elif basename.endswith('.json'):
                all_component.append(fpath)

    return (all_meta, all_table, all_element, all_component)


def read_notes_file(file_path):
    """
    Returns the contents of a notes file.

    If the notes file does not exist, None is returned
    """

    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'r') as f:
        return f.read()
