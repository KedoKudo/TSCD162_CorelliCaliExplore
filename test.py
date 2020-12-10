# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# load and merge the peaks
LoadIsawPeaks(Filename='/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_runs_133752_133812.peaks', OutputWorkspace='pws1')
LoadIsawPeaks(Filename="/SNS/CORELLI/IPTS-23019/shared/Natrolite/Natrolite_runs_133813_133871.peaks", OutputWorkspace="pws2")
CombinePeaksWorkspaces(LHSWorkspace="pws1", RHSWorkspace="pws2", OutputWorkspace="pws")

# calibrate the detector with SCDCalibratePanels
SCDCalibratePanels(
    PeakWorkspace='pws',
    DetCalFilename='corelli_natrolite.DetCal',
    XmlFilename='corelli_natrolite.xml',
    a=18.29, b=18.64, c=6.56, 
    alpha=90, beta=90, gamma=90,
    )

# load empty instrument
LoadEmptyInstrument(Filename="CORELLI_Definition.xml", OutputWorkspace="cws")
LoadParameterFile(Workspace="cws", Filename='corelli_natrolite.xml')

