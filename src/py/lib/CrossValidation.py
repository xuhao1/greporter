def exprToArff(path, fps, labels):
    import random
    def readExprData(fp_expr):
        EXPRIN = open(fp_expr, 'r')
        
        genes = []
        chips = []
        expr = {}

        lines = EXPRIN.readlines()
        chips = lines[0].rstrip().split('\t')
        for i in range(1, len(lines)):
            items = lines[i].rstrip().split('\t')
            gene = items[0]
            genes.append(gene)
            expr[gene] = {}
            for (i,chip) in enumerate(chips):
                expr[gene][chip] = items[i+1]
        
        return(chips, genes, expr)

    def shuffleChips(chips, comp, fp_pl):
        PLOUT = open(fp_pl, 'w')
        phenolist = {}

        comp_items = comp.split('_')
        random.shuffle(chips)
        for chip in chips:
            items = chip.split('.')
            if items[0].find(comp_items[0])!=-1:
                temp = comp_items[0]
            else:
                temp = comp_items[1]
            if temp == comp_items[0]:
                pheno = 'n'
            elif temp == comp_items[1]:
                pheno = 'p'
            phenolist[chip] = pheno
            print >>PLOUT, chip+','+pheno
        return(chips, phenolist)

    def writeArff(chips, genes, expr, phenolist, comp, fp_arff):
        ARFF = open(fp_arff, 'w')

        print >>ARFF, '@relation %s\n' % (comp)    # write relation header
        
        # write gene attributes
        for gene in genes:
            print >>ARFF, '@attribute %s numeric' % (gene)
        print >>ARFF, '@attribute Phenotype {p,n}\n'

        print >>ARFF, '@data'
        for chip in chips:
            writeline = ''
            for gene in genes:
                writeline = writeline+expr[gene][chip]+','
            writeline = writeline+phenolist[chip]
            print >>ARFF, writeline

    print 'Generating learning arff files...'
    for comp in labels.comp2:
        print '\tProcessing group: %s' % comp
        fp_expr = path.exprdata + '/expr_%s.txt' % comp
        fp_arff = path.arff + '/%s.arff' % comp
        fp_pl = path.arff + '/%s_learn_phenotype.csv' % comp
        (chips, genes, expr) = readExprData(fp_expr)
        (chips, phenolist) = shuffleChips(chips, comp, fp_pl)
        writeArff(chips, genes, expr, phenolist, comp, fp_arff)

def syncArffFeatures(path, fps, labels):
    import re
    def SyncFeatures(fp_features, fp_in, fp_out):
        features = []
        FEATUREF = open(fp_features, 'r')
        for line in FEATUREF:
            features.append(line.rstrip())

        pattr=re.compile(r'@attribute (.*) ({.*}||numeric)')
        FIN = open(fp_in, 'r')
        FOUT = open(fp_out,'w')
        featuresall = []
        featureposition = []

        while True:
            line = FIN.readline().rstrip()
            if not line:break
            print >>FOUT, line
        print >>FOUT, ''

        countfeature = 0
        while True:
            line = FIN.readline().rstrip()
            if pattr.match(line):
                att = pattr.match(line).groups()[0]
                featuresall.append(att)
                if att in features or att == 'Phenotype':
                    featureposition.append(countfeature)
                    print >>FOUT, line
                countfeature += 1
            else:
                break
        print >>FOUT, line
        line = FIN.readline().rstrip()
        print >>FOUT, line

        #print Data
        while True:
            line = FIN.readline().rstrip()
            if not line:break
            values = line.rstrip().split(',')
            out=[]
            for i in featureposition:
                out.append(values[i])
            print >>FOUT, ','.join(out)

    print 'Generating arff files...'
    for comp in labels.comp2:
        print '\tProcessing group: %s' % comp
        fp_features = fps['Gene List All'][comp]
        fp_in = '%s/%s.arff' % (path.arff, comp)
        fp_out = fps['Arff'][comp]
        SyncFeatures(fp_features, fp_in, fp_out)

def callWeka(fps, labels):
    import os
    print 'Doing cross validation...'
    for comp in labels.comp2:
        print '\tGroup: %s' % comp
        os.system('java weka.classifiers.trees.J48 -t "%s" -p 0 > "%s"' % (fps['Arff'][comp].replace('/','\\'), fps['CV Report'][comp].replace('/','\\')))
        