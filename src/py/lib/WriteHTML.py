import re
import math
import shutil

def judgeValue(val):
    if val=='---':
        return(val)
    if float(val)>0.5:
        val = str(1-float(val))
    if float(val)<0.00001:
        return('<0.0001')
    else:
        return(val)

def geomean(num_list):
    return sum(num_list) ** (1.0/len(num_list))

def OverviewTab1(labels, si):

    tablecontent = '<tr>\n<th>' + '' + '</th><th>' + '</th><th>'.join(labels.group) + '</th>\n</tr>\n' # header
    for type in labels.type:
        writeline = '<tr>\n<td>' + type
        for group in labels.group:
            writeline = writeline + '</td><td>' + str(si[type].num[group])
        tablecontent = tablecontent + writeline + '</td>\n</tr>\n'
    print "OverviewTab1: Over"
    return tablecontent


def OverviewTab2(labels, dagr, er):
    def RenameComp(oldcomp):

        fnmitems = oldcomp.split('_')
        newcomp = '%s vs. %s' % (labels.groupmap[fnmitems[1]], labels.groupmap[fnmitems[0]])
        return(newcomp)

    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Group', 'Sum of identified genes', '# Up-regulated genes', '# Down-regulated genes', 'Accuracy', 'False Positive Rate', 'False Negative Rate'])+'</th>\n</tr>\n' # header
    for comp in labels.comp2:
        sumnumber = str(dagr[comp].Num_Gene['Sum'])
        num_up = str(dagr[comp].Num_Gene['Up'])
        num_down = str(dagr[comp].Num_Gene['Down'])
        accuracy = er[comp].CV_IN['Accuracy']
        fpr = er[comp].CV_IN['FPR']
        fnr = er[comp].CV_IN['FNR']
        writeline = '<tr>\n<td>'+'</td><td>'.join([RenameComp(comp), sumnumber, num_up, num_down, accuracy, fpr, fnr])
        tablecontent = tablecontent+writeline+'</td>\n</tr>\n'
    print "OverviewTab for HTML: Over"
    return tablecontent

def Ann_Badge(agd, adgr, stolr, searchengine):

    tablecontent =  '<tr>\n<th>' + '</th><th>'.join(['Change', 'Gene', 'Probability', 'Description'])+'</th>\n</tr>\n' # header
    # 4 columns
    numcols = 4

    genes = agd.MappedGenes
    for gene in genes:
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: [Change, Probability, Fold(log2 level)], ...}
        if adgr.GeneInfo.has_key(gene):
            geneinfo = adgr.GeneInfo[gene]
            change = geneinfo[0]
            search=searchengine.replace('$gene',gene)
            if '+' in change:
                writeline = '<tr class="changed">\n<td>' + change + '</td>' + '<td><a href="%s">'%(search)+gene+'</a></td><td>'+ geneinfo[1]+'</td><td>'+desc
            else:
                writeline = '<tr>\n<td>' + change + '</td>' + '<td><a href="%s">'%(search)+gene+'</a></td><td>'+ geneinfo[1]+'</td><td>'+desc
            if gene in stolr.Genes:
                writeline = '<tr>\n<td><font color="#FF0000">' + change + '</font></td>' + '<td><a href="%s"><font color="#FF0000">'%(search)+gene+'</font></a></td><td><font color="#FF0000">'+ judgeValue(geneinfo[1])+'</font></td><td><font color="#FF0000">'+desc+'</font>'
            tablecontent = tablecontent+writeline+'</td>\n</tr>\n'


    print "Ann Table for HTML ..."
    return tablecontent

