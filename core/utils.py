import csv
import json
import logging
import os
import re
import uuid
from contextlib import contextmanager
from zipfile import ZipFile

import ijson
from django.conf import settings
from django.utils.translation import activate, get_language
from spoonbill.common import ROOT_TABLES

from core.column_headings import headings

logger = logging.getLogger(__name__)


def instance_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return "{0}/{1}.json".format(instance.id, uuid.uuid4().hex)


def export_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    selection = instance.dataselection_set.all()[0]
    ds_set = selection.url_set.all() or selection.upload_set.all()
    ds = ds_set[0]
    return "{0}/{1}".format(ds.id, filename.split("/")[-1])


def retrieve_available_tables(analyzed_data):
    tables = analyzed_data.get("tables", {})
    available_tables = []
    for key in ROOT_TABLES:
        if key not in tables:
            continue
        root_table = tables.get(key)
        if root_table.get("total_rows", 0) == 0:
            continue
        arrays_count = len([v for v in root_table.get("arrays", {}).values() if v > 0])
        available_table = {
            "name": root_table.get("name"),
            "rows": root_table.get("total_rows"),
            "arrays": {"count": arrays_count},
            "available_data": {
                "columns": {
                    "additional": list(root_table.get("additional_columns", {}).keys()),
                    "total": len(root_table.get("columns", {}).keys()),
                }
            },
        }
        available_cols = 0
        for col in root_table.get("columns", {}).values():
            if col.get("hits", 0) > 0:
                available_cols += 1
        available_table["available_data"]["columns"]["available"] = available_cols
        available_tables.append(available_table)
    return available_tables


def store_preview_csv(columns_key, rows_key, table_data, preview_path):
    headers = set()
    for row in table_data[rows_key]:
        headers |= set(row.keys())
    with open(preview_path, "w", newline="\n") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(table_data[rows_key])


def transform_to_r(value):
    return value.replace(" ", "_").lower()


def get_column_headings(datasource, tables, table):
    heading_formatters = {
        "en_r_friendly": transform_to_r,
        "es_r_friendly": transform_to_r,
        "en_user_friendly": lambda x: x,
        "es_user_friendly": lambda x: x,
    }
    column_headings = {}
    if datasource.headings_type == "ocds":
        return column_headings
    columns = tables[table.name]["columns"].keys() if table.split else tables[table.name]["combined_columns"].keys()
    for col in columns:
        non_index_based = re.sub(r"\d", "*", col)
        column_headings.update({col: heading_formatters[datasource.headings_type](headings.get(non_index_based, col))})
    return column_headings


def set_column_headings(datasource, analyzed_file_path):
    current_language_code = get_language()
    with open(analyzed_file_path) as fd:
        tables = json.loads(fd.read())["tables"]
    if datasource.headings_type.startswith("es"):
        activate("es")
    for table in datasource.tables.all():
        table.column_headings = get_column_headings(datasource, tables, table)
        table.save(update_fields=["column_headings"])
        if table.split:
            for a_table in table.array_tables.all():
                a_table.column_headings = get_column_headings(datasource, tables, a_table)
                a_table.save(update_fields=["column_headings"])
    activate(current_language_code)


def is_release_package(filepath):
    with open(filepath, "rb") as f:
        items = ijson.items(f, "releases.item")
        for item in items:
            if item:
                return True
    return False


def is_record_package(filepath):
    with open(filepath, "rb") as f:
        items = ijson.items(f, "records.item")
        for item in items:
            if item:
                return True
    return False


@contextmanager
def internationalization(lang_code="en"):
    current_lang = get_language()
    try:
        activate(lang_code)
        yield
    finally:
        activate(current_lang)


def zip_files(source_dir, zipfile, extension=None):
    with ZipFile(zipfile, "w") as fzip:
        for folder, _, files in os.walk(source_dir):
            for file_ in files:
                if extension and file_.endswith(extension):
                    fzip.write(os.path.join(folder, file_), file_)


def get_flatten_options(selection):
    selections = {}
    exclude_tables_list = []

    for table in selection.tables.all():
        if not table.include:
            exclude_tables_list.append(table.name)
            continue
        selections[table.name] = {"split": table.split}
        if table.column_headings:
            selections[table.name]["headers"] = table.column_headings
        if table.heading:
            selections[table.name]["name"] = table.heading
        if table.split:
            for a_table in table.array_tables.all():
                if not a_table.include:
                    exclude_tables_list.append(a_table.name)
                    continue
                selections[a_table.name] = {"split": a_table.split}
                if a_table.column_headings:
                    selections[a_table.name]["headers"] = a_table.column_headings
                if a_table.heading:
                    selections[a_table.name]["name"] = a_table.heading
    options = {"selection": selections}
    if exclude_tables_list:
        options["exclude"] = exclude_tables_list
    return options
