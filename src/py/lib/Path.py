class DataPaths(object):
    # Paths of data
    def __init__(self, path_work, labels):
        import os
        print 'Loading paths...'

        # Associated Files and Paths...
        self.work = path_work
        self.data = path_work + '/data'

        self.exprdata = '/'.join([path_work, 'data', 'exprdata'])
                        # dir: array/experiments data
        self.annlib = '/'.join([path_work, 'data', 'annlib'])
        self.arff = '/'.join([path_work, 'data', 'arff'])
        self.arff2 = '/'.join([self.arff, '%s_%s' % (labels.method, labels.cutoff)])

        self.flowchart = '/'.join([path_work, 'report', 'flowchart.jpg'])
                         # full path: flowchart figure
        self.genes = '/'.join([path_work, 'data', 'genes_contain',
                              'gene_list_%s_%s'
                              % (labels.method, labels.cutoff)])
                     # dir: lists of genes
        self.genereport = '/'.join([path_work, 'data', 'genes_contain',
                          '%s_table_%s' % (labels.method, labels.cutoff)])
                          # dir: summary tables of genes
        self.ann = '/'.join([path_work, 'data', 'DAVID', 'gene_list_%s_%s'
                            % (labels.method, labels.cutoff)])
                   # dir: DAVID output files - gene list (annotations)
        self.CVreport = '/'.join([path_work, 'data', 'statistics', 'J48',
                                  '%s_%s' % (labels.method, labels.cutoff)])
                        # dir: Results of Cross-Validation
        self.pathway = '/'.join([path_work, 'data', 'DAVID', 'pathway_%s_%s'
                                 % (labels.method, labels.cutoff)])
                       # dir: DAVID output files - clusters
        self.STRnetwork = '/'.join([path_work, 'data', 'STRING', '%s_%s'
                                    % (labels.method, labels.cutoff),
                                       'network', 'jpg_tagged'])
                          # dir: STRING network figures
        self.STRnetwork_raw = '/'.join([path_work, 'data', 'STRING', '%s_%s'
                                    % (labels.method, labels.cutoff),
                                       'network', 'jpg'])
                          # dir: STRING network figures(raw)
        self.STRnetworktable = '/'.join([path_work, 'data', 'STRING', '%s_%s'
                                         % (labels.method, labels.cutoff),
                                            'yedinput'])
                               # dir: STRING network tables
        self.STRING = '/'.join([path_work, 'data', 'STRING', '%s_%s'
                                % (labels.method, labels.cutoff)])
                      # dir: STRING folder
        self.edgelist = '/'.join([self.STRING, 'edgelist'])
                        # dir: STRING subfolder
        self.nodesinfo = '/'.join([self.STRING,'nodes_info'])
                        # dir: STRING subfolder
        self.yedinput = '/'.join([self.STRING,'yedinput'])
                        # dir: STRING subfolder

        if not os.path.isdir(self.data):
            os.makedirs(self.data.replace('/','\\'))
        if not os.path.isdir(self.exprdata):
            os.makedirs(self.exprdata.replace('/','\\'))
        if not os.path.isdir(self.annlib):
            os.makedirs(self.annlib.replace('/','\\'))
        if not os.path.isdir(self.arff):
            os.makedirs(self.arff.replace('/','\\'))
        if not os.path.isdir(self.arff2):
            os.makedirs(self.arff2.replace('/','\\'))
        if not os.path.isdir(self.genes):
            os.makedirs(self.genes.replace('/','\\'))
        if not os.path.isdir(self.genereport):
            os.makedirs(self.genereport.replace('/','\\'))
        if not os.path.isdir(self.ann):
            os.makedirs(self.ann.replace('/','\\'))
        if not os.path.isdir(self.CVreport):
            os.makedirs(self.CVreport.replace('/','\\'))
        if not os.path.isdir(self.pathway):
            os.makedirs(self.pathway.replace('/','\\'))
        if not os.path.isdir(self.STRnetwork):
            os.makedirs(self.STRnetwork.replace('/','\\'))
        if not os.path.isdir(self.STRnetwork_raw):
            os.makedirs(self.STRnetwork_raw.replace('/','\\'))
        if not os.path.isdir(self.STRnetworktable):
            os.makedirs(self.STRnetworktable.replace('/','\\'))
        if not os.path.isdir(self.STRING):
            os.makedirs(self.STRING.replace('/','\\'))
        if not os.path.isdir(self.edgelist):
            os.makedirs(self.edgelist.replace('/','\\'))
        if not os.path.isdir(self.nodesinfo):
            os.makedirs(self.nodesinfo.replace('/','\\'))
        if not os.path.isdir(self.yedinput):
            os.makedirs(self.yedinput.replace('/','\\'))

        for comp in labels.comp:
            for STRtype in labels.STRtypes2:
                path_STRnetwork_sep = '/'.join([self.STRnetwork, STRtype])
                if not os.path.isdir(path_STRnetwork_sep):
                    os.makedirs(path_STRnetwork_sep.replace('/','\\'))