def Ann_Diff_Badge(agd, sdr, stolr, searchengine):

    tablecontent = '<tr>\n<th>' + '</th><th>'.join(['Change', 'Gene', 'Probability', 'Description'])+'</th>\n</tr>\n' # header
    # 4 columns
    numcols = 4

    genes = agd.MappedGenes
    for gene in genes:
        desc = agd.Desc[gene]
        # sdr.GeneInfo = {gene1: Probability, ...}
        if sdr.GeneInfo.has_key(gene):
            geneinfo = sdr.GeneInfo[gene]
            search=searchengine.replace('$gene',gene)
            prob = geneinfo[0]
            if prob>0.5:
                change = '+'
                writeline = writeline = '<tr class="changed">\n<td>' + change + '</td>' + '<td><a href="%s">'%(search)+gene+'</a></td><td>'+ geneinfo[1]+'</td><td>'+desc
            else:
                change = '-'
                writeline = '<tr>\n<td>' + change + '</td>' + '<td><a href="%s">'%(search)+gene+'</a></td><td>'+ geneinfo[1]+'</td><td>'+desc
            if gene in stolr.Genes:
                writeline = '<tr>\n<td><font color="#FF0000">' + change + '</font></td>' + '<td><a href="%s"><font color="#FF0000">'%(search)+gene+'</font></a></td><td><font color="#FF0000">'+ judgeValue(geneinfo[1])+'</font></td><td><font color="#FF0000">'+desc+'</font>'
            tablecontent = tablecontent+writeline+'</td>\n</tr>\n'

    print "Ann Table Diff for HTML..."
    return tablecontent

def geneSummery(labels, adgr1, sdagr1, adgr2, sdagr2, stolr, searchengine):

    tablecontent = '\t'.join(['Gene','Change, %s' % labels.typemap['tp1'], 'Probability, %s' % labels.typemap['tp1'],
                              'Change, %s' % labels.typemap['tp2'], 'Probability, %s' % labels.typemap['tp2']]) + '\n'
                              # header

    genelist = adgr1.Genes
    for gene in adgr2.Genes:
        if not(gene in genelist):
            genelist.append(gene)
    for gene in genelist:

        search=searchengine.replace('$gene',gene)
        writeline_head = '<tr class="changed">\n' + '<td><a href="%s">'%(search)+gene+'</a></td>'
        if gene in sdagr1.Genes:
            geneinfo1 = sdagr1.GeneInfo[gene]
            prob1 = geneinfo1[1]
            change1 = geneinfo1[0]
            if '+' in change1:
                writeline = writeline_head + '<td><font color="#0066FF"><B>' + change1 + '</B></font></td><td><font color="#0066FF"><B>' + judgeValue(prob1) + '</B></font></td>'
            else:
                writeline = writeline_head + '<td><font color="#0066FF">' + change1 + '</font></td><td><font color="#0066FF">' + judgeValue(prob1) + '</font></td>'
        else:
            prob1 = '---'
            change1 = '---'
            writeline = writeline_head + '<td>' + change1 + '</td><td>' + judgeValue(prob1) + '</td>'

        if gene in sdagr2.Genes:
            geneinfo2 = sdagr2.GeneInfo[gene]
            prob2 = geneinfo2[1]
            change2 = geneinfo2[0]
            if '+' in change2:
                writeline = writeline + '<td><font color="#9900CC"><B>' + change2 + '</B></font></td><td><font color="#9900CC"><B>' + judgeValue(prob2) + '</B></font></td>'
            else:
                writeline = writeline + '<td><font color="#9900CC">' + change2 + '</font></td><td><font color="#9900CC">' + judgeValue(prob2) + '</font></td>'
        else:
            prob2 = '---'
            change2 = '---'
            line = writeline + '<td>' + change2 + '</td><td>' + judgeValue(prob2) + '</td>'

        if gene in stolr.Genes:
            if '+' in change1:
                writeline = writeline_head + '<td><font color="#FF0000"><B>' + change1 + '</B></font></td><td><font color="#FF0000"><B>' + judgeValue(prob1) + '</B></font></td>'
            else:
                writeline = writeline_head + '<td><font color="#FF0000">' + change1 + '</font></td><td><font color="#FF0000">' + judgeValue(prob1) + '</font></td>'
            if '+' in change2:
                writeline = writeline + '<td><font color="#FF0000"><B>' + change2 + '</B></font></td><td><font color="#FF0000"><B>' + judgeValue(prob2) + '</B></font></td>'
            else:
                writeline = writeline + '<td><font color="#FF0000">' + change2 + '</B></font></td><td><font color="#FF0000">' + judgeValue(prob2) + '</font></td>'


        tablecontent = tablecontent + writeline + '</td>\n</tr>\n'

    print 'Probabilities in all types...'
    return tablecontent


