# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# lattice constant for natrolite
# https://aip.scitation.org/doi/10.1063/1.2014932
a = 18.350_8  # A
b = 18.622_7  # A
c = 6.600_3  # A
alpha = 90  # deg
beta = 90  # deg
gamma = 90  # deg
lc_natrolite = {
    "a": a, "b": b, "c": c,
    "alpha": alpha, "beta": beta, "gamma": gamma,
}


def filter_peak_ws_by_bank(peak_ws, bank_nums):
    """poorman's tool for filtering peaks with bank name"""
    peaks_not_in_banks = []
    outwsn = f"{peak_ws}_b{'_'.join(map(str, bank_nums))}"
    CloneWorkspace(InputWorkspace=peak_ws, OutputWorkspace=outwsn)
    _pws = mtd[peak_ws]
    _banks = [f"bank{n}" for n in bank_nums]
    for i in range(_pws.getNumberPeaks()):
        if _pws.cell(i, 13) not in _banks:  # bank id is 13
            peaks_not_in_banks.append(i)
    # remove peaks not in banks
    DeleteTableRows(TableWorkspace=mtd[outwsn],Rows=peaks_not_in_banks)

# ------------------------
# load and merge the peaks
LoadIsawPeaks(Filename='/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_runs_133752_133812.peaks', OutputWorkspace='pws1')
LoadIsawPeaks(Filename="/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_runs_133813_133871.peaks", OutputWorkspace="pws2")
CombinePeaksWorkspaces(LHSWorkspace="pws1", RHSWorkspace="pws2", OutputWorkspace="pws")

# only calibrate bank 50 and 78
filter_peak_ws_by_bank("pws", [50, 78, 87])

# ----------------------------
# load the associated nxs file
filename = "/SNS/CORELLI/IPTS-23019/nexus/CORELLI_133752.nxs.h5"
LoadEventNexus(Filename=filename, OutputWorkspace='ws')

# ----------------------------------------------
# calibrate the detector with SCDCalibratePanels 
# without adjusting L1 and T0
SCDCalibratePanels(
    PeakWorkspace='pws_b50_78_87',
    # PeakWorkspace='pws',
    DetCalFilename='corelli_natrolite_noL1T0.DetCal',
    XmlFilename='corelli_natrolite_noL1T0.xml',
    ChangeL1=False, ChangeT0=False,
    **lc_natrolite,
    )
CloneWorkspace(InputWorkspace="ws", OutputWorkspace="ws_noL1T0")
LoadParameterFile(Workspace="ws_noL1T0", Filename='corelli_natrolite_noL1T0.xml')

# ----------------------------------------------
# calibrate the detector with SCDCalibratePanels 
# with adjusting L1 and T0
SCDCalibratePanels(
    PeakWorkspace='pws_b50_78_87',
    # PeakWorkspace='pws',
    DetCalFilename='corelli_natrolite.DetCal',
    XmlFilename='corelli_natrolite.xml',
    ChangeL1=True, ChangeT0=True,
    **lc_natrolite,
    )
CloneWorkspace(InputWorkspace="ws", OutputWorkspace="ws_fitAll")
LoadParameterFile(Workspace="ws_fitAll", Filename='corelli_natrolite.xml')
