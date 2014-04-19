import win32com.client as win32
import os, sys
cwd = os.getcwd()
path_lib = cwd + '/lib'
sys.path.append(path_lib)

path_work = cwd+'/../mouse2'
method = raw_input('L for limma/B for badge: ')

import Labels
import Path
labels = Labels.Labels(method)
path = Path.DataPaths(path_work,labels)
progpath = Path.ProgramPath(cwd)
expath = Path.ExternalPath()
IOpath = Path.IOPath(path_work)
fps = Path.AllFilesFP(path, labels)

import PreProcess
PreProcess.RMA(path, expath, progpath, labels)

if method=='L':
    import CallLimma
    CallLimma.Limma(path, expath, progpath, fps, labels)
else:
    words = 'Run Badge please. Input files appear in %s. Please save your file to directory: %s. Set the filenames like: grp1_grp2_selected_unsorted.txt. Then press Enter to continue. ' % (path.exprdata, path.genereport)
    raw_input(words)

if method=='L':
    import GetGenes
    GetGenes.getOverlap_Limma(fps, labels)
    GetGenes.geneSymToAffyID(fps, labels)
else:
    import GetGenes
    GetGenes.Sort(fps, labels)
    GetGenes.getOverlap_Badge(fps, labels)
    GetGenes.geneSymToAffyID(fps, labels)


import David
David.davidCall(fps, labels)

import String
String.stringCall(path, fps, labels)
String.genEdgeList(path, fps, labels)
String.genNetworkInput(path, fps, labels)
String.genNetwork(path, progpath)
String.annoNetwork(path, progpath, fps, labels)

import CrossValidation
CrossValidation.exprToArff(path, fps, labels)
CrossValidation.syncArffFeatures(path, fps, labels)
CrossValidation.callWeka(fps, labels)

import WriteReport
WriteReport.writeDocReport(path, IOpath, fps, labels)
