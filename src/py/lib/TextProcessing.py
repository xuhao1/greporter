def search_replace_all(w,find_str, replace_str):
    wdFindContinue = 1
    wdReplaceAll = 2
    # expression.Execute(FindText, MatchCase, MatchWholeWord,
    #   MatchWildcards, MatchSoundsLike, MatchAllWordForms, Forward, 
    #   Wrap, Format, ReplaceWith, Replace)
    w.Selection.Find.Execute(find_str, False, False, False, False, False, True, wdFindContinue, False, replace_str, wdReplaceAll)  

def text2table(rng,format,fontsize,fontname,fit):
        #transform text to table in Word
        table = rng.ConvertToTable(Separator='\t')
        if fit == 'AutoFit':
            table.Columns.AutoFit()
        elif fit == 'DistributeWidth':
            table.Columns.DistributeWidth()   
        table.AutoFormat(Format = format)
        rng.Font.Size = fontsize
        rng.Font.Name = fontname
        rng.Collapse(0)
        
        return table

def setTableWidth(table,widths):
        # set every column's width in table
        for (col, width) in enumerate(widths):
                table.Columns(col+1).SetWidth(width*28.35, 0)
        return table

def rmtag(doc,w,tag):
        # remove the tag in template
        doc.Range(0,0).Select()
        rng_whole = w.Selection
        rng_whole.Find.Execute(tag, False, False, False, False, False, True, 1, False, '', 1)
        rng = w.Selection

        return rng
