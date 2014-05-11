class Labels(object):
    # All needed lables
    def __init__(self, method_input):
        print 'Loading labels...'
        self.species = 'Mus musculus'
        self.taxid = '10090'
        self.array = 'MouseRef-8_V2'
        self.probemap = 'MouseRef-8_V2_0_R3_11278551_A.txt'
        self.group = {'grp1', 'grp2', 'grp3', 'grp4'}
        self.groupmap = {'grp1': 'Untreated', 'grp2': 'Drug',
                         'grp3': 'Radiation', 'grp4': 'Radiation&Drug'}
        self.shortgroupmap = {'grp1': 'Un', 'grp2': 'Drug',
                         'grp3': 'Rad', 'grp4': 'Rad&Drug'}
        self.type = {'tp1', 'tp2'}
        self.typemap = {'tp1': 'Blood', 'tp2': 'Tissue'}

        self.templatefnm = 'template_badge.doc'
        self.reportfnm = 'report_badge.doc'
        self.xlsfnm = 'report_badge.xls'

        if method_input == 'L':
            self.method = 'limma'
        else:
            self.method = 'badge'
        self.cutoff = 0.001
        self.threshold = 200
        self.overlap = []
        self.dic_overlap = {}
        self.diff = ['diff1_tp1', 'diff1_tp2']
        self.dic_diff = {'diff1_tp1': 'grp3_grp4_tp1 - grp1_grp2_tp1',
                         'diff1_tp2': 'grp3_grp4_tp2 - grp1_grp2_tp2'}
        self.comp = ['grp1_grp2_tp1', 'grp1_grp3_tp1', 'grp1_grp4_tp1',
                     'grp3_grp4_tp1', 'diff1_tp1',
                     'grp1_grp2_tp2', 'grp1_grp3_tp2', 'grp1_grp4_tp2',
                     'grp3_grp4_tp2', 'diff1_tp2']
                     # comparisons
        self.comp2 = ['grp1_grp2_tp1', 'grp1_grp3_tp1',
                      'grp1_grp4_tp1', 'grp3_grp4_tp1',
                      'grp1_grp2_tp2', 'grp1_grp3_tp2',
                      'grp1_grp4_tp2', 'grp3_grp4_tp2']
                      # comparisons excluding diffs and overlaps
        self.comp3 = ['grp1_grp2', 'grp1_grp3', 'grp1_grp4', 'grp3_grp4']
        self.STRtypes = ['neighborhood', 'coexpression', 'cooccurrence',
                         'databases', 'experiments', 'genefusion',
                         'textmining', 'black']
        self.STRtypes2 = ['neighborhood', 'coexpression', 'cooccurrence',
                          'databases', 'experiments', 'genefusion',
                          'textmining', 'complete', 'black']
                          # excluding 'complete'
