def writeDocReport(path, IOpath, fps, labels):
    import win32com.client as win32
    import sys

    import TextProcessing
    import ReportLoadFile
    import WriteTable
    import WriteFigure

    #---------Get full paths of all needed input files----------
    si = ReportLoadFile.SampleInfo(fps, labels)
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
    tolr = ReportLoadFile.TypeOverlapReport(fps, labels)
    dr = ReportLoadFile.DiffReport(fps, labels)
    dar = ReportLoadFile.DiffAllReport(fps, labels)

    #==================================

    #======FUNCTIONS===================
    def WriteCutoff(w):
        TextProcessing.search_replace_all(w,'<tag: cutoff>', labels.cutoff)
        print "WriteCutoff: Over!"
    def WriteAllAnnTabs(doc, w):
        if labels.method == 'badge':
            for comp in labels.comp2:
                tb = WriteTable.Ann_Badge(doc, w, '<tag: table - annotation table - %s>' % comp, gd[comp], dgr[comp], tolr[comp])
            for overlap in labels.overlap:
                tb = WriteTable.Ann_Overlap_Badge(doc, w, '<tag: table - annotation table - %s>' % overlap, gd[overlap], olr[overlap])
            for diff in labels.diff:
                tb = WriteTable.Ann_Diff_Badge(doc, w, '<tag: table - annotation table - %s>' % diff, gd[diff], dr[diff], tolr[diff])
        else:
            for comp in labels.comp2:
                tb = WriteTable.Ann_Limma(doc, w, '<tag: table - annotation table - %s>' % comp, gd[comp], dgr[comp])
            for overlap in labels.overlap:
                tb = WriteTable.Ann_Overlap_Limma(doc, w, '<tag: table - annotation table - %s>' % overlap, gd[overlap], olr[overlap])
            for diff in labels.diff:
                tb = WriteTable.Ann_Diff_Limma(doc, w, '<tag: table - annotation table - %s>' % diff, gd[diff], dr[diff], tolr[diff])
    def WriteGeneSummery(doc, w):
        if labels.method == 'badge':
            for comp in labels.comp3:
                comp1 = comp + '_tp1'
                comp2 = comp + '_tp2'
                tb = WriteTable.geneSummery_Badge(doc, w, '<tag: table - summery table - %s>' % comp, labels, dgr[comp1], dagr[comp1], dgr[comp2], dagr[comp2], tolr[comp1])
        else:
            for comp in labels.comp3:
                            comp1 = comp + '_tp1'
                            comp2 = comp + '_tp2'
                            tb = WriteTable.geneSummery_Limma(doc, w, '<tag: table - summery table - %s>' % comp, labels, dgr[comp1], dagr[comp1], dgr[comp2], dagr[comp2], tolr[comp1])
    def WriteAllPathwayTabs(doc, w):
        for comp in labels.comp:
            if comp in labels.overlap:
                tb = WriteTable.Pathway2(doc, w, '<tag: table - pathway table - %s>' % comp, pd[comp])
            elif comp in labels.diff:
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
    5. Write gene summery
    6. Write Pathway tables
    7. Insert network Figures
    8. Write network tables
    9. Write Cluster Info
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
            WriteTable.OverviewTab1(doc, w, '<tag: table - overview statistics - sample>', labels, si)
            WriteTable.OverviewTab2(doc, w, '<tag: table - overview statistics - comparison>', labels, dagr, er)
        elif command == '4':
            WriteAllAnnTabs(doc, w)
        elif command == '5':
            WriteGeneSummery(doc, w)
        elif command == '6':
            WriteAllPathwayTabs(doc, w)
        elif command == '7':
            WriteFigure.STRNetwork(doc, w, '<tag: figure - STRING networks>', 2, fps['STRING Network'], labels)
        elif command == '8':
            WriteNetworkTabs(doc, w)
        elif command == '9':
            WriteCalCluster(doc, w)
        else:
            break

    if command == 'A' or command == 'a':
        WriteCutoff(w)
        fg_fc = WriteFigure.FlowChart(doc, w, '<tag: figure - flow chart>', path.flowchart)
        WriteTable.OverviewTab1(doc, w, '<tag: table - overview statistics - sample>', labels, si)
        WriteTable.OverviewTab2(doc, w, '<tag: table - overview statistics - comparison>', labels, dagr, er)
        WriteAllAnnTabs(doc, w)
        WriteGeneSummery(doc, w)
        WriteAllPathwayTabs(doc, w)
        WriteFigure.STRNetwork(doc, w, '<tag: figure - STRING networks>', 2, fps['STRING Network'], labels)
        WriteNetworkTabs(doc, w)
        WriteCalCluster(doc, w)

    doc.SaveAs(wpath_report.replace('/','\\'))
    doc.Close(False)
    w.Application.Quit()
    del w

