from TextProcessing import *
import re
import math
import operator

def geomean(num_list):
    return sum(num_list) ** (1.0/len(num_list))

def OverviewTab(doc, w, tag, labels, dgr, er):
    def RenameComp(oldcomp):
        # eg. "sal_dox_blood" to "Doxorubicin vs. Saline in blood"
        fnmitems = oldcomp.split('_')
        newcomp = '%s vs. %s' % (labels.groupmap[fnmitems[1]], labels.groupmap[fnmitems[0]])
        return(newcomp)

    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Group', 'Sum of identified genes', '# Up-regulated genes', '# Down-regulated genes', 'Accuracy', 'False Positive Rate', 'False Negative Rate'])+'\n' # header
    # 7 columms
    for comp in labels.comp2:
        sumnumber = str(dgr[comp].Num_Gene['Sum'])
        num_up = str(dgr[comp].Num_Gene['Up'])
        num_down = str(dgr[comp].Num_Gene['Down'])
        accuracy = er[comp].CV_IN['Accuracy']
        fpr = er[comp].CV_IN['FPR']
        fnr = er[comp].CV_IN['FNR']
        writeline = '\t'.join([RenameComp(comp), sumnumber, num_up, num_down, accuracy, fpr, fnr])
        tablecontent = tablecontent+writeline+'\n'
    rng.InsertAfter(tablecontent)
    tb = text2table(rng,18,10,'Times New Roman','AutoFit')
    #tb = setTableWidth(tb,[w1, w2, w3, w4])  # in cm
    print "OverviewTab: Over"
    return(tb)

def Ann_Badge(doc, w, tag, agd, adgr):
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Gene', 'Probability', 'Description'])+'\n' # header
    # 3 columns
    rowsup = []
    rowsoverlap = []
    numcols = 3
    countrow = 2
    
    genes = agd.MappedGenes
    for gene in genes:
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: [Change, Probability, Fold(log2 level)], ...}
        geneinfo = adgr.GeneInfo[gene]
        change = geneinfo[0]
        if change.find('+')!=-1:
            rowsup.append(countrow)
        writeline = gene+'\t'+ geneinfo[1]+'\t'+desc
        tablecontent = tablecontent+writeline+'\n'
        countrow  += 1

    rng.InsertAfter(tablecontent)
    tb = text2table(rng,9,8,'Times New Roman','DistributeWidth')
    tb = setTableWidth(tb,[2.4, 3.25, 6.4])  # in cm

    for row in range(2, countrow):
        for col in range(1, numcols+1):
            if row in rowsup:
                tb.Cell(row,col).Range.Font.Bold = True
                tb.Cell(row,col).Range.Font.Underline = True
    print "Ann Table ..."
    return tb

def Ann_Overlap_Badge(doc, w, tag, agd, aolr):
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Gene', 'Probability', 'Description'])+'\n' # header
    # 3 columns
    rowsup = []
    rowsoverlap = []
    numcols = 3
    countrow = 2
    
    genes = agd.MappedGenes
    for gene in genes:
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: Probability, ...}
        geneinfo = aolr.GeneInfo[gene]

        writeline = gene+'\t'+ geneinfo+'\t'+desc
        tablecontent = tablecontent+writeline+'\n'
        countrow  += 1

    rng.InsertAfter(tablecontent)
    tb = text2table(rng,9,8,'Times New Roman','DistributeWidth')
    tb = setTableWidth(tb,[2.4, 3.25, 6.4])  # in cm

    print "Ann Table Overlap..."
    return tb

def Ann_Overlap_Limma(doc, w, tag, agd, aolr):
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Gene', 'P-value', 'Description'])+'\n' # header
    # 3 columns
    rowsup = []
    rowsoverlap = []
    numcols = 3
    countrow = 2
    
    genes = agd.MappedGenes
    for gene in genes:
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: P-value, ...}
        geneinfo = aolr.GeneInfo[gene]

        writeline = gene+'\t'+ geneinfo[1]+'\t'+desc
        tablecontent = tablecontent+writeline+'\n'
        countrow  += 1

    rng.InsertAfter(tablecontent)
    tb = text2table(rng,9,8,'Times New Roman','DistributeWidth')
    tb = setTableWidth(tb,[2.4, 3.25, 6.4])  # in cm

    print "Ann Table Overlap..."
    return tb

