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
    
## The APM random Generator
try:
    prod
    array
except:
    from numpy import prod, array

class LcgRand:
    def __init__(my, seed):
        my.seed = seed
        my.state = seed
        
    def lcg(my):
        my.state = 16807*my.state % 2147483647
        return my.state
    
    def rand(my):
        return my.lcg() / 2147483647.0
    
    def _randint( my, low, high):
        return ( my.lcg() % (high - low) )  + low
    
    def randint(my,low, high = None, size = None ):
        if( high == None ): 
            high = low
            low = 0
        if( size == None and type(high) == tuple):
            size = high
            high = low
            low = 0        
        if( size == None ):
            return my._randint(low, high)
        else:
            if( type(size) != tuple ):
                size = ( size, )
            tmp = array( [ my._randint(low, high) for i in range( prod( size) ) ] )   
            return tmp.reshape( size )

APM = LcgRand(1)
    
m = 1.6
b1 = 3.0
b2 = -1.0

n = 50

tmp = APM.rand() * 5

Positives = [ (tmp, m*tmp + b1) ]

tmp = rand() * 5
Negatives = [ (tmp,m*tmp + b2) ]

for i in range(n):
    x = APM.rand()*5
    y = m*x+b1 + APM.rand()*5.0
    
    Positives.append( (x,y) )
    
    x = APM.rand()*5
    y = m*x+b2 - APM.rand()*5.0
    
    Negatives.append( (x,y) )
    
Positives = array( Positives ) 
Negatives = array( Negatives )

Unclassified = []

for i in range(10):
    x = APM.rand()*5
    y = ( ( m*x+b1 + APM.rand()*5.0 )+( m*x+b2 - APM.rand()*5.0 ) )/2.0
    Unclassified.append( (x,y+APM.randint(-1,2)) )
    
UnclassifiedObservations = array( Unclassified ) 

figsize(7,5)


HTML(""" <p>The <b>View</b> function for viewing data sets is ready </p> <br/>
        <p>The <b>Positives</b> and <b>Negatives</b> data sets have been 
        generated, as well as the <b>UnclassifiedObservations</b> data
     """ )