class ProgramPath(object):
    # Paths of files of this reporter program
    def __init__(self, cwd):
        path_program = cwd.replace('\\', '/')
        self.java = '\\'.join([cwd, 'source', 'java', 'src'])
        self.source = path_program + '/source'
        self.colorlabel = '/'.join([path_program, 'source',
                                    'java', 'colorlabel'])
        self.rscript = '/'.join([path_program, 'source', 'R'])


class ExternalPath(object):
    # Paths of external files
    def __init__(self):
        self.R = 'I:/Program Files/R/R-2.15.3/bin'
                 # Where your Rscript.exe lies

class IOPath(object):
    # Paths of I/O of report files
    def __init__(self, path_work):
        self.CEL = ''
        self.template = '/'.join([path_work, 'report', 'template'])
        self.report = '/'.join([path_work, 'report'])


def AllFilesFP(path, labels):
    print 'Loading file paths...'
    # Get full path of all needed input files.
    fps = {}
    # Initialization
    cutoff = labels.cutoff
    fps['Expression Data'] = {}
    fps['Gene List'] = {}
    fps['Gene List All'] = {}
    fps['Gene List AffyID'] = {}
    fps['Gene List EnterzID'] = {}
    fps['Gene Table'] = {}
    fps['Gene Table Unsorted'] = {}
    fps['CV Report'] = {}
    fps['DAVID Ann'] = {}
    fps['DAVID Pathway'] = {}
    fps['STRING Network'] = {}
    fps['STRING Network Table'] = {}
    fps['Arff'] = {}
    fps['Probe Map'] = '%s/%s' % (path.annlib, labels.probemap)
    fps['Overlap Table All'] = {}
    fps['Overlap Table'] = {}
    fps['Diff Table All'] = {}
    fps['Diff Table'] = {}
    for type in labels.type:
        fps['Expression Data'][type] = '%s/expr_%s.txt' % (path.exprdata, type)
    for overlap in labels.overlap:
        fps['Overlap Table All'][overlap] = '%s/%s_%s_all.txt' \
                                   % (path.genereport, overlap, cutoff)
        fps['Overlap Table'][overlap] = '%s/%s_%s.txt' \
                                   % (path.genereport, overlap, cutoff)
    for diff in labels.diff:
        fps['Diff Table All'][diff] = '%s/%s_%s_all.txt' \
                                   % (path.genereport, diff, cutoff)
        fps['Diff Table'][diff] = '%s/%s_%s.txt' \
                                   % (path.genereport, diff, cutoff)

    for comp in labels.comp2:
        #fps['Expression Data'][comp] = '%s/expr_%s.txt' % (path.exprdata,comp)
        fps['Gene Table'][comp] = '%s/%s_%s_selected.txt'\
                                   % (path.genereport, comp, cutoff)
                                   #grp1_grp2_tp1_0.005_selected.txt
        fps['Gene Table Unsorted'][comp] = '%s/%s_%s_selected_unsorted.txt'\
                                   % (path.genereport, comp, cutoff)
                                   #grp1_grp2_tp1_0.005_selected_unsorted.txt
        fps['CV Report'][comp] = '%s/%s_%s_CV-in.txt' \
                                 % (path.CVreport, comp, cutoff)
        fps['Arff'][comp] = '%s/%s_%s/%s_%s_filtered.arff' \
                            % (path.arff, labels.method, cutoff, comp, cutoff)
    for comp in labels.comp:
        fps['Gene List'][comp] = '%s/%s_%s_genes.txt' \
                                 % (path.genes, comp, cutoff)
                                #e.g. grp1_grp2_tp1_0.005_genes.txt
        fps['Gene List All'][comp] = '%s/%s_%s_allgenes.txt' \
                                     % (path.genes, comp, cutoff)
                                     #e.g. grp1_grp2_tp1_0.005_allgenes.txt
        fps['Gene List AffyID'][comp] = '%s/%s_%s_genes_affyid.txt' \
                                        % (path.genes, comp, cutoff)
        fps['Gene List EnterzID'][comp] = '%s/%s_%s_genes_enterzid.txt' \
                                        % (path.genes, comp, cutoff)
        fps['DAVID Ann'][comp] = '%s/%s_%s_genelist.txt' \
                                 % (path.ann, comp, cutoff)
                                 #grp1_grp2_tp1_0.005_genelist.txt
        fps['DAVID Pathway'][comp] = '%s/%s_%s_ptw.txt' \
                                     % (path.pathway, comp, cutoff)
                                     #grp1_grp2_tp1_0.005_ptw.txt
        fps['STRING Network Table'][comp] = '%s/%s_%s-edgelist.csv' \
                                 % (path.STRnetworktable, comp, cutoff)
                                 #grp1_grp2_tp1_0.005-edgelist.csv
        fps['STRING Network'][comp] = {}
        for STRtype in labels.STRtypes2:
            fps['STRING Network'][comp][STRtype] = '%s/%s/%s_%s_%s.jpg' \
                           % (path.STRnetwork, STRtype, comp, cutoff, STRtype)
            #grp1_grp2_tp1_0.005_cooccurence.jpg
    return(fps)
