from pathlib import Path
from typing import Iterable

import pandas as pd

from pycbecs.codes import CodeHeaders, make_code_dict


class Cbecs2018DataHandler:
    def __init__(self):
        pass

    @staticmethod
    def load_microdata(filepath: Path) -> pd.DataFrame:
        return pd.read_csv(filepath)

    @staticmethod
    def load_codebook(filepath: Path) -> pd.DataFrame:
        cbecs_codebook = pd.read_excel(filepath, skiprows=1, skipfooter=1)
        cbecs_codebook.columns = [e.value for e in CodeHeaders]
        cbecs_codebook = cbecs_codebook.set_index(CodeHeaders.var_name)
        return cbecs_codebook

    @staticmethod
    def filter_codebook(
        codebook: pd.DataFrame,
        var_names: Iterable,
    ):
        cbecs_codebook = codebook.loc[[e for e in var_names]]
        return cbecs_codebook

    @staticmethod
    def transform_codes_to_dict(
        codebook: pd.DataFrame,
    ):
        cbecs_codebook = codebook.copy()
        cbecs_codebook.loc[:, CodeHeaders.codes] = cbecs_codebook.loc[
            :, CodeHeaders.codes
        ].apply(make_code_dict)
        return cbecs_codebook
