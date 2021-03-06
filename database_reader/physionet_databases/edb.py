# -*- coding: utf-8 -*-
"""
"""
import os
from datetime import datetime
from typing import Union, Optional, Any, List, NoReturn
from numbers import Real

import wfdb
import numpy as np
np.set_printoptions(precision=5, suppress=True)
import pandas as pd

from ..utils.common import (
    ArrayLike,
    get_record_list_recursive,
)
from ..base import PhysioNetDataBase


__all__ = [
    "EDB",
]


class EDB(PhysioNetDataBase):
    """ NOT finished,

    European ST-T Database

    ABOUT edb
    ---------
    to write

    NOTE
    ----

    ISSUES
    ------

    Usage
    -----
    1. ST segment

    References
    ----------
    [1] https://physionet.org/content/edb/1.0.0/
    """
    def __init__(self, db_dir:Optional[str]=None, working_dir:Optional[str]=None, verbose:int=2, **kwargs:Any) -> NoReturn:
        """
        Parameters
        ----------
        db_dir: str, optional,
            storage path of the database
            if not specified, data will be fetched from Physionet
        working_dir: str, optional,
            working directory, to store intermediate files and log file
        verbose: int, default 2,
            log verbosity
        kwargs: auxilliary key word arguments
        """
        super().__init__(db_name="edb", db_dir=db_dir, working_dir=working_dir, verbose=verbose, **kwargs)
        self.data_ext = "dat"
        self.ann_ext = "atr"
        self.all_leads = ["V1", "V2", "V3", "V4", "V5", "D3", "MLI", "MLIII"]

        self._ls_rec()


    def _ls_rec(self, local:bool=True) -> NoReturn:
        """ finished, checked,

        find all records (relative path without file extension),
        and save into `self._all_records` for further use

        Parameters
        ----------
        local: bool, default True,
            if True, read from local storage, prior to using `wfdb.get_record_list`
        """
        try:
            super()._ls_rec(local=local)
        except:
            self._all_records = [
                "e0103", "e0104", "e0105", "e0106", "e0107", "e0108", "e0110",
                "e0111", "e0112", "e0113", "e0114", "e0115", "e0116", "e0118",
                "e0119", "e0121", "e0122", "e0123", "e0124", "e0125", "e0126",
                "e0127", "e0129", "e0133", "e0136", "e0139", "e0147", "e0148",
                "e0151", "e0154", "e0155", "e0159", "e0161", "e0162", "e0163",
                "e0166", "e0170", "e0202", "e0203", "e0204", "e0205", "e0206",
                "e0207", "e0208", "e0210", "e0211", "e0212", "e0213", "e0302",
                "e0303", "e0304", "e0305", "e0306", "e0403", "e0404", "e0405",
                "e0406", "e0408", "e0409", "e0410", "e0411", "e0413", "e0415",
                "e0417", "e0418", "e0501", "e0509", "e0515", "e0601", "e0602",
                "e0603", "e0604", "e0605", "e0606", "e0607", "e0609", "e0610",
                "e0611", "e0612", "e0613", "e0614", "e0615", "e0704", "e0801",
                "e0808", "e0817", "e0818", "e1301", "e1302", "e1304",
            ]


    def get_subject_id(self, rec) -> int:
        """

        """
        raise NotImplementedError


    def database_info(self) -> NoReturn:
        """

        """
        print(self.__doc__)
