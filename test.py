# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# ------------------------
# load and merge the peaks
LoadIsawPeaks(Filename='/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_runs_133752_133812.peaks', OutputWorkspace='pws1')
LoadIsawPeaks(Filename="/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_runs_133813_133871.peaks", OutputWorkspace="pws2")
CombinePeaksWorkspaces(LHSWorkspace="pws1", RHSWorkspace="pws2", OutputWorkspace="pws")

# ----------------------------
# load the associated nxs file
filename = "/SNS/CORELLI/IPTS-16227/nexus/CORELLI_23019.nxs.h5"
LoadEventNexus(Filename=filename, OutputWorkspace='ws')

# ----------------------------------------------
# calibrate the detector with SCDCalibratePanels 
# without adjusting L1 and T0
SCDCalibratePanels(
    PeakWorkspace='pws',
    DetCalFilename='corelli_natrolite_noL1T0.DetCal',
    XmlFilename='corelli_natrolite_noL1T0.xml',
    a=18.29, b=18.64, c=6.56, 
    alpha=90, beta=90, gamma=90,
    ChangeL1=False, ChangeT0=False,
    )
CloneWorkspace(InputWorkspace="ws", OutputWorkspace="ws_noL1T0")
LoadParameterFile(Workspace="ws_noL1T0", Filename='corelli_natrolite_noL1T0.xml')

# ----------------------------------------------
# calibrate the detector with SCDCalibratePanels 
# with adjusting L1 and T0
SCDCalibratePanels(
    PeakWorkspace='pws',
    DetCalFilename='corelli_natrolite.DetCal',
    XmlFilename='corelli_natrolite.xml',
    a=18.29, b=18.64, c=6.56, 
    alpha=90, beta=90, gamma=90,
    ChangeL1=True, ChangeT0=True,
    )
CloneWorkspace(InputWorkspace="ws", OutputWorkspace="ws_fitAll")
LoadParameterFile(Workspace="ws_fitAll", Filename='corelli_natrolite.xml')
