## Doesn't yet work in Firefox for every possible argument (waiting for srcdoc -- Probably Oct 2013 in Firefox 25) 

## Tested on Chrome 28, Firefox 22, and Safari 5.1.7 on Windows 7 Home, Professional

from __future__ import division
from IPython.display import HTML


class DetachableView:
    "ONLY DOUBLE QUOTES PERMITTED IN HTMLview -- use &apos; for single quotes"
    def __init__(my, PostType = "OneWay" ): #PostType is for later
        my.framecntr = 0 
        lttrs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
        
        my.frameSig = ""
        for i in range(20):
            my.frameSig += lttrs[ randint(len(lttrs)) ]

    def URLView( my, URL, width=None, height=None, toggle = True,  message = None):
        """ URLView(URL) -> Detachable View of the page at URL
        
            if message != None, then postMessage API used to send message to Views"""
        
        # Each LaunchView is unique -- probably could have one LaunchView + arguments, 
        # but the data to be displayed (i.e., the would-be argument) is the lion's 
        # share of the definition
        my.framecntr += 1
        fcntr = my.frameSig + str(my.framecntr)
        
        HtmlString = ""
        # toggle = False suppresses the popup window
        if( toggle):
            HtmlString += """

                <script type='text/javascript'>
                    var win;
                    var messageHandler%s ;
                    var MessageRepeater%s ;
                    function LaunchView%s( ) {
                        var iFrame = document.getElementById('IframeView%s');
                        if( iFrame.style.display == 'block') {
                            win = window.open( '%s', 'Detached%s' ,'height=500,width=800,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');
                    """ % (fcntr, fcntr, fcntr, fcntr, URL, fcntr ) 
            if( message != None):
                HtmlString += """
                            messageHandler%s = function(event){
                                if( event.data == 'ready' ) { 
                                    win.postMessage('%s', '*' ) ;
                                }
                                if( event.data == 'done'  ) {
                                    window.removeEventListener('message',arguments.callee,false)
                                }
                            }
                            window.addEventListener('message',messageHandler%s, false);
                  """ %(fcntr, message, fcntr )

            HtmlString += """
                        iFrame.style.display = 'none'
                    } else { 
                        iFrame.style.display = 'block'
                    };

                }
                
                </script>  
      
                <input type='button' value='toggle view' onclick='LaunchView%s()'> <br>
                
            """ % fcntr 
        
        # Set width, height
        if( width == None):
            width = "95%"
        elif( type(width) != type( "500px" )):
            width = "%spx" % width
            
        if( height == None):
            height = "24em"
        elif( type(height) != type( "500px" )):
            height = "%spx" % height
           
        # Create an Iframe (BTW, HTML() is fantastic! 
        HtmlString += """
            <iframe id = 'IframeView%s' src = '%s' style = 'width:%s;height:%s;display:block;' > 
                Your browser does not support iframes </iframe> 
            """ % ( fcntr, URL, width, height)

        if( message != None):
            HtmlString += """
                <script type="text/javascript">

                    var MessageHandler%s = function(event){
                        if( event.data == 'ready' ) {
                            document.getElementById('IframeView%s').contentWindow.postMessage('%s', '*' ) ;
                        }
                        if( event.data == 'done'  ) {
                            window.removeEventListener('message',arguments.callee,false)
                        }
                    }
            
                    window.addEventListener('message',MessageHandler%s, false);
            
                </script> """ %(fcntr, fcntr, message, fcntr)
        return HTML(HtmlString)
        

    def HTMLView( my, HTMLCode, width=None, height=None, toggle = True):
        """        HTMLCode  -> Detachable View of the Code
        
        ONLY DOUBLE QUOTES PERMITTED IN HTMLview -- use &apos; for single quotes"""
        
        # Each LaunchView is unique -- probably could have one LaunchView + arguments, 
        # but the data to be displayed (i.e., the would-be argument) is the lion's 
        # share of the definition
        my.framecntr += 1
        fcntr = my.frameSig + str(my.framecntr)
        
        #Javascript is weird
        HTMLJS = HTMLCode.replace('</script>', '<\/script>' )
        HTMLlist = HTMLJS.split('\n')
        
        #Split into lines for the win_doc.writeln commands
        HTMLtext = "' '"
        for line in HTMLlist:
            HTMLtext += ", '%s' " % line
 
        HtmlString  = ""
        
        # toggle = False suppresses the popup window
        if( toggle):
            HtmlString += """

           <script type='text/javascript'> 
                
                function LaunchView%s( ) {
                    var iFrame = document.getElementById('IframeView%s');
                    var iStringArray = [ %s ];
                    var DetachedName = 'Detached%s';
                    if( iFrame.style.display == 'block') {
                        var win = window.open('about:blank', DetachedName ,'height=500,width=800,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');
                        
                        var win_doc = win.document;
                        win_doc.open();
                        win_doc.writeln('<!DOCTYPE html><htm' + 'l><head><body>');
                        for (var i = 0; i < iStringArray.length; i++) {
                            win_doc.writeln( iStringArray[i] );
                        };
                        win_doc.writeln('</body></ht' + 'ml>');
                        win_doc.close();
                        iFrame.style.display = 'none'
                    } else { 
                        iFrame.style.display = 'block'
                    };
                }
                
            </script>  
      
                <input type='button' value='toggle view' onclick='LaunchView%s()'> <br>
                
            """ % ( fcntr, fcntr, HTMLtext, fcntr, fcntr ) 
        
        # Set width, height
        if( width == None):
            width = "95%"
        elif( type(width) != type( "500px" )):
            width = "%spx" % width
            
        if( height == None):
            height = "24em"
        elif( type(height) != type( "500px" )):
            height = "%spx" % height
           
        HTMLJS = HTMLJS.replace('"','&quot;' )
        
        # Create an Iframe (BTW, HTML() is fantastic! 
        HtmlString += """
            <iframe id = 'IframeView%s' srcdoc = '%s'  src = "javascript: '%s' " style = 'width:%s;height:%s;display:block;' > 
                Your browser does not support iframes </iframe> 
            """ % ( fcntr, HTMLCode, HTMLJS, width, height)
        return HTML(HtmlString)
        

