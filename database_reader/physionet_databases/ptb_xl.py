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
    "PTB_XL",
]


class PTB_XL(PhysioNetDataBase):
    """ NOT finished,

    PTB-XL, a large publicly available electrocardiography dataset

    ABOUT ptb-xl
    ------------
    1. consists of 21837 clinical 12-lead ECGs from 18885 patients of 10 second length between October 1989 and June 1996
    2. data was annotated by up to two cardiologists, who assigned potentially multiple ECG statements to each record. The in total 71 different ECG statements conform to the SCP-ECG standard and cover diagnostic, form, and rhythm statements
    3. original sampling frequency is 500Hz (stored in the folder ./records500); 100Hz down-sampled data are stored in the folder ./records100
    4. distribution of diagnosis
        #Records    Superclass  Description
        9528        NORM        Normal ECG
        5486        MI          Myocardial Infarction
        5250        STTC        ST/T Change
        4907        CD          Conduction Disturbance
        2655        HYP         Hypertrophy
    5. all metadata is stored in ./ptbxl_database.csv, with 28 columns, which can be categorized into
        category                    columns
        Identifiers                 ecg_id, patient_id, filename_hr, filename_lr
        General Metadata            age, sex, height, weight, nurse, site, device, recording_date
        ECG statements              scp_codes, report, heart_axis, infarction_stadium1,
                                    infarction_stadium2, validated_by, second_opinion,
                                    initial_autogenerated_report, validated_by_human
        Signal Metadata             static_noise, burst_noise, baseline_drift, electrodes_problems,
                                    extra_beats, pacemaker
        Cross-validation Folds      strat_fold
    6. the "scp_codes" are organized in the form of dict with "statement: likelihood" as key, value pairs
    7. the file ./scp_statements.csv stores mappings to other annotation standards such as AHA, aECGREFID, CDISC and DICOM, and side-information such as the category each statement can be assigned to (diagnostic, form and/or rhythm). For diagnostic statements, a proposed hierarchical organization into "diagnostic_class" and "diagnostic_subclass" is provided.

    NOTE
    ----
    1. in the "scp_codes" column, which is of the form "statement: likelihood", the likelihood is set to 0 if unknown

    ISSUES
    ------

    Usage
    -----
    1. ECG arrhythmia detection

    References
    ----------
    [1] https://physionet.org/content/ptb-xl/1.0.1/
    [2] https://physionetchallenges.github.io/2020/
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
        super().__init__(db_name="ptb-xl", db_dir=db_dir, working_dir=working_dir, verbose=verbose, **kwargs)
        self.data_ext = "dat"
        self.ann_ext = "atr"
        # wfdb.get_record_list currently not available for this new dataset
        self._ls_rec()
        
        self.fs = kwargs.get("fs", 500)
        assert int(self.fs) in [100, 500]
        self.spacing = 1000/self.fs

        self.metadata_fp = os.path.join(self.db_dir, "ptbxl_database.csv")
        self.scp_statements_fp = os.path.join(self.db_dir, "scp_statements.csv")
        self.df_metadata = pd.read_csv(self.metadata_fp)
        self.df_scp_statements = pd.read_csv(self.scp_statements_fp)
        

    def get_subject_id(self, rec) -> int:
        """

        """
        raise NotImplementedError


    def database_info(self) -> NoReturn:
        """

        """
        print(self.__doc__)
