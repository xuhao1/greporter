import re

def OverlapReport(fps, labels):
    '''
    data structure of dgr:
    olr = {comp1:aolr1, comp2:aolr2 ...}   eg. {'sal_dox_blood':aolr1}...
    aolr.Genes = [gene1, gene2, ...]
    aolr.GeneInfo = {gene1: Probability, ....}
    '''   
    class AOverlapReport(object):
        def __init__(self, fp):
            def Get3Figures(val):
                newval = "%.5f" % float(val)
                return(str(newval))
                        
            def ParseReportTable(fp):
                RTIN = open(fp, 'r')
                content = RTIN.readlines()
                genes = []
                rt = {}
                
                start = 1
                for i in range(start, len(content)):
                    items = content[i].rstrip().split('\t')
                    gene = items[0]
                    prob = items[1]

                    rt[gene] = Get3Figures(prob)
                    if gene not in genes:
                        genes.append(gene)
                return(rt, genes)
            # Now create the struct
            (rt, genes) =  ParseReportTable(fp)
            self.Genes = genes
            self.GeneInfo = rt
    # Now create olr struct
    olr = {}
    for overlap in labels.overlap:
        fp = fps['Overlap Table'][overlap]
        olr[overlap] = AOverlapReport(fp)
    return(olr)

def OverlapAllReport(fps, labels):
    '''
    data structure of dgr:
    olar = {comp1:aolr1, comp2:aolr2 ...}   eg. {'sal_dox_blood':aolr1}...
    solar.Genes = [gene1, gene2, ...]
    solar.GeneInfo = {gene1: Probability ...}
    '''   
    class SingleAllOverlapReport(object):
        def __init__(self, fp):
            def Get3Figures(val):
                newval = "%.5f" % float(val)
                return(str(newval))
                        
            def ParseReportTable(fp):
                RTIN = open(fp, 'r')
                content = RTIN.readlines()
                genes = []
                rt = {}
                
                start = 1
                for i in range(start, len(content)):
                    items = content[i].rstrip().split('\t')
                    gene = items[0]
                    prob = items[1]

                    rt[gene] = Get3Figures(prob)
                    if gene not in genes:
                        genes.append(gene)
                return(rt, genes)
            # Now create the struct
            (rt, genes) =  ParseReportTable(fp)
            self.Genes = genes
            self.GeneInfo = rt
    # Now create olar struct
    olar = {}
    for overlap in labels.overlap:
        fp = fps['Overlap Table All'][overlap]
        olar[overlap] = SingleAllOverlapReport(fp)
    return(olar)

def DiffGeneReport_Badge(fps, labels):
    '''
    data structure of dgr:
    dgr = {comp1:adgr1, comp2:adgr2 ...}   eg. {'sal_dox_blood':adgr1}...
    adgr.Genes = [gene1, gene2, ...]
    adgr.Num_Gene = {'Sum':***, 'Up':***, 'Down':*** }      the number of identified genes
    adgr.GeneInfo = {gene1: [Change, Probability, Fold(log2 level)]}
    '''   
    class ADiffGeneReport(object):
        def __init__(self, fp):
            def Get3Figures(val):
                newval = "%.5f" % float(val)
                return(str(newval))
                        
            def ParseReportTable(fp):
                RTIN = open(fp, 'r')
                content = RTIN.readlines()
                num_up = 0
                num_down = 0
                sumnumber = 0
                genes = []
                rt = {}
                
                start = 1
                for i in range(start, len(content)):
                    items = content[i].rstrip().split('\t')
                    gene = items[1]
                    foldchange = items[3]
                    prob = items[2]
                    change = items[0]
                    # gene: [Change, Probability, Fold(log2 level)]
                    rt[gene] = [change, Get3Figures(prob), Get3Figures(foldchange)]
                    if gene not in genes:
                        genes.append(gene)
                    if change.find('-') != -1:
                        num_down += 1
                    else:
                        num_up += 1
                sumnumber = num_up+num_down
                return(rt, genes, num_up, num_down, sumnumber)
            # Now create the struct
            (rt, genes, num_up, num_down, sumnumber) =  ParseReportTable(fp)
            self.Genes = genes
            self.Num_Gene = {'Sum':sumnumber, 'Up':num_up, 'Down':num_down}
            self.GeneInfo = rt
    # Now create dgr struct
    dgr = {}
    for comp in labels.comp2:
        fp = fps['Gene Table'][comp]
        dgr[comp] = ADiffGeneReport(fp)
    return(dgr)

