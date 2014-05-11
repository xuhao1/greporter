def davidCall(fps, labels):
    def getDict(fps, labels):
        start = 9
        content = open(fps['Probe Map'], 'r').readlines()
        dict = {}
        for i in range(start, len(content)):
            items = content[i].rstrip().split('\t')
            if len(items)>10:
                nuID = items[11]
                enterzID = items[8]
                if (nuID!='') and (enterzID!=''):
                    dict[enterzID] = nuID
        return dict

    from suds.client import Client

    print 'Now Calling DAVID...'
    client = Client('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl')
    client.service.authenticate('cxw2010@mail.ustc.edu.cn')

    for comp in labels.comp:
        print '\tProcessing group: %s' % comp
        dict_ids = getDict(fps, labels)

        inputIDs = ','.join(open(fps['Gene List EnterzID'][comp],'r').read().split('\n'))
        client.service.addList(inputIDs,'ENTREZ_GENE_ID',comp,0)

        # list report
        print '\t\tGenerating list report'
        listReport = client.service.getListReport()
        OUT_LIST = open(fps['DAVID Ann'][comp],'w')
        print >>OUT_LIST, '\t'.join(['EnterzID','Gene Symbol','Description'])
        for row in listReport:
            rowDict = dict(row)
            desc = str(rowDict['name'])
            enterzid = str(rowDict['values'][0])
            nuid = dict_ids[enterzid]
            print >>OUT_LIST, '\t'.join([enterzid, nuid, desc])

        # cluster report
        print '\t\tGenerating cluster report'
        clusterReport = client.service.getTermClusterReport(3,3,3,0.5,50)
        OUT_CLUSTER = open(fps['DAVID Pathway'][comp],'w')

        num = 1
        for row in clusterReport:
            rowDict = dict(row)
            score = str(rowDict['score'])
            print >>OUT_CLUSTER, 'Annotation Cluster %d\tEnrichment score: %s' % (num, score)
            num += 1
            single = rowDict['simpleChartRecords']
            print >>OUT_CLUSTER, '\t'.join(['Category', 'Term', 'PValue', 'Genes', 'Fold Enrichment', 'Bonferroni', 'Benjamini', 'FDR'])
            for row2 in single:
                rowDict2 = dict(row2)
                categoryName = str(rowDict2['categoryName'])
                term = str(rowDict2['termName'])
                pvalue = str(rowDict2['ease'])
                enterzids = str(rowDict2['geneIds']).split(', ')
                genelist = []
                for enterzid in enterzids:
                    genelist.append(dict_ids[enterzid.lower()])
                genes = ', '.join(genelist)
                enrich = str(rowDict2['foldEnrichment'])
                bonferroni = str(rowDict2['bonferroni'])
                benjamini = str(rowDict2['benjamini'])
                fdr = str(rowDict2['afdr'])
                print >>OUT_CLUSTER, '\t'.join([categoryName, term, pvalue, genes, enrich, bonferroni, benjamini, fdr])