def RMA(path, expath, progpath, labels):
    import os
    os.chdir(expath.R)
    cmd = 'Rscript.exe "%s\\rma.R" "%s"' % (progpath.rscript.replace('/', '\\'), path.data)
    os.system(cmd)
    
    