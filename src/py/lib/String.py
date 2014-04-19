def stringCall(path, fps, labels):
    import urllib
    print 'Calling STRING...'
    for comp in labels.comp:
        print '\tProcessing group: %s' % comp
        genes = open(fps['Gene List'][comp],'r').read()
        genelist = genes.split('\n')
        listinput = '%0D'.join(genelist)
        url = 'http://string-db.org/api/psi-mi-tab/interactionsList?identifiers=%s&species=%s&required_score=400&additional_network_nodes=0&limit=0' % (listinput, labels.taxid)
        res = urllib.urlopen(url).readlines()
        file_out = path.STRING + '/%s_%s.txt' % (comp, labels.cutoff)
        OUT = open(file_out, 'w')
        print >>OUT, '\t'.join(['node1', 'node2', 'neighborhood', 'fusion', 'cooccurrence', 'homology', 'coexpression', 'experimental', 'knowledge', 'textmining', 'combined_score'])
        for line in res:
            items = line.rstrip().split('\t')
            node1 = items[2]
            node2 = items[3]
            nei = '0'
            fus = '0'
            cooc = '0'
            homo = '0'
            coex = '0'
            exp = '0'
            kno = '0'
            text = '0'
            comb = '0'
            scorelist = items[14].split('|')
            for score in scorelist:
                items2 = score.split(':')
                if items2[0]=='nscore':
                    nei = items2[1]
                if items2[0]=='fscore':
                    fus = items2[1]
                if items2[0]=='pscore':
                    cooc = items2[1]
                if items2[0]=='hscore':
                    homo = items2[1]
                if items2[0]=='ascore':
                    coex = items2[1]
                if items2[0]=='escore':
                    exp = items2[1]
                if items2[0]=='dscore':
                    kno = items2[1]
                if items2[0]=='tscore':
                    text = items2[1]
                if items2[0]=='score':
                    comb = items2[1]
            print >>OUT, '\t'.join([node1, node2, nei, fus, cooc, homo, coex, exp, kno, text, comb])

def genEdgeList(path, fps, labels):
    def labelBN(fp_network):
        el = []     
        judgeedge = {} #[edge] : combined_score (float)
        nodes = []
        NETWORK = open(fp_network, 'r')
        line = NETWORK.readline() #skip the first line: 0-node1, 1-node2, 2-neighborhood, 3-fusion, 4-cooccurrence, 5-homology
                                  #                        6-coexpression, 7-experimental, 8-knowledge, 9-textmining, 10-combined_score
                                  
        for line in NETWORK.readlines():
            items = line.rstrip().split('\t')
            node1 = items[0]
            node2 = items[1]
            edge = node1+','+node2
            redge = node2+','+node1
            values = ','.join([items[2],items[3],items[4],items[5],items[6],items[7],items[8],items[9],items[10]])
            if not judgeedge.has_key(edge):
                if not judgeedge.has_key(redge):
                    judgeedge[edge] = float(items[10])
                    if not node1 in nodes:
                        nodes.append(node1)
                    if not node2 in nodes:
                        nodes.append(node2)               
                    line = edge+':'+values
                    el.append(line)
                else:
                    oldscore = judgeedge[redge]
                    if float(items[10]) > oldscore:
                        judgeedge[redge] = float(items[10])
            else:
                oldscore = judgeedge[edge]
                if float(items[10]) > oldscore:
                    judgeedge[edge] = float(items[10])                       

        NETWORK.close()
        return (el, nodes)


    def printEdgeList(fp_edgelist,el):
        EDGELIST = open(fp_edgelist,'w')
        for edge in el:
            print >>EDGELIST, edge
        EDGELIST.close()
    def printNodesInfo(fp_genelist, fp_hit, fp_external, nodes_edges):
        GENELIST = open(fp_genelist,'r')  
        nodes_original = GENELIST.read().split('\n')
        set_original = set(nodes_original)

        set_edges = set(nodes_edges)
        
        nodes_hit = list(set_original&set_edges) #type 3: hit
        nodes_external = list(set_edges-set_original) #type 4: external
   
        NODESINFO1 = open(fp_hit,'w')
        print >>NODESINFO1, '\n'.join(nodes_hit)+'\n'
        NODESINFO2 = open(fp_external,'w')
        print >>NODESINFO2, '\n'.join(nodes_external)+'\n'

        NODESINFO1.close()
        NODESINFO2.close()

    print 'Generating edge list...'
    for comp in labels.comp:
        fp_network = path.STRING + '/%s_%s.txt' % (comp, labels.cutoff)
        fp_edgelist = path.STRING + '/edgelist/%s_%s_edgelist.csv' % (comp, labels.cutoff)
        fp_genelist = fps['Gene List'][comp]
        fp_hit = path.STRING + '/nodes_info/%s_%s_nodes_hit.txt' % (comp, labels.cutoff)
        fp_external = path.STRING + '/nodes_info/%s_%s_nodes_external.txt' % (comp, labels.cutoff)
        (el, nodes) = labelBN(fp_network)
        printEdgeList(fp_edgelist,el)
        printNodesInfo(fp_genelist, fp_hit, fp_external, nodes)

