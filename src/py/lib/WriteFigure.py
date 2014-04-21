from TextProcessing import *
import os

def FlowChart(doc, w, tag, fp):
    rng = rmtag(doc, w, tag)
    img = rng.InlineShapes.AddPicture(fp)
    return img
    print "FlowChart: Over"

def STRNetwork(doc, w, tag, whichfigure, fps, labels):
    def RenameComp(oldcomp):
        if oldcomp == 'overlap1':
            newcomp = 'Overlap1'
        else:
            fnmitems = oldcomp.split('_')
            newcomp = '%s vs. %s' % (labels.groupmap[fnmitems[1]], labels.groupmap[fnmitems[0]])
        return(newcomp)
    #------------------------------------------------
    # remove the tag
    rng = rmtag(doc,w,tag)
    explain = 'Edges - the predicted functional links, consist of up to 7 lines: one color for each type of evidence. (Green: "Neighborhood", red: "Gene Fusion", blue: "Cooccurrence", black: "Coexpression", magenta: "Experiments", cyan: "Databases" and orange: "Textmining"). Thicker line denotes a higher prediction confidence.'
    
    for comp in labels.comp:
        figtitle = 'Figure %s. Knowledge-based Networks %s (Yellow nodes: genes from our data set, Blue nodes: genes from external database but not in our dataset)' % (whichfigure, RenameComp(comp))
        #Write Figure Title
        rng.Paragraphs.Add()
        rng.ParagraphFormat.Alignment = 1
        rng.Collapse(0)
        rng.InsertAfter(figtitle)
        rng.Font.Size = 12
        rng.Collapse(0)
        subdecs = []
        num_subfig = 1
        for STRtype in labels.STRtypes:
            fp = fps[comp][STRtype]
            # insert pic
            subtitle = "Figure %d. (%d) " % (whichfigure, num_subfig)
            rng.Paragraphs.Add()
            rng.ParagraphFormat.Alignment = 1
            rng.InsertAfter(subtitle)
            rng.Collapse(0)
            if STRtype == 'black':
                print("(%d) %s network. " % (num_subfig, 'complete'))
                subdecs.append("(%d) %s network. " % (num_subfig, 'complete'))
            else:
                print("(%d) %s network. " % (num_subfig, STRtype))
                subdecs.append("(%d) %s network. " % (num_subfig, STRtype))
            print fp
            pic = rng.InlineShapes.AddPicture(fp)
            num_subfig += 1
            rng.Collapse(0)
            #pic.Height = 10*28.35
            #pic.Width = 10*28.35
        #Write Description
        rng.Paragraphs.Add()
        rng.Collapse(0)
        dec= 'Figure %s: ' % (whichfigure) + ' '.join(subdecs)
        rng.InsertAfter(dec)
        rng.Font.Size = 9
        rng.Collapse(0)
        whichfigure += 1
    print "STRNetwork: Over"