def DiffGeneReport_Limma(fps, labels):
    '''
    data structure of adgr:
    dgr = {comp1:adgr1, comp2:adgr2 ...}   eg. {'sal_dox_blood':adgr1}...
    adgr.Genes = [gene1, gene2, ...]
    adgr.Num_Gene = {'Sum':***, 'Up':***, 'Down':*** }      the number of identified genes
    adgr.GeneInfo = {gene1: [Change, Fold/Fold(log2 level), P-val/adj. P-val]}
    '''   
    class ADiffGeneReport(object):
        def __init__(self, fp):
            def Get4Figures(val):
                parts = val.split('e')
                figures = "%.4f" % float(parts[0])
                if val.find('e') != -1:
                    newval = str(figures)+'E'+parts[1]
                else:
                    newval = str(figures)
                return(newval)
                        
            def ParseReportTable(fp):
                RTIN = open(fp, 'r')
                rt = {}
                num_up = 0
                num_down = 0
                sumnumber = 0
                genes = []
                RTIN.readline()  # Skip the header
                for line in RTIN:
                    # 0:ID, 1:Fold Change, 2:Fold Change(log2 level), 3:Expr1, 4:Expr2, 5:t, 6:P.Value, 7:adj.P.Val, 8:B
                    items = line.rstrip().split('\t')
                    if items[0] not in genes:
                        genes.append(items[0])
                        if float(items[2]) < 1:
                            change = '-'
                            num_down += 1
                        else:
                            change = '+'
                            num_up += 1
                    # gene: [Change, Fold/Fold(log2 level), P-val/adj.P-val]
                    rt[items[0]] = [change, Get4Figures(items[1])+','+Get4Figures(items[2]), Get4Figures(items[6])+','+Get4Figures(items[7])]
                sumnumber = num_up+num_down
                return(rt, genes, num_up, num_down, sumnumber)
            # Now create the struct
            (rt, genes, num_up, num_down, sumnumber) =  ParseReportTable(fp)
            self.Genes = genes
            self.Num_Gene = {'Sum':sumnumber, 'Up':num_up, 'Down':num_down}
            self.GeneInfo = rt
    # Now create dgr struct
    dgr = {}
    for comp in labels.comp:
        fp = fps['Gene Table'][comp]
        dgr[comp] = ADiffGeneReport(fp)
    return(dgr)

def DiffAllGeneReport_Badge(fps, labels):
    '''
    data structure of dagr:
    dagr = {comp1:adgr1, comp2:adgr2 ...}   eg. {'TP0_TP1':adgr1}...
    sdagr.Genes = [gene1, gene2, ...]
    sdagr.Num_Gene = {'Sum':***, 'Up':***, 'Down':*** }      the number of identified genes
    sdagr.GeneInfo = {gene1: [Change, Probability, Fold(log2 level)]}
    '''   
    class SingleDiffAllGeneReport(object):
        def __init__(self, fp):
            def Get3Figures(val):
                newval = "%.5f" % float(val)              
                return(str(newval))
                        
            def ParseReportTable(fp):                          
                RTIN = open(fp, 'r')
                content = RTIN.readlines()
                num_up = 0
                num_down = 0
                sumnumber = 0
                genes = []
                rt = {}
                
                start = 3
                for i in range(start, len(content)):
                    items = content[i].rstrip().split('\t')
                    gene = items[1]
                    foldchange = items[3]
                    prob = items[2]
                    change = items[0]
                    # gene: [Change, Probability, Fold(log2 level)]
                    rt[gene] = [change, Get3Figures(prob), Get3Figures(foldchange)]
                    if gene not in genes:
                        genes.append(gene)
                    if change.find('-') != -1:
                        num_down += 1
                    else:
                        num_up += 1
                sumnumber = num_up+num_down
                return(rt, genes, num_up, num_down, sumnumber)
            # Now create the struct
            (rt, genes, num_up, num_down, sumnumber) =  ParseReportTable(fp)
            self.Genes = genes
            self.Num_Gene = {'Sum':sumnumber, 'Up':num_up, 'Down':num_down}
            self.GeneInfo = rt
    # Now create dgr struct
    dagr = {}
    for comp in labels.comp2:
        fp = fps['Gene Table Unsorted'][comp]
        dagr[comp] = SingleDiffAllGeneReport(fp)
    return(dagr)

