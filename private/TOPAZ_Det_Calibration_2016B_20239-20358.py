import math
#TOPAZ Detector calibration using new SCDCalibratePanels, 09/10/2017 
LoadIsawPeaks(Filename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/Si2mm_Cubic_F.integrate', 
  OutputWorkspace='Si_Peaks')
#Remove peaks on detector edge
peaks_on_edge=[]
for i in range(mtd['Si_Peaks'].getNumberPeaks()):
  pi=mtd['Si_Peaks'].getPeak(i)
  if pi.getSigmaIntensity() >0:
      Intens_sigI = pi.getIntensity() / pi.getSigmaIntensity()
  else:
      Intens_sigI =0.0
  if pi.getRow()<16 or pi.getRow()>240 or pi.getCol()<16 or pi.getCol()>240 or  math.isnan(pi.getSigmaIntensity()) or pi.getDSpacing()<0.60 or (pi.getIntensity() <50) or Intens_sigI < 3.0:
      peaks_on_edge.append(i)
DeleteTableRows(TableWorkspace=mtd['Si_Peaks'],Rows=peaks_on_edge)

FindUBUsingIndexedPeaks(PeaksWorkspace='Si_Peaks', Tolerance=0.20000000000000001)
IndexPeaks(PeaksWorkspace='Si_Peaks', Tolerance=0.25, RoundHKLs=False)

SCDCalibratePanels(PeakWorkspace='Si_Peaks', 
  a=5.431072, b=5.431072, c=5.431072, 
  alpha=90, beta=90, gamma=90, 
  ChangeT0=False, EdgePixels=16, 
  DetCalFilename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/TOPAZ_2017B.DetCal', 
  XmlFilename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/Si.xml', 
  ColFilename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/col.xml', 
  RowFilename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/row.xml', 
  TofFilename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/tof.nxs')

#Reindex and refine lattice constant for Si crystal using new TOPAZ detector calibration
LoadIsawDetCal(InputWorkspace='Si_Peaks', 
  Filename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/TOPAZ_2017B.DetCal')
FindUBUsingFFT(PeaksWorkspace='Si_Peaks', MinD=3, MaxD=5, Tolerance=0.18)
IndexPeaks(PeaksWorkspace='Si_Peaks', RoundHKLs=False)
ShowPossibleCells(PeaksWorkspace='Si_Peaks', BestOnly=False)
SelectCellOfType(PeaksWorkspace='Si_Peaks', Centering='F', Apply=True, AllowPermutations=False)
IndexPeaks(PeaksWorkspace='Si_Peaks', Tolerance=0.12, RoundHKLs=False)
FindUBUsingIndexedPeaks(PeaksWorkspace='Si_Peaks', Tolerance=0.12)

SaveIsawUB(InputWorkspace='Si_Peaks',
    Filename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/Si2mm_Cubic_F_use_DetCal.mat')
SaveIsawPeaks(InputWorkspace='Si_Peaks',
    Filename='/SNS/TOPAZ/IPTS-9918/shared/2016B/Si/Si2mm_useEng_20239-20358/dmin0p65minIntens50/Si2mm_Cubic_F_use_DetCal.integrate')