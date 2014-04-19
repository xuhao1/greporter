def Limma(path, expath, progpath, fps, labels):
    import os
    os.chdir(expath.R)
    print 'Doing differential-expression analysis...'
    for comp in labels.comp2:
        print '\tProcessing group: %s' % comp
        groups = comp.split('_')
        cmd = 'Rscript.exe "%s\\limma.R" "%s" "%s" "%f" "%d" "%s" "%s" "%s" "%s" "%s"' % (progpath.rscript.replace('/', '\\'), groups[0], groups[1], labels.cutoff, labels.threshold, fps['Expression Data'][comp], fps['Gene List'][comp], fps['Gene List All'][comp], fps['Gene Table'][comp], fps['Gene Table Unsorted'][comp])
        os.system(cmd)
    
    