def DiffAllGeneReport_Limma(fps, labels):
    '''
    data structure of adgr:
    dagr = {comp1:adgr1, comp2:adgr2 ...}   eg. {'sal_dox_blood':adgr1}...
    sdagr.Genes = [gene1, gene2, ...]
    sdagr.Num_Gene = {'Sum':***, 'Up':***, 'Down':*** }      the number of identified genes
    sdagr.GeneInfo = {gene1: [Change, Fold/Fold(log2 level), P-val/adj. P-val]}
     ''' 
    class SingleDiffAllGeneReport(object):
        def __init__(self, fp):
            def Get4Figures(val):
                parts = val.split('e')
                figures = "%.4f" % float(parts[0])
                if val.find('e') != -1:
                    newval = str(figures)+'E'+parts[1]
                else:
                    newval = str(figures)                
                return(newval)
                        
            def ParseReportTable(fp):                          
                RTIN = open(fp, 'r')
                rt = {}
                num_up = 0
                num_down = 0
                sumnumber = 0
                genes = []
                RTIN.readline()  # Skip the header
                for line in RTIN:
                    # 0:ID, 1:Fold Change, 2:Fold Change(log2 level), 3:Expr1, 4:Expr2, 5:t, 6:P.Value, 7:adj.P.Val, 8:B
                    items = line.rstrip().split('\t')
                    if items[0] not in genes:
                        genes.append(items[0])
                        if float(items[2]) < 1:
                            change = '-'
                            num_down += 1
                        else:
                            change = '+'
                            num_up += 1
                    # gene: [Change, Fold/Fold(log2 level), P-val/adj.P-val]
                    rt[items[0]] = [change, Get4Figures(items[1])+','+Get4Figures(items[2]), Get4Figures(items[6])+','+Get4Figures(items[7])]
                sumnumber = num_up+num_down
                return(rt, genes, num_up, num_down, sumnumber)
            # Now create the struct
            (rt, genes, num_up, num_down, sumnumber) =  ParseReportTable(fp)
            self.Genes = genes
            self.Num_Gene = {'Sum':sumnumber, 'Up':num_up, 'Down':num_down}
            self.GeneInfo = rt
    # Now create dgr struct
    dagr = {}
    for comp in labels.comp:
        fp = fps['Gene Table Unsorted'][comp]
        dagr[comp] = SingleDiffAllGeneReport(fp)
    return(dagr)

def EvalReport(fps, labels):
    '''
    data structure of er:
    er = {comp1:aer1, comp2:aer2 ...}
    aer.CV_IN = ['Accuracy': ***, 'FPR': ***, 'FNR': ***]
    '''   
    class AEvalReport(object):
        def __init__(self, fp):                    
            def ParseCVReportTable(fp):                          
                IN = open(fp, 'r')
                p_pred = re.compile(r'\s*\w+\s*\w:(\w)\s*\w:(\w)\s*.*')
                content = IN.readlines()
                num = 0
                tp = 0
                fp = 0
                tn = 0
                fn = 0
                for line in content:
                    if p_pred.match(line.rstrip()):
                        pred = p_pred.match(line.rstrip()).groups()
                        num += 1   
                        if pred[0] == 'n':
                            if pred[1] == 'n':
                                tn += 1
                            else:
                                fp += 1
                        else:
                            if pred[1] == 'p':
                                tp += 1
                            else:
                                fn += 1
                accuracy = float(tp+tn)/float(num)
                fpr = float(fp)/float(tp+fp)
                fnr = float(fn)/float(tn+fn)
                return(str("%.3f" % accuracy), str("%.3f" % fpr), str("%.3f" % fnr))
            # Now create the struct
            (accuracy, fpr, fnr) = ParseCVReportTable(fp)
            self.CV_IN = {'Accuracy':accuracy, 'FPR':fpr, 'FNR':fnr}
    # Now create er struct
    er = {}
    for comp in labels.comp2:
        fp = fps['CV Report'][comp]
        er[comp] = AEvalReport(fp)
    return(er)

def GeneDatabase(fps, labels):        
    '''
    data structure of gd:
    gd = {comp1:agd, comp2:agd ...}   eg. {'TP0_TP1': agd1}
    agd.MappedGenes = [gene1, gene2, ...]   # genes that annotated by DAVID
    agd.Desc = {gene1: full gene name}
    '''  
    class AGeneDatabase(object):
        def __init__(self, fp_genelist, fp_ann):
            '''def getGenes(fp_genelist):
                genes = []
                GENES = open(fp_genelist, 'r')
                for line in GENES:
                    gene = line.rstrip()
                    genes.append(gene)
                return(genes)    '''                   
            def ParseAnn(fp_ann):
                ANN = open(fp_ann,'r')
                ANN.readline()  # Skip the header
                ann = {}
                mappedgenes = []
                for line in ANN:
                    items = line.rstrip().split('\t')
                    if items[1] != '':
                        ann[items[1]] = items[2]
                        mappedgenes.append(items[1])
                return(ann, mappedgenes)
            (ann, mappedgenes) = ParseAnn(fp_ann)
            self.MappedGenes = mappedgenes
            self.Desc = ann
    # Now create gd structure
    gd = {}
    for comp in labels.comp:
        fp_genelist = fps['Gene List'][comp]
        fp_ann = fps['DAVID Ann'][comp]
        gd[comp] = AGeneDatabase(fp_genelist, fp_ann)
    return(gd)
            