def Ann_Limma(doc, w, tag, agd, adgr):
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Gene', 'P-val, adj.P-val(BH)', 'Description'])+'\n' # header
    # 3 columns
    rowsup = []
    rowsoverlap = []
    numcols = 3
    countrow = 2
    
    genes = agd.MappedGenes
    for gene in genes:
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: [Change, Fold/Fold(log2 level), P-val/adj. P-val], ...}
        geneinfo = adgr.GeneInfo[gene]
        change = geneinfo[0]
        if change.find('+')!=-1:
            rowsup.append(countrow)
        writeline = gene+'\t'+geneinfo[2]+'\t'+desc
        tablecontent = tablecontent+writeline+'\n'
        countrow  += 1

    rng.InsertAfter(tablecontent)
    tb = text2table(rng,9,8,'Times New Roman','DistributeWidth')
    tb = setTableWidth(tb,[2.4, 3.25, 6.4])  # in cm

    for row in range(2, countrow):
        for col in range(1, numcols+1):
            if row in rowsup:
                tb.Cell(row,col).Range.Font.Bold = True
                tb.Cell(row,col).Range.Font.Underline = True
    print "Ann Table ..."
    return tb

def Pathway(doc, w, tag, apd, sdagr):
    
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Annotation Cluster','Term','Associated Gene Symbols','Up-regulated Gene Symbols', 'Down-regulated Gene Symbols', 'Pvalue', 'Bonferroni', 'FDR'])+'\n' # header
    # 8 cols
    sigrows1 = []
    sigrows2 = []
    numcols = 8
    countrow = 2
    genelist_cap = []
    genelist = sdagr.Genes
    for gene in sdagr.Genes:
        gene_cap = gene.upper().strip()
        genelist_cap.append(gene_cap)
    dic_pathway = apd.Pathway
    sort_cluster = sorted(dic_pathway.keys(), cmp=lambda x,y : cmp(int(x.split('(')[0]), int(y.split('(')[0])), key=None, reverse=False)  
    for cluster in sort_cluster:
        for term in dic_pathway[cluster]:
            genes = dic_pathway[cluster][term][0].rstrip().split(',')
            genes_up = ''
            genes_down = ''
            for gene in genes:
                gene = gene.strip()
                if gene in genelist_cap:
                    k = genelist_cap.index(gene)
                    change = sdagr.GeneInfo[genelist[k]][0]
                    if (change.find('+')!=-1):
                        genes_up = genes_up + gene + ','
                    else:
                        genes_down = genes_down + gene + ','
            dic_pathway[cluster][term][1]
            terminfo = '\t'.join([re.sub('\(.*\)','',cluster),term,dic_pathway[cluster][term][0], genes_up[:-1], genes_down[:-1],dic_pathway[cluster][term][1],dic_pathway[cluster][term][2],dic_pathway[cluster][term][3]])
            tablecontent = tablecontent+terminfo+'\n'
            if float(dic_pathway[cluster][term][2]) < 0.05:
                sigrows1.append(countrow)
            elif float(dic_pathway[cluster][term][1]) < 0.05:
                sigrows2.append(countrow)
            countrow += 1

    rng.InsertAfter(tablecontent)
    tb = text2table(rng,5,8,'Times New Roman','DistributeWidth')
    # Label Significant terms
    for sigrow1 in sigrows1:
        for col in range(1, numcols+1):
            tb.Cell(sigrow1,col).Range.Font.Color = 0x9900CC #purple
    for sigrow2 in sigrows2:
        for col in range(1, numcols+1):
            tb.Cell(sigrow2,col).Range.Font.Color = 0x0066FF #orange
    tb = setTableWidth(tb,[1.5,3,2.19,2,2,1.5,1.75,1.37])  # in cm
    print "Pathway Table ..."
    return tb

