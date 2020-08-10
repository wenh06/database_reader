# -*- coding: utf-8 -*-
"""
"""
import os
import json
from datetime import datetime
from typing import Union, Optional, Any, List, Tuple, Sequence, NoReturn
from numbers import Real

import numpy as np
import pandas as pd
import wfdb
from easydict import EasyDict as ED

from database_reader.utils.common import (
    ArrayLike,
    get_record_list_recursive,
)
from database_reader.base import PhysioNetDataBase, ECGWaveForm


__all__ = [
    "LUDB",
]


class LUDB(PhysioNetDataBase):
    """ NOT Finished, 

    Lobachevsky University Electrocardiography Database

    ABOUT ludb:
    -----------
    1. consist of 200 10-second conventional 12-lead (i, ii, iii, avr, avl, avf, v1, v2, v3, v4, v5, v6) ECG signal records, with sampling frequency 500 Hz
    2. boundaries of P, T waves and QRS complexes were manually annotated by cardiologists, and with the corresponding diagnosis
    3. annotated are 16797 P waves, 21966 QRS complexes, 19666 T waves (in total, 58429 annotated waves)
    4. distributions of data:
        4.1. rhythm distribution:
            Rhythms	                        Number of ECGs
            Sinus rhythm	                143
            Sinus tachycardia	            4
            Sinus bradycardia	            25
            Sinus arrhythmia	            8
            Irregular sinus rhythm	        2
            Abnormal rhythm	                19
        4.2. electrical axis distribution:
            Heart electric axis	            Number of ECGs
            Normal	                        75
            Left axis deviation (LAD)	    66
            Vertical	                    26
            Horizontal	                    20
            Right axis deviation (RAD)	    3
            Undetermined	                10
        4.3. distribution of records with conduction abnomalities (totally 79):
            Conduction abnormalities	                        Number of ECGs
            Sinoatrial blockade, undetermined	                1
            I degree AV block	                                10
            III degree AV-block	                                5
            Incomplete right bundle branch block	            29
            Incomplete left bundle branch block	                6
            Left anterior hemiblock	                            16
            Complete right bundle branch block	                4
            Complete left bundle branch block	                4
            Non-specific intravintricular conduction delay	    4
        4.4. distribution of records with extrasystoles (totally 35):
            Extrasystoles	                                                    Number of ECGs
            Atrial extrasystole, undetermined	                                2
            Atrial extrasystole, low atrial	                                    1
            Atrial extrasystole, left atrial	                                2
            Atrial extrasystole, SA-nodal extrasystole	                        3
            Atrial extrasystole, type: single PAC	                            4
            Atrial extrasystole, type: bigemini	                                1
            Atrial extrasystole, type: quadrigemini	                            1
            Atrial extrasystole, type: allorhythmic pattern	                    1
            Ventricular extrasystole, morphology: polymorphic	                2
            Ventricular extrasystole, localisation: RVOT, anterior wall	        3
            Ventricular extrasystole, localisation: RVOT, antero-septal part	1
            Ventricular extrasystole, localisation: IVS, middle part	        1
            Ventricular extrasystole, localisation: LVOT, LVS	                2
            Ventricular extrasystole, localisation: LV, undefined	            1
            Ventricular extrasystole, type: single PVC	                        6
            Ventricular extrasystole, type: intercalary PVC	                    2
            Ventricular extrasystole, type: couplet	                            2
        4.5. distribution of records with hypertrophies (totally 253):
            Hypertrophies	                    Number of ECGs
            Right atrial hypertrophy	        1
            Left atrial hypertrophy	            102
            Right atrial overload	            17
            Left atrial overload	            11
            Left ventricular hypertrophy	    108
            Right ventricular hypertrophy	    3
            Left ventricular overload	        11
        4.6. distribution of records of pacing rhythms (totally 12):
            Cardiac pacing	                Number of ECGs
            UNIpolar atrial pacing	        1
            UNIpolar ventricular pacing	    6
            BIpolar ventricular pacing	    2
            Biventricular pacing	        1
            P-synchrony	                    2
        4.7. distribution of records with ischemia (totally 141):
            Ischemia	                                            Number of ECGs
            STEMI: anterior wall	                                8
            STEMI: lateral wall	                                    7
            STEMI: septal	                                        8
            STEMI: inferior wall	                                1
            STEMI: apical	                                        5
            Ischemia: anterior wall	                                5
            Ischemia: lateral wall	                                8
            Ischemia: septal	                                    4
            Ischemia: inferior wall	                                10
            Ischemia: posterior wall	                            2
            Ischemia: apical	                                    6
            Scar formation: lateral wall	                        3
            Scar formation: septal	                                9
            Scar formation: inferior wall	                        3
            Scar formation: posterior wall	                        6
            Scar formation: apical	                                5
            Undefined ischemia/scar/supp.NSTEMI: anterior wall	    12
            Undefined ischemia/scar/supp.NSTEMI: lateral wall	    16
            Undefined ischemia/scar/supp.NSTEMI: septal	            5
            Undefined ischemia/scar/supp.NSTEMI: inferior wall	    3
            Undefined ischemia/scar/supp.NSTEMI: posterior wall	    4
            Undefined ischemia/scar/supp.NSTEMI: apical	            11
        4.8. distribution of records with non-specific repolarization abnormalities (totally 85):
            Non-specific repolarization abnormalities	    Number of ECGs
            Anterior wall	                                18
            Lateral wall	                                13
            Septal	                                        15
            Inferior wall	                                19
            Posterior wall	                                9
            Apical	                                        11
        4.9. there are also 9 records with early repolarization syndrome
        there might well be records with multiple conditions.
    

    NOTE:
    -----

    ISSUES:
    -------

    Usage:
    ------
    1. ECG wave delineation
    2. ECG arrhythmia classification

    References:
    -----------
    [1] https://physionet.org/content/ludb/1.0.0/
    [2] Kalyakulina, A., Yusipov, I., Moskalenko, V., Nikolskiy, A., Kozlov, A., Kosonogov, K., Zolotykh, N., & Ivanchenko, M. (2020). Lobachevsky University Electrocardiography Database (version 1.0.0).
    """
    def __init__(self, db_dir:str, working_dir:Optional[str]=None, verbose:int=2, **kwargs):
        """
        Parameters:
        -----------
        db_dir: str,
            storage path of the database
        working_dir: str, optional,
            working directory, to store intermediate files and log file
        verbose: int, default 2,
        """
        super().__init__(db_name='ludb', db_dir=db_dir, working_dir=working_dir, verbose=verbose, **kwargs)
        self.freq = 500
        self.spacing = 1000 / self.freq
        self.data_ext = "dat"
        self.all_leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6',]
        self.beat_ann_ext = [f"atr_{item.lower()}" for item in self.all_leads]

        self._all_symbols = ['(', ')', 'N', 'p', 't']
        """
        this can be obtained using the following code:
        >>> data_gen = LUDB(db_dir="/home/wenhao71/data/PhysioNet/ludb/1.0.0/")
        >>> all_symbols = set()
        >>> for rec in data_gen.all_records:
        ...     for ext in data_gen.beat_ann_ext:
        ...         ann = wfdb.rdann(os.path.join(data_gen.db_dir, rec), extension=ext)
        ...         all_symbols.update(ann.symbol)
        """
        self._symbol_to_wavename = ED(N='qrs', p='pwave', t='twave')

        self._ls_rec()
    

    def get_subject_id(self, rec:str) -> int:
        """

        """
        raise NotImplementedError


    def load_data(self, rec:str) -> np.ndarray:
        """

        """
        raise NotImplementedError


    def load_ann(self, rec:str, leads:Optional[Sequence[str]]=None, metadata:bool=False) -> dict:
        """

        Parameters:
        -----------

        Returns:
        --------
        """
        ann_dict = ED()

        # wave delineation annotations
        _leads = leads or self.all_leads
        _leads = [l for l in self.all_leads if l in _leads]  # keep in order
        _ann_ext = [f"atr_{item.lower()}" for item in _leads]
        ann_dict['waves'] = ED({l:[] for l in _leads})
        for l, e in zip(_leads, _ann_ext):
            ann = wfdb.rdann(os.path.join(self.db_dir, rec), extension=e)
            df_lead_ann = pd.DataFrame()
            symbols = np.array(ann.symbol)
            peak_inds = np.where(np.isin(symbols, ['p', 'N', 't']))[0]
            df_lead_ann['peak'] = ann.sample[peak_inds]
            df_lead_ann['onset'] = np.nan
            df_lead_ann['offset'] = np.nan
            for i, row in df_lead_ann.iterrows():
                peak_idx = peak_inds[i]
                if peak_idx == 0:
                    df_lead_ann.loc[i, 'onset'] = row['peak']
                    if symbols[peak_idx+1] == ')':
                        df_lead_ann.loc[i, 'offset'] = ann.sample[peak_idx+1]
                    else:
                        df_lead_ann.loc[i, 'offset'] = row['peak']
                elif peak_idx == len(symbols) - 1:
                    df_lead_ann.loc[i, 'offset'] = row['peak']
                    if symbols[peak_idx-1] == '(':
                        df_lead_ann.loc[i, 'onset'] = ann.sample[peak_idx-1]
                    else:
                        df_lead_ann.loc[i, 'onset'] = row['peak']
                else:
                    if symbols[peak_idx-1] == '(':
                        df_lead_ann.loc[i, 'onset'] = ann.sample[peak_idx-1]
                    else:
                        df_lead_ann.loc[i, 'onset'] = row['peak']
                    if symbols[peak_idx+1] == ')':
                        df_lead_ann.loc[i, 'offset'] = ann.sample[peak_idx+1]
                    else:
                        df_lead_ann.loc[i, 'offset'] = row['peak']
            # df_lead_ann['onset'] = ann.sample[np.where(symbols=='(')[0]]
            # df_lead_ann['offset'] = ann.sample[np.where(symbols==')')[0]]

            df_lead_ann['duration'] = (df_lead_ann['offset'] - df_lead_ann['onset']) * self.spacing
            
            df_lead_ann.index = symbols[peak_inds]

            for c in ['peak', 'onset', 'offset']:
                df_lead_ann[c] = df_lead_ann[c].values.astype(int)
            
            for _, row in df_lead_ann.iterrows():
                w = ECGWaveForm(
                    name=self._symbol_to_wavename[row.name],
                    onset=int(row.onset),
                    offset=int(row.offset),
                    peak=int(row.peak),
                    duration=row.duration,
                )
                ann_dict['waves'][l].append(w)

        if metadata:
            raise NotImplementedError
        
        return ann_dict


    def database_info(self) -> NoReturn:
        """

        """
        print(self.__doc__)