def PathwayDatabase(fps, labels):
    '''
    data structure of pd:
    pd = {comp1:apd1, comp2:apd2 ...}   eg. {'sal_dox_blood': apd1}
    apd.Cluster = [cluster1, cluster2, ...]
    apd.Term = [term1, term2, ...]
    apd.Pathway = {[Cluster]:{Term:[genes,Pvalue, Bonferroni, FDR]...}}
    apd.Enrich = {[cluster]:enrichment score 1, ...}
    '''
    class APathwayDatabase(object):
        def __init__(self, fp):
            def ParsePathway(fp):
                def Get3Figures(val):
                    parts = val.split('E')
                    figures = "%.3f" % float(parts[0])
                    if val.find('E') != -1:
                        newval = str(figures)+'E'+parts[1]
                    else:
                        newval = str(figures)         
                    return(newval)
                                
                clusters = []
                terms = []
                dic_pathway = {}
                dict_enrich = {}
                # load in pathway files
                PATHWAY = open(fp, 'r')
                ''' Original Format:
                0-Annotation Cluster n, 1- Enrichment Score: x
                0-Category,1-Term,2-PValue,3-Genes,4-Fold Enrichment,5-Bonferroni,6-Benjamini,7-FDR
                '''
                for readline in PATHWAY:
                    items = readline.rstrip().split('\t')
                    if len(items) == 2:
                        enrich = Get3Figures(items[1].replace('Enrichment score: ',''))
                        curcluster = '%s ( %s )'%(items[0].replace('Annotation Cluster ',''), enrich)
                        dic_pathway[curcluster] = {}
                        dict_enrich[curcluster] = enrich
                        clusters.append(curcluster)
                    elif len(items) == 8:
                        if items[0] == 'Category':
                            continue
                        #Term:[genes,Pvalue, Bonferroni, FDR]
                        dic_pathway[curcluster][items[1]] = [items[3], Get3Figures(items[2]), Get3Figures(items[5]), Get3Figures(items[7])]
                        if not items[1] in terms:
                            terms.append(items[1])                 
                return (dic_pathway, clusters, terms, dict_enrich)

            (dic_pathway, clusters, terms, dict_enrich) = ParsePathway(fp)
            self.Cluster = clusters
            self.Term = terms
            self.Pathway = dic_pathway
            self.Enrich = dict_enrich
    # Now create pd structure
    pd = {}
    for comp in labels.comp:
        fp = fps['DAVID Pathway'][comp]
        pd[comp] = APathwayDatabase(fp)
    return(pd)

def NetworkTable(fps, labels):
    '''
    data structure of bnt:
        bnt = {comp1: sbnt1, comp2: sbnt2, ...}
    data structure of sbnt:
        sbnt.Genes = [gene1, gene2, ...]
        sbnt.Info = {gene1:[numneighbor, thickness], gene2:[numneighbor, thickness], ...}
    '''
    class SingleNetworkTable(object):
        def __init__(self, fp):
            def ParseNetworkTable(fp):
                NT = open(fp, 'r')
                genes = []
                nt = {}
                conf={}
                neinum={}
                for line in NT:
                    #0:gene1 1:gene2 ... 12:confidence
                    items = line.rstrip().split(',')
                    #gene1
                    if items[0] not in genes:
                        genes.append(items[0])
                        neinum[items[0]] = 1
                        conf[items[0]] = []
                    else:
                        neinum[items[0]] += 1                       
                    conf[items[0]].append(float(items[11]))
                    #gene2
                    if items[1] not in genes:
                        genes.append(items[1])
                        neinum[items[1]] = 1
                        conf[items[1]] = []
                    else:
                        neinum[items[1]] += 1                       
                    conf[items[1]].append(float(items[11]))
                for gene in genes:
                    nt[gene] = []
                for gene in genes:
                    nt[gene].append(neinum[gene])
                    nt[gene].append("%.3f" % (sum(conf[gene])/len(conf[gene])))
                return(nt, genes)
            #create the abnt structure
            (nt, genes) = ParseNetworkTable(fp)
            self.Genes = genes
            self.Info = nt
    #create the bnt structure
    bnt = {}
    for comp in labels.comp:
        fp = fps['STRING Network Table'][comp]
        bnt[comp] = SingleNetworkTable(fp)
    return(bnt)