## View -- for tables, etc. 

FramesAndArrays = DetachableView( )

Precision = 5
ComplexUnitString = "j"

try:
    cround
except:
    def cround(z,n=5): return complex(round(z.real,n), round(z.imag,n)) 


def FormatForView( entry ): 
    "entry -> nice representation for this object"
    
    try:
        if(entry.dtype.kind in typecodes['AllFloat'] ):
            entry = round(entry,Precision)
        elif( entry.imag != 0):
            if( entry.real == 0):
                entry = " %s %s " % (round( entry.imag,Precision), ComplexUnitString )
            else:
                entry = cround(entry,Precision)
                entry = " %s + %s %s" % (entry.real, entry.imag, ComplexUnitString)
        elif( entry.dtype.kind in typecodes['Complex']+'c' ):
            entry = round(entry.real,Precision)
        return entry
    except:
        try:
            if( entry.imag != 0):
                if( entry.real == 0):
                    entry = " %s %s " % (round( entry.imag,Precision), ComplexUnitString )
                else:
                    entry = cround(entry,Precision)
                    entry = " %s + %s %s" % (entry.real, entry.imag, ComplexUnitString)
            return entry
        except:
            return entry


def View( DataFrameOrArray ):
    """array or dataframe ->  Detachable View in Notebook
    
    If DataFrameOrArray is either a Pandas Dataframe or a Numpy array 
    (anything which has a .shape), then View creates a custom view with
    relevant information and places it in a detachable view.  Otherwise, 
    View returns a detachable view of the standard representation. 
    
    Clicking on the [toggle view] button detaches the View and places
    it in a popup.  Clicking again restores the original inline view. 
    
    NOTE:  DESIGNED TO WORK WITH PYLAB!
    
    Examples: 
    
    In [ ]: A = array( [ [1,2],[3,4] ] )
            View(A)
    
    Out[ ]: [toggle view]
            Formatted table with scrollbars if necessary
    
    
    
    In [ ]: from pandas import DataFrame
            B = DataFrame( A , index = [1,2], columns = ["A","B"] )
            View(B)   
            
    Out[ ]: [toggle view]
            Formatted table with scrollbars if necessary
            and with Column/Row headings


    In [ ]: C = randn( 50, 50) # Gaussian random sampled 50x50 array
            View(C)
            
    Out[ ]: [toggle view]
            Scrolled View of Large Matrix
    
    """
    
    # Is this a data frame (based on existence of column/index lists 
    IsDF = False
    try: 
        DataFrameOrArray[DataFrameOrArray.columns[0]][DataFrameOrArray.index[0]]
        len( DataFrameOrArray.columns )
        len( DataFrameOrArray.index )
        IsDF = True
    except:
        pass 

    # Standard Rep if not a DataFrame or an Array
    try:
        DataFrameOrArray.shape
        if( not IsDF ):
            DataFrameOrArray.dtype.names
    except:
        return FramesAndArrays.HTMLView(str(DataFrameOrArray) )
    
    # Find all names that instance is bound to
    nme = "Name(s): "
    for nm in get_ipython().magic(u'who_ls'): 
        if( eval(nm) is DataFrameOrArray ):
            nme += nm + str(", ")
    nme = nme[0:-2]

    
    # Establish values for nrows and ncols
    if( len(DataFrameOrArray.shape) == 1 ):
        if( DataFrameOrArray.dtype.names ):
            nrows = len(DataFrameOrArray)
            ncols = len( DataFrameOrArray.dtype.names ) 
        else:
            ncols = len(DataFrameOrArray)
            nrows = 1
    else:
        nrows, ncols = DataFrameOrArray.shape
        
    # Not too small, but after height = 35em, scrollbars
    hght = "%sem" % max(  8, min( 2*nrows+8, 35 ))
    if( ncols < 8):
        wdth = "50%" 
    else:
        wdth = "95%"
    
    # Create header info for the 3 types -- array, Structured Array, DataFrame
    if( IsDF ):
        typ = "DataFrame: Entries via  Name[col][row] "
        shp = ( len( DataFrameOrArray.index), len(DataFrameOrArray.columns) )
        dtp = ""
        for tp in DataFrameOrArray.dtypes:
            dtp += "%s, " % tp
    elif( DataFrameOrArray.dtype.names ):
        typ = "Structured Array: Entries via  Name[col][row] "
        shp = ( DataFrameOrArray.shape[0], len(DataFrameOrArray.dtype.names) )
        dtp = ""
        for tp in DataFrameOrArray.dtype.descr:
            dtp += "%s, " % tp[1]
        dtp = dtp.replace("<","&amp;lt;")
        dtp = dtp.replace(">","&amp;gt;")
    elif( nrows == 1 ):
        typ = "Numpy 1D Array: Entries via  Name[index] "
        shp = DataFrameOrArray.shape
        dtp = DataFrameOrArray.dtype
    else:
        typ = "Numpy Array: Entries via  Name[row, col] "
        shp = DataFrameOrArray.shape
        dtp = DataFrameOrArray.dtype
    
    # Style and Header Info
    HtmlString   = """
    <style>
        table   { width:95%;border:1px solid LightGray;border-spacing:0;border-collapse: collapse; }
        th      { border:1px solid LightGray;padding:2px 4px; white-space:nowrap; } 
        td      { border:1px solid LightGray;padding:2px 4px;text-align:center;white-space:nowrap; } 
        caption { text-align:left; } 
        #bcap   { font-size:larger; } 
    </style>
    """
    
    HtmlString  += """
    <div> <b id =  "bcap" > %s  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | </b>
            &nbsp; &nbsp; &nbsp; &nbsp; %s  <sub> &nbsp; </sub> <br>  
        <table border=1 >
            <caption> shape: %s  &nbsp;&nbsp;&nbsp;&nbsp; Type(s): %s   </caption>
    """  % ( nme, typ, shp, dtp ) 
    
    # Create HTML5 table of given structure -- lots of details, but mainly iterating over rows and
    # columns to insert <tr>, <th>, and <td> tags as appropriate
    if( IsDF ):
        HtmlString += "<tr> <th> &nbsp; </th>"
        for nme in DataFrameOrArray.columns:
            HtmlString += '<th> %s </th> ' % nme 
        HtmlString += "</tr>" 
        for idx in DataFrameOrArray.index:
            HtmlString += '<tr><td><b> %s </b></td> ' % idx
            for col in DataFrameOrArray.columns:
                HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[col][idx]) 
            HtmlString += "</tr>"
    elif( DataFrameOrArray.dtype.names ):
        HtmlString += "<tr> "
        for nme in DataFrameOrArray.dtype.names:
            HtmlString += '<th> %s </th> ' % nme 
        HtmlString += "</tr>  "
        for row in range(ncols):
            HtmlString += "<tr>"
            for nme in DataFrameOrArray.dtype.names:
                HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[nme][row]) 
            HtmlString += "</tr>  "
    else:
        for row in range(nrows):
            HtmlString += "<tr>"
            for col in range(ncols):
                if(len(DataFrameOrArray.shape) > 1 ):
                    HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[row,col])
                else:
                    HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[col])
            HtmlString += "</tr>  "
    
    HtmlString += "  </table></div> " 
    return  FramesAndArrays.HTMLView(HtmlString, width = wdth, height=hght)
    