def NetworkTable(doc, w, tag, sbnt):
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Genes', 'Number of Neighbors', 'Thickness' ])+'\n' # header
    #3 columns

    genes=[]
    sbnt_sorted = sorted(sbnt.Info.iteritems(), key = lambda x:x[1][0], reverse = True )
    for i in range(0, len(sbnt_sorted)):
        genes.append(sbnt_sorted[i][0])
    for gene in genes:
        writeline = gene + '\t' + str(sbnt.Info[gene][0]) + '\t' + str(sbnt.Info[gene][1])
        tablecontent = tablecontent + writeline + '\n'
        
    rng.InsertAfter(tablecontent)
    tb = text2table(rng,13,10,'Times New Roman','DistributeWidth')
    tb = setTableWidth(tb,[5, 5, 5])  # in cm

    print "Network Table..."
    return tb

def CalCluster(doc, w, tag, apd):
    
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Annotation Cluster', 'Enrichment Score', 'p-value', 'FDR'])+'\n' # header
    # 4 cols
    
    list_FDR_all = []
    sum_enrich = 0
    for cluster in apd.Cluster:
        sum_enrich += float(apd.Enrich[cluster])
        p = math.exp(float(apd.Enrich[cluster]))
        list_FDR = []
        for term in apd.Pathway[cluster]:
            list_FDR.append(float(apd.Pathway[cluster][term][3]))
            list_FDR_all.append(float(apd.Pathway[cluster][term][3]))
        FDR = round(geomean(list_FDR),3)
        tablecontent += '\t'.join([re.sub('\(.*\)','',cluster), apd.Enrich[cluster], str(round(p,3)), str(FDR)]) + '\n'
    FDR_all = geomean(list_FDR_all)
    p_all = math.exp(-sum_enrich)
    if p_all<0.001:
        p_all_str = '<0.001'
    else:
        p_all_str = str(round(p_all,3))
    tablecontent += '\t'.join(['overall', str(round(sum_enrich,3)),p_all_str,str(round(FDR_all,3))]) + '\n'


    rng.InsertAfter(tablecontent)
    tb = text2table(rng,5,8,'Times New Roman','DistributeWidth')
    tb = setTableWidth(tb,[4,4,4,4])  # in cm
    print "Pathway Table ..."
    return tb
def Pathway2(doc, w, tag, apd):
    
    rng = rmtag(doc,w,tag)
    tablecontent = '\t'.join(['Annotation Cluster(Enrichment Score)','Term','Associated Gene Symbols','Pvalue', 'Bonferroni', 'FDR'])+'\n' # header
    # 6 cols
    sigrows1 = []
    sigrows2 = []
    numcols = 6
    countrow = 2
    dic_pathway = apd.Pathway
    sort_cluster = sorted(dic_pathway.keys(), cmp=lambda x,y : cmp(int(x.split('(')[0]), int(y.split('(')[0])), key=None, reverse=False)  
    for cluster in sort_cluster:
        for term in dic_pathway[cluster]:
            dic_pathway[cluster][term][1]
            terminfo = '\t'.join([cluster,term,dic_pathway[cluster][term][0],dic_pathway[cluster][term][1],dic_pathway[cluster][term][2],dic_pathway[cluster][term][3]])
            tablecontent = tablecontent+terminfo+'\n'
            if float(dic_pathway[cluster][term][2]) < 0.05:
                sigrows1.append(countrow)
            elif float(dic_pathway[cluster][term][1]) < 0.05:
                sigrows2.append(countrow)
            countrow += 1

    rng.InsertAfter(tablecontent)
    tb = text2table(rng,5,8,'Times New Roman','DistributeWidth')
    # Label Significant terms
    for sigrow1 in sigrows1:
        for col in range(1, numcols+1):
            tb.Cell(sigrow1,col).Range.Font.Color = 0x9900CC
    for sigrow2 in sigrows2:
        for col in range(1, numcols+1):
            tb.Cell(sigrow2,col).Range.Font.Color = 0x0066FF
    tb = setTableWidth(tb,[2.91,4.28,3.5,1.5,1.75,1.37])  # in cm
    print "Pathway Table ..."
    return tb