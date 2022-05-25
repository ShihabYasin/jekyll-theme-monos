import importlib
import os
import sys

import pandas as pd
import shutil

file_path = None


class GenericFileHelper:
    # file related
    @classmethod
    def create_file(cls, file_path):
        f = open (file_path, 'a+')
        f.close ()

    @classmethod
    def remove_file(cls, file_path):
        if os.path.exists (file_path):
            os.remove (file_path)

    @classmethod
    def read_file_lines(cls, file_path):
        with open (file_path) as f:
            lines = f.readlines ()
        return lines

    @classmethod
    def append_file(cls, file_path, lines_to_append=[], append_beginning_of_file=True):
        with open (file_path, 'r') as f:
            old_lines = f.readlines ()
        for new_line in lines_to_append:
            flag = True
            for old_line in old_lines:
                if new_line in old_line:
                    flag = False
                    break

            if flag:
                if append_beginning_of_file:
                    old_lines.insert (0, new_line)
                else:
                    old_lines.append (new_line)

        a_file = open (file_path, "w")
        a_file.writelines (old_lines)
        a_file.close ()

    @classmethod
    def large_text_file_reader(file_name):
        try:
            for _line in open (file_name, "r"):
                yield _line.strip ()
        except Exception as e:
            print (e, file=open ('log_large_text_file_reader.txt', 'a'))
            yield (f'error')


class GenericTextProcessing:
    pass


class GenericDictHelper:
    @classmethod
    def get_all_key_value(cls, dictionary: dict):
        ls = []
        for key, value in dictionary.items ():
            ls.append ((key, value))
        return ls


class GenericETLHelper:
    @classmethod
    def collect_columns_from_tsv_or_csv_file(cls, file_path='a.tsv', input_column_separator="\t", colms_to_colllect=[0, 2]):
        '''For csv use coma'''
        dataset = pd.read_csv (file_path, sep=input_column_separator)
        df = pd.DataFrame (dataset)
        df = df[df.columns[colms_to_colllect]]
        ls = df.values.tolist ()
        return ls


class GenericPythonHelper:
    @classmethod
    def format_pyhton_file(cls, file_path):
        os.system (f'autopep8 -i {file_path} ')

    @classmethod
    def import_module_from_file(cls, file_path='django_prepare_project_0.8.py', module_name='django_prepare_project'):
        # After calling this f() Use module in code like ==>  from django_prepare_project import DebugHelper
        spec = importlib.util.spec_from_file_location (module_name, file_path)
        module = importlib.util.module_from_spec (spec)
        spec.loader.exec_module (module)
        sys.modules[module_name] = module