## ViewDecisionTree  for DecisionTree viewer

import numpy as np

from sklearn import tree

from sklearn.tree import _tree 


def export_json(decision_tree, out_file=None, feature_names=None):
    """Export a decision tree in JSON format.

    This function generates a JSON representation of the decision tree,
    which is then written into `out_file`. Once exported, graphical renderings
    can be generated using, for example::

        $ dot -Tps tree.dot -o tree.ps      (PostScript format)
        $ dot -Tpng tree.dot -o tree.png    (PNG format)

    Parameters
    ----------
    decision_tree : decision tree classifier
        The decision tree to be exported to JSON.

    out : file object or string, optional (default=None)
        Handle or name of the output file.

    feature_names : list of strings, optional (default=None)
        Names of each of the features.

    Returns
    -------
    out_file : file object
        The file object to which the tree was exported.  The user is
        expected to `close()` this object when done with it.

    Examples
    --------
    >>> from sklearn.datasets import load_iris
    >>> from sklearn import tree

    >>> clf = tree.DecisionTreeClassifier()
    >>> iris = load_iris()

    >>> clf = clf.fit(iris.data, iris.target)
    >>> import tempfile
    >>> out_file = tree.export_json(clf, out_file=tempfile.TemporaryFile())
    >>> out_file.close()
    """