def writeXlsReport(path, IOpath, fps, labels):
    import win32com.client as win32
    import ReportLoadFile
    import WriteExcel

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


    xlpath = IOpath.report+'/'+labels.xlsfnm
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

def writeHTMLReport(path, IOpath, fps, labels):
    import os
    import ReportLoadFile
    import WriteHTML

    #---------Get full paths of all needed input files----------
    si = ReportLoadFile.SampleInfo(fps, labels)
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
    tolr = ReportLoadFile.TypeOverlapReport(fps, labels)
    dr = ReportLoadFile.DiffReport(fps, labels)
    dar = ReportLoadFile.DiffAllReport(fps, labels)


    #------------Add Content--------------
    searchengine_gene='http://www.uniprot.org/uniprot/?query=gene%3A$gene+AND+organism%3AMouse&sort=score'
    searchengine_term='http://www.uniprot.org/uniprot/?query=$term+AND+organism%3AMouse&sort=score'
    htmlpath_template = IOpath.template+'/'+labels.htmltemplatefnm
    htmlpath_report = IOpath.report+'/'+labels.htmlreportfnm
    figuredir=htmlpath_report.replace('.html','_figures')
    if not os.path.exists(figuredir):
        os.makedirs(figuredir)
    print 'Writing HTML Report...\n'
    warning='<p class="error">load error!</p>\n'
    HTMLtemplate=open(htmlpath_template,'r')
    HTMLreport=open(htmlpath_report,'w')
    lines = HTMLtemplate.readlines(10000)
    for line in lines:
        line=line.replace('$cutoff',str(labels.cutoff))
        if line[0]!='$':
            HTMLreport.write(line)
        else:
            line=line.replace('\n','')
            line=line.split('-')
            if line[0]=='$figure':
                if line[1]=='flow chart':
                    HTMLreport.write(WriteHTML.FlowChart(path.flowchart,figuredir))
                elif line[1]=='STRING networks':
                    HTMLreport.write(WriteHTML.STRNetwork(2, fps['STRING Network'], labels, figuredir))
                else:
                    HTMLreport.write(warning)
            elif line[0]=='$table':
                if line[1]=='overview statistics':
                    if line[2]=='sample':
                        HTMLreport.write(WriteHTML.OverviewTab1(labels, si))
                    else:
                        HTMLreport.write(WriteHTML.OverviewTab(labels, dagr, er))
                elif line[1]=='annotation':
                    '''if line[2] in labels.overlap:
                        HTMLreport.write(WriteHTML.Ann_Overlap_Badge(gd[line[2]], olr[line[2]],searchengine_gene))
                    '''
                    if line[2] in labels.comp2:
                        HTMLreport.write(WriteHTML.Ann_Badge(gd[line[2]], dgr[line[2]],searchengine_gene))
                    elif line[2] in labels.diff:
                        HTMLreport.write(WriteHTML.Ann_Diff_Badge(gd[line[2]], dr[line[2]], tolr[line[2]], searchengine_gene))
                    else:
                        HTMLreport.write(warning)
                elif line[1]=='pathway':
                    if (line[2] in labels.overlap) or (line[2] in labels.diff):
                        HTMLreport.write(WriteHTML.Pathway2(pd[line[2]], searchengine_gene, searchengine_term))
                    elif line[2] in labels.comp:
                        HTMLreport.write(WriteHTML.Pathway(pd[line[2]], dagr[line[2]],searchengine_gene,searchengine_term))
                    else:
                        HTMLreport.write(warning)
                elif line[1]=='network':
                    if line[2] in labels.comp:
                        HTMLreport.write(WriteHTML.NetworkTable(bnt[line[2]],searchengine_gene))
                    else:
                        HTMLreport.write(warning)
                elif line[1]=='cluster':
                    if line[2] in labels.comp:
                        HTMLreport.write(WriteHTML.CalCluster(pd[line[2]]))
                    else:
                        HTMLreport.write(warning)
                elif line[1]=='summery table':
                    comp = line[2]
                    comp1 = comp + '_tp1'
                    comp2 = comp + '_tp2'
                    HTMLreport.write(WriteHTML.geneSummery(labels, dgr[comp1], dagr[comp1], dgr[comp2], dagr[comp2], tolr[comp1], searchengine_gene))
                else:
                    HTMLreport.write(warning)
            else:
                HTMLreport.write(warning)
    HTMLtemplate.close()
    HTMLreport.close()
