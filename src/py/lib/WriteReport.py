def writeDocReport(path, IOpath, fps, labels):
    import win32com.client as win32
    import os
    import sys
    import re
    
    import TextProcessing
    import ReportLoadFile
    import WriteTable
    import WriteFigure

    #---------Get full paths of all needed input files----------
    er = ReportLoadFile.EvalReport(fps, labels)
    gd = ReportLoadFile.GeneDatabase(fps, labels)
    pd = ReportLoadFile.PathwayDatabase(fps, labels)
    bnt = ReportLoadFile.NetworkTable(fps, labels)
    if labels.method=='badge':
        dgr = ReportLoadFile.DiffGeneReport_Badge(fps, labels)
        dagr = ReportLoadFile.DiffAllGeneReport_Badge(fps, labels)
    else:
        dgr = ReportLoadFile.DiffGeneReport_Limma(fps, labels)
        dagr = ReportLoadFile.DiffAllGeneReport_Limma(fps, labels)
    olr = ReportLoadFile.OverlapReport(fps, labels)
    olar = ReportLoadFile.OverlapAllReport(fps, labels)
    #==================================

    #======FUNCTIONS===================
    def WriteCutoff(w):
        TextProcessing.search_replace_all(w,'<tag: cutoff>', labels.cutoff)
        print "WriteCutoff: Over!"
    def WriteAllAnnTabs(doc, w):
        if labels.method == 'badge':
            for comp in labels.comp2:
                tb = WriteTable.Ann_Badge(doc, w, '<tag: table - annotation table - %s>' % comp, gd[comp], dgr[comp])
            for overlap in labels.overlap:
                tb = WriteTable.Ann_Overlap_Badge(doc, w, '<tag: table - annotation table - %s>' % overlap, gd[overlap], olr[overlap])
        else:
            for comp in labels.comp2:
                tb = WriteTable.Ann_Limma(doc, w, '<tag: table - annotation table - %s>' % comp, gd[comp], dgr[comp])
            for overlap in labels.overlap:
                tb = WriteTable.Ann_Overlap_Limma(doc, w, '<tag: table - annotation table - %s>' % overlap, gd[overlap], olr[overlap])
    def WriteAllPathwayTabs(doc, w):
        for comp in labels.comp:
            if comp == 'overlap1':
                tb = WriteTable.Pathway2(doc, w, '<tag: table - pathway table - %s>' % comp, pd[comp])
            else:
                tb = WriteTable.Pathway(doc, w, '<tag: table - pathway table - %s>' % comp, pd[comp], dagr[comp])
    def WriteNetworkTabs(doc, w):
        for comp in labels.comp:
            tb = WriteTable.NetworkTable(doc, w, '<tag: table - network table - %s>' % comp, bnt[comp])
    def WriteCalCluster(doc, w):
        for comp in labels.comp:
            tb = WriteTable.CalCluster(doc, w, '<tag: table - cluster - %s>' % comp, pd[comp])

    #==================================

    #======Main Space==================
    #---------Open doc file------------
    wpath_template = IOpath.template+'/'+labels.templatefnm
    wpath_report = IOpath.report+'/'+labels.reportfnm
    w = win32.Dispatch('Word.Application')
    try:
        doc = w.Documents.Open(wpath_template.replace('/','\\'))
        print "%s : Open Successfully!" % wpath_template
    except:
        print "ERROR!"
        sys.exit(0)

    w.Options.Overtype = False # Current: insert mode
    w.Visible = False # Don't show the word document
    #------------Add Content--------------
    
    print 'Writing Report...\n'

    Navigation = """
    *************************************************************
    Enter command:

    1. Write cutoff
    2. Insert Flow Chart
    3. Write overview tables on different types of samples
    4. Write annotation tables
    5. Write Pathway tables
    6. Insert network Figures
    7. Write network tables
    8. Write Cluster Info
    A. Execute all steps
    Other. Terminate writing
    *************************************************************

    """

    while(1):
        command = raw_input(Navigation)
        if command == '1':
            WriteCutoff(w)
        elif command == '2':
            fg_fc = WriteFigure.FlowChart(doc, w, '<tag: figure - flow chart>', path.flowchart)
        elif command == '3':    
            WriteTable.OverviewTab(doc, w, '<tag: table - overview statistics>', labels, dgr, er)
        elif command == '4':
            WriteAllAnnTabs(doc, w)
        elif command == '5':
            WriteAllPathwayTabs(doc, w)
        elif command == '6':
            WriteFigure.STRNetwork(doc, w, '<tag: figure - STRING networks>', 2, fps['STRING Network'], labels)
        elif command == '7':
            WriteNetworkTabs(doc, w)
        elif command == '8':
            WriteCalCluster(doc, w)
        else:
            break

    if command == 'A' or command == 'a':
        WriteCutoff(w)
        fg_fc = WriteFigure.FlowChart(doc, w, '<tag: figure - flow chart>', path.flowchart)
        WriteTable.OverviewTab(doc, w, '<tag: table - overview statistics>', labels, dgr, er)
        WriteAllAnnTabs(doc, w)
        WriteAllPathwayTabs(doc, w)
        WriteFigure.STRNetwork(doc, w, '<tag: figure - STRING networks>', 2, fps['STRING Network'], labels)
        WriteNetworkTabs(doc, w)
        WriteCalCluster(doc, w)

    doc.SaveAs(wpath_report.replace('/','\\'))
    doc.Close(False)
    w.Application.Quit()
    del w

def writeXlsReport(path, fps, labels):
    import win32com.client as win32
    import os
    import sys
    import re

    import ReportLoadFile
    import WriteExcel

    er = ReportLoadFile.EvalReport(fps, labels)
    gd = ReportLoadFile.GeneDatabase(fps, labels)
    dgr = ReportLoadFile.DiffGeneReport(fps, labels)
    pd = ReportLoadFile.PathwayDatabase(fps, labels)
    bnt = ReportLoadFile.NetworkTable(fps, labels)
    dagr = ReportLoadFile.DiffAllGeneReport(fps, labels)

    xlpath = path.report+'/'+labels.xlsfnm
    xl = win32.Dispatch('Excel.Application')
    wb = xl.Workbooks.Add()
    print "New workbook added successfully"

    #-------------------Write in excel-----------------------------
    for comp in labels.comp2:
        WriteExcel.AllGenes(wb, comp, labels, dagr[comp])


    print xlpath.replace('/','\\')
    wb.SaveAs(xlpath.replace('/','\\'))
    wb.Close(False)
    xl.Application.Quit()
    del xl
        