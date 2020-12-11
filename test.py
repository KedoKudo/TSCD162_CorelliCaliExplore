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


# ------------------------
# load and merge the peaks
LoadIsawPeaks(Filename='/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_runs_133752_133812.peaks', OutputWorkspace='pws')

# ----------------------------
# load the associated nxs file
filename = "/SNS/CORELLI/IPTS-23019/nexus/CORELLI_133752.nxs.h5"
LoadEventNexus(Filename=filename, OutputWorkspace='ws_mantid')
CloneWorkspace(InputWorkspace="ws_mantid", OutputWorkspace="ws_isaw")

# ----------------------------------------------
# calibrate the detector with SCDCalibratePanels 
# without adjusting L1 and T0
SCDCalibratePanels(
    PeakWorkspace='pws',
    DetCalFilename='corelli_natrolite_mantid.DetCal',
    ChangeL1=True, ChangeT0=True,
    **lc_natrolite,
    )

# ---------
# compare
LoadIsawDetCal("ws_isaw", "corelli_natrolite_isaw.DetCal")
LoadIsawDetCal("ws_mantid", "corelli_natrolite_mantid.DetCal")