'''def Ann_Limma(agd, adgr, searchengine):
    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Gene', 'P-val, adj.P-val(BH)', 'Description'])+'</th>\n</tr>\n'# header
    # 3 columns
    genes = agd.MappedGenes
    for gene in genes:
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: [Change, Fold/Fold(log2 level), P-val/adj. P-val], ...}
        geneinfo = adgr.GeneInfo[gene]
        change = geneinfo[0]
        search=searchengine.replace('$gene',gene)
        if '+' in change:
            writeline = '<tr class="changed">\n<td><a href="%s">'%(search)+gene+'</a></td><td>'+geneinfo[2]+'</td><td>'+desc
        else:
            writeline = '<tr>\n<td><a href="%s">'%(search)+gene+'</a></td><td>'+geneinfo[2]+'</td><td>'+desc
        tablecontent = tablecontent+writeline+'</td>\n</tr>\n'
    print "Ann Table for HTML ..."
    return tablecontent
'''
'''
def Ann_Overlap_Badge(agd, aolr, searchengine):
    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Gene', 'Probability', 'Description'])+'</th>\n</tr>\n'# header
    # 3 columns
    genes = agd.MappedGenes
    for gene in genes:
        search=searchengine.replace('$gene',gene)
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: Probability, ...}
        geneinfo = aolr.GeneInfo[gene]
        if float(geneinfo)<0.001:
            geneinfo='<0.001'
        else:
            geneinfo= geneinfo
        writeline = '<tr>\n<td><a href="%s">'%(search)+gene+'</a></td><td>'+ geneinfo+'</td><td>'+desc
        tablecontent = tablecontent+writeline+'</td>\n</tr>\n'

    print "Ann Table Overlap for HTML ..."
    return tablecontent
'''
'''
def Ann_Overlap_Limma(agd, aolr, searchengine):
    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Gene', 'P-value', 'Description'])+'</th>\n</tr>\n'# header
    # 3 columns
    genes = agd.MappedGenes
    for gene in genes:
        search=searchengine.replace('$gene',gene)
        desc = agd.Desc[gene]
        # adgr.GeneInfo = {gene1: P-value, ...}
        geneinfo = aolr.GeneInfo[gene]
        if float(geneinfo)<0.001:
            geneinfo='<0.001'
        else:
            geneinfo= geneinfo
        writeline = '<tr>\n<td><a href="%s">'%(search)+gene+'</a></td><td>'+ geneinfo[1]+'</td><td>'+desc
        tablecontent = tablecontent+writeline+'</td>\n</tr>\n'

    print "Ann Table Overlap for HTML ..."
    return tablecontent
'''
def Pathway(apd, sdagr, searchengine, searchengine_term):
    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Annotation Cluster','Term','Associated Gene Symbols','Up-regulated Gene Symbols', 'Down-regulated Gene Symbols', 'P-value', 'Bonferroni', 'FDR'])+'</th>\n</tr>\n' # header
    # 8 cols
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
                    search=searchengine.replace('$gene',gene)
                    if ('+' in change):
                        genes_up = genes_up+'<a href="%s">'%search+gene+'</a>,'
                    else:
                        genes_down = genes_down+'<a href="%s">'%search+gene+'</a>,'
            newgenes=''
            for gene in genes:
                search=searchengine.replace('$gene',gene.strip())
                newgenes+='<a href="%s">'%search+gene.strip()+'</a>, '
            if '~' in term:
                search=searchengine_term.replace('$term',term.split('~')[-1].replace(' ','+'))
                terms='<a href="%s">'%(search)+term+'</a>'
            elif ':' in term:
                search=searchengine_term.replace('$term',term.split(':')[-1].replace(' ','+'))
                terms='<a href="%s">'%(search)+term+'</a>'
            else:
                search=searchengine_term.replace('$term',term.replace(' ','+'))
                terms='<a href="%s">'%(search)+term+'</a>'
            if float(dic_pathway[cluster][term][1])<0.001:
                pvalue='<0.001'
            else:
                pvalue= dic_pathway[cluster][term][1]
            terminfo = '</td><td>'.join([re.sub('\(.*\)','',cluster),terms,newgenes.strip(' ,'), genes_up[:-1], genes_down[:-1],pvalue,dic_pathway[cluster][term][2],dic_pathway[cluster][term][3]])
            if float(dic_pathway[cluster][term][2]) < 0.05:
                terminfo = '<tr class="up_enhance">\n<td>'+terminfo
            elif float(dic_pathway[cluster][term][1]) < 0.05:
                terminfo = '<tr class="down_enhance">\n<td>'+terminfo
            else:
                terminfo = '<tr>\n<td>'+terminfo
            tablecontent = tablecontent+terminfo+'</td>\n</tr>\n'
    print "Pathway Table for HTML ..."
    return tablecontent

