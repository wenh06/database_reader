# -*- coding: utf-8 -*-
"""
"""
import os
from datetime import datetime
from typing import Union, Optional, Any, List, NoReturn
from numbers import Real

import numpy as np
np.set_printoptions(precision=5, suppress=True)
import pandas as pd

from ..utils.common import (
    ArrayLike,
    get_record_list_recursive,
)
from ..base import OtherDataBase


__all__ = [
    "PPGBP",
]


class PPGBP(OtherDataBase):
    """

    ABOUT PPG_BP (ref. [1])
    -----------------------
    1. the PPG sensor:
        1.1. sensor model was SEP9AF-2 (SMPLUS Company, Korea)
        1.2. contains dual LED with 660nm (Red light) and 905 nm (Infrared) wavelengths
        1.3. sampling rate 1 kHz and 12-bit ADC
        1.4. hardware filter design is 0.5‒12Hz bandpass
    more to be written

    NOTE
    ----
    1. PPG analysis tips (ref. [1],[2]):
        1.1. Taking the first and second derivatives of the PPG signals may help in detecting the informative inflection points more accurately

    ISSUES
    ------

    Usage
    -----
    1. blood pressure prediction from PPG

    References
    ----------
    [1] Liang Y, Chen Z, Liu G, et al. A new, short-recorded photoplethysmogram dataset for blood pressure monitoring in China[J]. Scientific data, 2018, 5: 180020.
    [2] Allen J. Photoplethysmography and its application in clinical physiological measurement[J]. Physiological measurement, 2007, 28(3): R1.
    [3] Elgendi M. On the analysis of fingertip photoplethysmogram signals[J]. Current cardiology reviews, 2012, 8(1): 14-25.
    [4] https://figshare.com/articles/PPG-BP_Database_zip/5459299/3
    """
    
    def __init__(self, db_dir:str, working_dir:Optional[str]=None, verbose:int=2, **kwargs:Any) -> NoReturn:
        """ finished, to be improved,

        Parameters
        ----------
        db_dir: str,
            storage path of the database
        working_dir: str, optional,
            working directory, to store intermediate files and log file
        verbose: int, default 2,
            log verbosity
        kwargs: auxilliary key word arguments

        typical "db_dir": "/export/servers/kuangzhexiang/data/PPG_BP/"
        ------------------
        to be written
        """
        super().__init__(db_name="PPG_BP", db_dir=db_dir, working_dir=working_dir, verbose=verbose, **kwargs)

        self.ppg_data_dir = None
        self.unkown_file = None
        self.ann_file = None
        self.form_paths()

        self.fs = 1000
        self._all_records = sorted(list(set([fn.split("_")[0] for fn in os.listdir(self.ppg_data_dir)])), key=lambda r:int(r))
        self.rec_ext = "txt"

        self.ann_items = [
            "Num.", "subject_ID",
            "Sex(M/F)", "Age(year)", "Height(cm)", "Weight(kg)", "BMI(kg/m^2)",
            "Systolic Blood Pressure(mmHg)", "Diastolic Blood Pressure(mmHg)", "Heart Rate(b/m)",
            "Hypertension", "Diabetes", "cerebral infarction", "cerebrovascular disease",
        ]


    def form_paths(self) -> NoReturn:
        """ finished, checked, to be improved,

        """
        self.ppg_data_dir = os.path.join(self.db_dir, "0_subject")
        self.unkown_file = os.path.join(self.db_dir, "Table 1.xlsx")
        self.ann_file = os.path.join(self.db_dir, "PPG-BP dataset.xlsx")


    def get_subject_id(self, rec_no:int) -> int:
        """ not finished,

        Parameters
        ----------
        rec_no: int,
            number of the record, or "subject_ID"

        Returns
        -------
        int, the `subject_id` corr. to `rec_no`
        """
        return int(self._all_records[rec_no])
    

    def database_info(self, detailed:bool=False) -> NoReturn:
        """ not finished,

        print the information about the database

        detailed: bool, default False,
            if False, an short introduction of the database will be printed,
            if True, then docstring of the class will be printed additionally
        """
        raw_info = {}

        print(raw_info)
        
        if detailed:
            print(self.__doc__)
        

    def load_ppg_data(self, rec_no:int, seg_no:int, verbose: int=None) -> np.ndarray:
        """ finished, checked,

        Parameters
        ----------
        rec_no: int,
            number of the record, or "subject_ID"
        seg_no: int,
            number of the segment measured from the subject
        
        Returns
        -------
        data: ndarray,
            the ppg data
        """
        verbose = self.verbose if verbose is None else verbose
        rec_fn = f"{self._all_records[rec_no]}_{seg_no}.txt"
        data = []
        with open(self.ppg_data_dir+rec_fn, "r") as f:
            data = f.readlines()
        data = np.array([float(i) for i in data[0].split("\t") if len(i)>0]).astype(int)
        
        if verbose >= 2:
            import matplotlib.pyplot as plt
            fig,ax = plt.subplots(figsize=(8,4))
            ax.plot(np.arange(0,len(data)/self.fs, 1/self.fs),data)
            plt.show()
        
        return data


    def load_ann(self, rec_no:Optional[int]=None) -> pd.DataFrame:
        """ finished, checked,
        
        Parameters
        ----------
        rec_no: int, optional,
            number of the record, or "subject_ID",
            if not specified, then all annotations will be returned
        
        Returns
        -------
        df_ann: DataFrame,
            the annotations
        """
        df_ann = pd.read_excel(self.ann_file)
        df_ann.columns = df_ann.iloc[0]
        df_ann = df_ann[1:].reset_index(drop=True)
        
        if rec_no is None:
            return df_ann
        
        df_ann = df_ann[df_ann["subject_ID"]==int(self._all_records[rec_no])].reset_index(drop=True)
        return df_ann


    def load_diagnosis(self, rec_no:int) -> Union[List[str],list]:
        """ finished, checked,
        
        Parameters
        ----------
        rec_no: int,
            number of the record, or "subject_ID"
        
        Returns
        -------
        diagonosis: list,
            the list of diagnosis or empty list for the normal subjects
        """
        diagonosis_items = [
            "Hypertension", "Diabetes", "cerebral infarction", "cerebrovascular disease",
        ]
        df_ann = self.load_ann(rec_no)[diagonosis_items].dropna(axis=1)
        diagonosis = [item for item in df_ann.iloc[0].tolist() if item != "Normal"]
        return diagonosis


    def get_patient_info(self, rec_no:int, items:Optional[List[str]]=None) -> Union[Real,str,pd.DataFrame]:
        """ not finished,

        Parameters
        ----------
        rec_no: int,
            number of the record, or "subject_ID"
        items: list of str, optional,
            items of the patient information (e.g. sex, age, etc.)
        
        Returns
        -------
        if `items` contains only one item, then value of this item in the subject"s information will be returned,
        otherwise, a dataframe of all information of the subject will be returned
        """
        if items is None or len(items) == 0:
            info_items = [
                "Sex(M/F)","Age(year)","Height(cm)","Weight(kg)","BMI(kg/m^2)",
                "Systolic Blood Pressure(mmHg)","Diastolic Blood Pressure(mmHg)","Heart Rate(b/m)",
            ]
        else:
            info_items = items
        df_info = self.load_ann(rec_no)[info_items]
        
        if len(info_items) == 1:
            return df_info.iloc[0].values[0]
        else:
            return df_info


    def plot(self,) -> NoReturn:
        """
        """
        raise NotImplementedError
