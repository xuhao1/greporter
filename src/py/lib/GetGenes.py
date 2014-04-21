def Sort(fps, labels):
    def sortGenes(fp_input, fp_table, fp_genes, fp_allgenes, threshold):
        
        start = 3 # skip header
        dic_info = {}
        dic_sort = {}
        OUT_table = open(fp_table, 'w')
        OUT_genes = open(fp_genes, 'w')
        OUT_allgenes = open(fp_allgenes, 'w')
        content = open(fp_input, 'r').readlines()

        for i in range(start-1, start):
            print >>OUT_table, content[i].rstrip()

        for i in range(start, len(content)):
            items = content[i].rstrip().split('\t')
            gene = items[1]
            prob = float(items[2])
            if prob <= 0.5:
                prob = 1-prob
            dic_sort[gene] = prob
            dic_info[gene] = content[i].rstrip()
        genes_sort = sorted(dic_sort.keys(), cmp=lambda x,y : cmp(dic_sort[x], dic_sort[y]), key=None, reverse=True)

        for i in range(0, len(genes_sort)):
            print >>OUT_allgenes, genes_sort[i]
        for i in range(0, min(len(content), threshold)):
            print >>OUT_table, dic_info[genes_sort[i]]
            print >>OUT_genes, genes_sort[i]

#-----------------------------------------------------
    print 'Sorting...'
    for comp in labels.comp2:
        print '\tProcessing group: %s' % comp
        sortGenes(fps['Gene Table Unsorted'][comp], fps['Gene Table'][comp], fps['Gene List'][comp], fps['Gene List All'][comp], labels.threshold)
    
def getOverlap_Badge(fps, labels):
    print 'Getting overlaps...'
    for overlap in labels.overlap:
        print '\tProcessing %s: %s' % (overlap, labels.dic_overlap[overlap])
        start = 3
        comps = labels.dic_overlap[overlap].split(' vs ')
        OUT_overlaptable_all = open(fps['Overlap Table All'][overlap], 'w')
        OUT_overlaptable = open(fps['Overlap Table'][overlap], 'w')
        OUT_genes = open(fps['Gene List'][overlap],'w')
        OUT_allgenes = open(fps['Gene List All'][overlap], 'w')
        content1 = open(fps['Gene Table Unsorted'][comps[0]],'r').readlines()
        content2 = open(fps['Gene Table Unsorted'][comps[1]],'r').readlines()

        genelist = []
        dic1_sort = {}
        dic_sort = {}
        for i in range(start, len(content1)):
            items = content1[i].rstrip().split('\t')
            gene = items[1]
            prob = float(items[2])
            if prob <= 0.5:
                prob = 1-prob
            dic1_sort[gene] = prob
        for i in range(start, len(content2)):
            items = content2[i].rstrip().split('\t')
            gene = items[1]
            prob = float(items[2])
            if prob <= 0.5:
                prob = 1-prob
            if dic1_sort.has_key(gene):
                dic_sort[gene] = prob * dic1_sort[gene]
        genes_sort = sorted(dic_sort.keys(), cmp=lambda x,y : cmp(dic_sort[x], dic_sort[y]), key=None, reverse=True)

        print >>OUT_overlaptable_all, '\t'.join(['Gene', 'Probability'])
        print >>OUT_overlaptable, '\t'.join(['Gene', 'Probability'])
        for gene in genes_sort:
            print >>OUT_overlaptable_all, '\t'.join([gene, str(dic_sort[gene])])
            print >>OUT_allgenes, gene
        for i in range(0, min(len(genes_sort),labels.threshold)):
            print >>OUT_overlaptable, '\t'.join([genes_sort[i], str(dic_sort[genes_sort[i]])])
            print >>OUT_genes, genes_sort[i]

def getOverlap_Limma(fps, labels):
    print 'Getting overlaps...'
    for overlap in labels.overlap:
        print '\tProcessing %s: %s' % (overlap, labels.dic_overlap[overlap])
        start = 3
        comps = labels.dic_overlap[overlap].split(' vs ')
        OUT_overlaptable_all = open(fps['Overlap Table All'][overlap], 'w')
        OUT_overlaptable = open(fps['Overlap Table'][overlap], 'w')
        OUT_genes = open(fps['Gene List'][overlap],'w')
        OUT_allgenes = open(fps['Gene List All'][overlap], 'w')
        content1 = open(fps['Gene Table Unsorted'][comps[0]],'r').readlines()
        content2 = open(fps['Gene Table Unsorted'][comps[1]],'r').readlines()

        genelist = []
        dic1_sort = {}
        dic_sort = {}
        for i in range(start, len(content1)):
            items = content1[i].rstrip().split('\t')
            gene = items[0]
            pval = float(items[2])
            if pval <= 0.5:
                pval = 1-pval
            dic1_sort[gene] = pval
        for i in range(start, len(content2)):
            items = content2[i].rstrip().split('\t')
            gene = items[0]
            pval = float(items[6])
            if pval <= 0.5:
                pval = 1-pval
            if dic1_sort.has_key(gene):
                dic_sort[gene] = pval * dic1_sort[gene]
        genes_sort = sorted(dic_sort.keys(), cmp=lambda x,y : cmp(dic_sort[x], dic_sort[y]), key=None, reverse=True)

        print >>OUT_overlaptable_all, '\t'.join(['Gene', 'P-value'])
        print >>OUT_overlaptable, '\t'.join(['Gene', 'Probability'])
        for gene in genes_sort:
            print >>OUT_overlaptable_all, '\t'.join([gene, str(dic_sort[gene])])
            print >>OUT_allgenes, gene
        for i in range(0, min(len(genes_sort),labels.threshold)):
            print >>OUT_overlaptable, '\t'.join([genes_sort[i], str(dic_sort[genes_sort[i]])])
            print >>OUT_genes, genes_sort[i]


def geneSymToAffyID(fps, labels):
    def getDict(fps, labels):
        start = 23
        content = open(fps['Probe Map'], 'r').readlines()
        dict = {}
        for i in range(23, len(content)):
            items = content[i].rstrip().split('","')
            genesym = items[14].split(' /// ')[0]
            if genesym != '---':
                dict[genesym] = items[0].replace('"','')
        return dict

    print 'Translating gene symbols to affymetrix IDs...'
    dict = getDict(fps, labels)
    for comp in labels.comp:
        print '\tProcessing group: %s' % comp
        OUTPUT = open(fps['Gene List AffyID'][comp],'w')
        for line in open(fps['Gene List'][comp],'r').readlines():
            genesym = line.rstrip()
            print >>OUTPUT, dict[genesym]
        
        
        