def NetworkTable(sbnt, searchengine):
    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Genes', 'Number of Neighbors', 'Thickness' ])+'</th>\n</tr>\n'# header
    #3 columns
    genes=[]
    sbnt_sorted = sorted(sbnt.Info.iteritems(), key = lambda x:x[1][0], reverse = True )
    for i in range(0, len(sbnt_sorted)):
        genes.append(sbnt_sorted[i][0])
    for gene in genes:
        search=searchengine.replace('$gene',gene)
        writeline = '<tr>\n<td><a href="%s">'%(search)+gene+'</a></td><td>'+str(sbnt.Info[gene][0])+'</td><td>'+str(sbnt.Info[gene][1])
        tablecontent = tablecontent+writeline +'</td>\n</tr>\n'
    print "Network Table for HTML ..."
    return tablecontent

def CalCluster(apd):
    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Annotation Cluster', 'Enrichment Score', 'p-value', 'FDR'])+'</th>\n</tr>\n' # header
    # 4 cols
    list_FDR_all = []
    sum_enrich = 0
    for cluster in apd.Cluster:
        sum_enrich += float(apd.Enrich[cluster])
        p = math.exp(float(apd.Enrich[cluster]))
        if float(p)<0.001:
            p_str='<0.001'
        else:
            p_str= str(round(p,3))
        list_FDR = []
        for term in apd.Pathway[cluster]:
            list_FDR.append(float(apd.Pathway[cluster][term][3]))
            list_FDR_all.append(float(apd.Pathway[cluster][term][3]))
        FDR = round(geomean(list_FDR),3)
        tablecontent += '<tr>\n<td>'+'</td><td>'.join([re.sub('\(.*\)','',cluster), apd.Enrich[cluster],p_str,str(FDR)])+'</th>\n</tr>\n'
    FDR_all = geomean(list_FDR_all)
    p_all = math.exp(-sum_enrich)
    if p_all<0.0001:
        p_all_str = '<0.0001'
    else:
        p_all_str = str(round(p_all,3))
    tablecontent += '<tr>\n<td>'+'</td><td>'.join(['overall', str(round(sum_enrich,3)),p_all_str,str(round(FDR_all,3))])+'</th>\n</tr>\n'
    print "Pathway Table for HTML ..."
    return tablecontent