def genNetworkInput(path, fps, labels):
    def fillHashValue(dic_nodeinfo,nodes,value):
        for node in nodes:
            if dic_nodeinfo.has_key(node):
                print 'WARNING: conficts in node %s' % (node)
                continue
            dic_nodeinfo[node] = value
            
        return(dic_nodeinfo)

    def recordNodeInfo(fp_hit, fp_external):
        dic_nodeinfo = {} # SNPs: genes
        EXNODE = open(fp_external,'r')
        HITNODE = open(fp_hit,'r')

        exnodes = [i for i in EXNODE.read().split('\n') if i != '' ]
        hitnodes = [i for i in HITNODE.read().split('\n') if i != '' ]

        dic_nodeinfo = fillHashValue(dic_nodeinfo,exnodes,'external')
        dic_nodeinfo = fillHashValue(dic_nodeinfo,hitnodes,'hit')
        
        return (dic_nodeinfo)

    # ------------------------------------------
    def createEL(fp_edgelist, fp_elinput, dic_nodeinfo):
        INPUTEL = open(fp_edgelist,'r')
        OUTEL = open(fp_elinput,'w')        
        threshold = 0.9
        
        for readline in INPUTEL:
            items = readline.rstrip().split(':')
            pairnodes = items[0].split(',')
            infos = []
            vals = items[1].split(',')
            if float(vals[len(vals)-1])<threshold:
                continue
            for node in pairnodes:
                infos.append(dic_nodeinfo[node])
            print >>OUTEL, ','.join(pairnodes+infos)+':'+items[1]

    print 'Generating input files..'
    for comp in labels.comp:
        print '\tProcessing group: %s' % comp
        fp_edgelist = path.STRING + '/edgelist/%s_%s_edgelist.csv' % (comp, labels.cutoff)
        fp_hit = path.STRING + '/nodes_info/%s_%s_nodes_hit.txt' % (comp, labels.cutoff)
        fp_external = path.STRING + '/nodes_info/%s_%s_nodes_external.txt' % (comp, labels.cutoff)
        fp_elinput = path.STRING + '/yedinput/%s_%s-edgelist.csv' % (comp, labels.cutoff)
        dic_nodeinfo = recordNodeInfo(fp_hit, fp_external)
        createEL(fp_edgelist, fp_elinput, dic_nodeinfo)

def genNetwork(path, progpath):
    import os
    import time
    print 'Generating network graphs...'
    now = time.strftime('%Y-%m-%d')
    os.system('date 2012-11-02')
    os.chdir(progpath.java)
    os.system('javac Runner.java')
    os.system('java Runner "%s"' % path.STRING.replace('/','\\'))
    os.system('date %s' % now)

def annoNetwork(path, progpath, fps, labels):
    import os, sys
    import math
    from PIL import Image
    def Anno(fp_pic,fp_tag,fp_save,scalePic,scaleTag):
        pic = Image.open(fp_pic)
        picScale=tuple([int(round(scalePic*x)) for x in pic.size])
        pic=pic.resize(picScale)
        tag=Image.open(fp_tag)
        tagScale=tuple([int(round(scaleTag*x)) for x in tag.size])
        tag=tag.resize(tagScale)
        
        pic.paste(tag,(picScale[0]-tagScale[0],picScale[1]-tagScale[1]-2))
        pic.save(fp_save)

    print 'Tagging network graphs...'
    for type in labels.STRtypes2:
        print '\tTagging type: %s' % type
        fp_tag = progpath.colorlabel+'/%s.jpg' % type
        if type == 'black':
            for comp in labels.comp:
                fp_pic = fps['STRING Network'][comp][type].replace('jpg_tagged','jpg')
                fp_save = fps['STRING Network'][comp][type]
                Image.open(fp_pic).save(fp_save)
        else:
            for comp in labels.comp:
                fp_pic = fps['STRING Network'][comp][type].replace('jpg_tagged','jpg')
                fp_save = fps['STRING Network'][comp][type]
                
                Anno(fp_pic, fp_tag, fp_save,0.4,2)
                
            