#   import numpy as np

#    from sklearn.tree import _tree

    def arr_to_py(arr):
        arr = arr.ravel()
        wrapper = float
        if np.issubdtype(arr.dtype, np.int):
            wrapper = int
        return map(wrapper, arr.tolist())


    def node_to_str(tree, node_id):
        node_repr = '"error": %.4f, "samples": %d, "value": %s' \
                    % (tree.init_error[node_id],
                       tree.n_samples[node_id],
                       arr_to_py(tree.value[node_id]))
        if tree.children_left[node_id] != _tree.TREE_LEAF:
            if feature_names is not None:
                feature = feature_names[tree.feature[node_id]]
            else:
                feature = "X[%s]" % tree.feature[node_id]

            label = '"label": "%s <= %.2f"' % (feature,
                                               tree.threshold[node_id])
            node_type = '"type": "split"'
        else:
            node_type = '"type": "leaf"'
            label = '"label": "Leaf - %d"' % node_id
        node_repr = ", ".join((node_repr, label, node_type))
        return node_repr

    def recurse(tree, node_id, parent=None):
        if node_id == _tree.TREE_LEAF:
            raise ValueError("Invalid node_id %s" % _tree.TREE_LEAF)

        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]

        # Open node with description
        out_file.write('{%s' % node_to_str(tree, node_id))

        # write children
        if left_child != _tree.TREE_LEAF:  # and right_child != _tree.TREE_LEAF
            out_file.write(', "children": [')
            recurse(tree, left_child, node_id)
            out_file.write(', ')
            recurse(tree, right_child, node_id)
            out_file.write(']')

        # close node
        out_file.write('}')

    if out_file is None:
        out_file = open("tree.json", "w")
    elif isinstance(out_file, basestring):
        out_file = open(out_file, "w")

    if isinstance(decision_tree, _tree.Tree):
        recurse(decision_tree, 0)
    else:
        recurse(decision_tree.tree_, 0)

    return out_file

import StringIO

def ViewDecisionTree( decision_tree, feature_names=None):
    """ViewDecisionTree( decision_tree ) ->  DetachableView of the tree

    This function generates a JSON representation of the decision tree,
    which is displayed as a Detachable View in the IPython Notebook.

    Parameters
    ----------
    decision_tree : decision tree classifier
        The decision tree to be exported to JSON.

    feature_names : list of strings, optional (default=None)
        Names of each of the features.

    Returns
    -------
    An inline view (for HTML5 compliant browsers) along with a button that 
    launches a detached view (in all browsers)

    Examples
    --------
    In [ ]: from sklearn.datasets import load_iris
            from sklearn import tree
            clf = tree.DecisionTreeClassifier()
            iris = load_iris()

            clf = clf.fit(iris.data, iris.target)
            ViewDecisionTree(clf) #Only in IPython Notebook
            
    Out[ ]: [toggle view]
            Detachable View of Tree

    """


    output = StringIO.StringIO()
    
    out_file = export_json(clf, out_file=output, feature_names=feature_names)
    msg = out_file.getvalue()
    out_file.close()
    return FramesAndArrays.URLView( 'http://math.etsu.edu/knisleyj/scripts/DecisionTreeViewer.html', message = msg, width = "100%")    


    




HTML(""" The <b>DetachableView</b> class is ready <br>
         The <b>View</b> function is ready <br>
         The <b>ViewDecisionTree</b> function is ready""" )