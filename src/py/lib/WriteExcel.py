def AllGenes(wb, comp, labels, sdagr):
    def RenameComp(oldcomp):
        fnmitems = oldcomp.split('_')
        newcomp = '%s vs. %s' % (labels.groupmap[fnmitems[1]], labels.groupmap[fnmitems[0]])
        return(newcomp)

    sht = wb.Worksheets.Add()
    sht.Name= RenameComp(comp)
    sht.Activate()
    sht.Cells(1,1).Value = 'All the Identified Genes in %s group' % RenameComp(comp)
    sht.Cells(2,1).Value = 'Gene Name'
    sht.Cells(2,2).Value = 'Change'
    sht.Cells(2,3).Value = 'Probability'
    for (i,gene) in enumerate(sdagr.Genes):
        info = sdagr.GeneInfo[gene]
        sht.Cells(i+3,1).Value = gene
        sht.Cells(i+3,2).Value = info[0]
        sht.Cells(i+3,3).Value = info[1]