def Pathway2(apd, searchengine , searchengine_term):
    tablecontent = '<tr>\n<th>'+'</th><th>'.join(['Annotation Cluster(Enrichment Score)','Term','Associated Gene Symbols','p-value', 'Bonferroni', 'FDR'])+'</th>\n</tr>\n' # header
    # 6 cols
    dic_pathway = apd.Pathway
    sort_cluster = sorted(dic_pathway.keys(), cmp=lambda x,y : cmp(int(x.split('(')[0]), int(y.split('(')[0])), key=None, reverse=False)
    for cluster in sort_cluster:
        for term in dic_pathway[cluster]:
            dic_pathway[cluster][term][1]
            newgenes=''
            for gene in dic_pathway[cluster][term][0].strip().split(','):
                search=searchengine.replace('$gene',gene.strip())
                newgenes+='<a href="%s">'%search+gene.strip()+'</a>, '
            if '~' in term:
                search=searchengine_term.replace('$term',term.split('~')[-1].replace(' ','+'))
                terms='<a href="%s">'%(search)+term+'</a>'
            elif ':' in term:
                search=searchengine_term.replace('$term',term.split(':')[-1].replace(' ','+'))
                terms='<a href="%s">'%(search)+term+'</a>'
            else:
                search=searchengine_term.replace('$term',term.replace(' ','+'))
                terms='<a href="%s">'%(search)+term+'</a>'
            if float(dic_pathway[cluster][term][1])<0.001:
                pvalue='<0.001'
            else:
                pvalue=dic_pathway[cluster][term][1]
            terminfo = '</td><td>'.join([cluster,terms,newgenes.strip(', '),pvalue,dic_pathway[cluster][term][2],dic_pathway[cluster][term][3]])
            if float(dic_pathway[cluster][term][2]) < 0.05:
                terminfo = '<tr class="up_enhance">\n<td>'+terminfo
            elif float(dic_pathway[cluster][term][1]) < 0.05:
                terminfo = '<tr class="down_enhance">\n<td>'+terminfo
            else:
                terminfo='<tr>\n<td>'+terminfo
            tablecontent = tablecontent+terminfo+'</th>\n</tr>\n'
    print "Pathway Table for HTML ..."
    return tablecontent

#write figures
def FlowChart(fp, figuredir):
    newfp=figuredir+'/'+fp.split('/')[-1]
    shutil.copyfile(fp,newfp)
    newfp=figuredir.split('/')[-1]+'/'+fp.split('/')[-1]
    return '<div class="centerdiv">\n<a href="%s" class="image"><img src="%s" alt="Process Overview" align="center"></a>\n<span align="center">%s</span>\n</div>\n'%(newfp, newfp,'Figure 1: Process Overview:')

def STRNetwork(whichfigure, fps, labels, figuredir):
    def RenameComp(oldcomp):
        if oldcomp == 'overlap1':
            newcomp = 'Overlap1'
        else:
            fnmitems = oldcomp.split('_')
            newcomp = '%s vs. %s' % (labels.groupmap[fnmitems[1]], labels.groupmap[fnmitems[0]])
        return(newcomp)
    #'Edges - the predicted functional links, consist of up to 7 lines: one color for each type of evidence. (Green: "Neighborhood", red: "Gene Fusion", blue: "Cooccurrence", black: "Coexpression", magenta: "Experiments", cyan: "Databases" and orange: "Textmining"). Thicker line denotes a higher prediction confidence.'
    figurecontent=''
    for comp in labels.comp:
        figtitle = '<span align="center">Figure %s. Knowledge-based Networks %s (Yellow nodes: genes from our data set, Blue nodes: genes from external database but not in our dataset)</spa>\n' % (whichfigure, RenameComp(comp))
        subdecs = []
        num_subfig = 1
        figbody=''
        for STRtype in labels.STRtypes:
            fp = fps[comp][STRtype]
            newfp = figuredir+'/'+fp.split('/')[-1]
            shutil.copyfile(fp,newfp)
            newfp = figuredir.split('/')[-1]+'/'+fp.split('/')[-1]
            subtitle = "Figure %d. (%d)" % (whichfigure, num_subfig)
            if STRtype == 'black':
                print("(%d) %s network. " % (num_subfig, 'complete'))
                subdecs.append("(%d) %s network. " % (num_subfig, 'complete'))
            else:
                print("(%d) %s network. " % (num_subfig, STRtype))
                subdecs.append("(%d) %s network. " % (num_subfig, STRtype))
            figbody=figbody+'<div class="centerdiv">\n<a href="%s" class="image"><img src="%s" alt="Process Overview" align="center"></a>\n<span align="center">%s</span>\n</div>\n'%(newfp,newfp,subtitle)
            num_subfig += 1
        #Write Description
        dec= '<span align="center">Figure %s: ' % (whichfigure) + ' '.join(subdecs)+'</span>\n'
        whichfigure+=1
        figurecontent+=figtitle+figbody+dec
    return figurecontent
