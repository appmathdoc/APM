#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Doesn't yet work in Firefox for every possible argument (waiting for srcdoc -- Probably Oct 2013 in Firefox 25) 

## Tested on Chrome 28, Firefox 22, and Safari 5.1.7 on Windows 7 Home, Professional

from __future__ import division
from IPython.display import HTML
from pandas import DataFrame


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
        
    # Not too small, but after height = 40em, wdth = 80 em, scrollbars
    hght = "%sem" % max(  8, min( 2*nrows+8, 40 ))
    wdth = "%sem" % max( 40, min( 4*ncols+4, 80 ))
    
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
        for row in range(nrows):
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
            
            
    def _choose( my, low, high, number):
        if( number > high-low ):
            raise "Number of choices %s exceeds difference between %s and %s" % ( number, high, low )
        result = []
        
        for i in xrange(number):
            tmp = my.randint(low,high)
            for j in xrange(1000*number):
                if( not ( tmp in result ) ):
                    result.append(tmp)
                    break
                tmp = my.randint(low,high)
            else:
                raise Exception("Failed to generate choose.  Please execute again")
            
        return array(result)
            
    def choose( my, low, high = None, size = None ):
        if( high == None ): 
            high = low
            low = 0
        if( size == None and type(high) == tuple):
            size = high
            high = low
            low = 0        
        if( size == None ):
            return my._choose(low, high, 1)
        else:
            if( type(size) != tuple ):
                size = ( size, )
            tmp = my._choose(low, high, prod( size) )   
            return tmp.reshape( size )

    def sample(my, seq, number, with_replacement = True):
        "sample(seq, number) -> number of samples from seq"
        if( with_replacement ):
            return array([ seq[j] for j in my.randint(0,len(seq), number ) ] )
        else:
            if( len(seq) < number ):
                raise Exception( "number must be no greater than the length of %s" % seq )
            inds = my.choose(0,len(seq), number)
            tmp = array(seq)
            return tmp[inds]

 


HouseholdNames = [  "SMITH","JOHNSON","WILLIAMS","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE","TAYLOR","ANDERSON","THOMAS","JACKSON","WHITE",
                    "HARRIS","MARTIN","THOMPSON","GARCIA","MARTINEZ","ROBINSON","CLARK","RODRIGUEZ","LEWIS","LEE","WALKER","HALL","ALLEN","YOUNG",
                    "HERNANDEZ","KING","WRIGHT","LOPEZ","HILL","SCOTT","GREEN","ADAMS","BAKER","GONZALEZ","NELSON","CARTER","MITCHELL","PEREZ","ROBERTS",
                    "TURNER","PHILLIPS","CAMPBELL","PARKER","EVANS","EDWARDS","COLLINS","STEWART","SANCHEZ","MORRIS","ROGERS","REED","COOK","MORGAN","BELL",
                    "MURPHY","BAILEY","RIVERA","COOPER","RICHARDSON","COX","HOWARD","WARD","TORRES","PETERSON","GRAY","RAMIREZ","JAMES","WATSON","BROOKS","KELLY",
                    "SANDERS","PRICE","BENNETT","WOOD","BARNES","ROSS","HENDERSON","COLEMAN","JENKINS","PERRY","POWELL","LONG","PATTERSON","HUGHES","FLORES",
                    "WASHINGTON","BUTLER","SIMMONS","FOSTER","GONZALES","BRYANT","ALEXANDER","RUSSELL","GRIFFIN","DIAZ","HAYES","MYERS","FORD","HAMILTON",
                    "GRAHAM","SULLIVAN","WALLACE","WOODS","COLE","WEST","JORDAN","OWENS","REYNOLDS","FISHER","ELLIS","HARRISON","GIBSON","MCDONALD","CRUZ",
                    "MARSHALL","ORTIZ","GOMEZ","MURRAY","FREEMAN","WELLS","WEBB","SIMPSON","STEVENS","TUCKER","PORTER","HUNTER","HICKS","CRAWFORD","HENRY",
                    "BOYD","MASON","MORALES","KENNEDY","WARREN","DIXON","RAMOS","REYES","BURNS","GORDON","SHAW","HOLMES","RICE","ROBERTSON","HUNT","BLACK",
                    "DANIELS","PALMER","MILLS","NICHOLS","GRANT","KNIGHT","FERGUSON","ROSE","STONE","HAWKINS","DUNN","PERKINS","HUDSON","SPENCER","GARDNER",
                    "STEPHENS","PAYNE","PIERCE","BERRY","MATTHEWS","ARNOLD","WAGNER","WILLIS","RAY","WATKINS","OLSON","CARROLL","DUNCAN","SNYDER","HART",
                    "CUNNINGHAM","BRADLEY","LANE","ANDREWS","RUIZ","HARPER","FOX","RILEY","ARMSTRONG","CARPENTER","WEAVER","GREENE","LAWRENCE","ELLIOTT",
                    "CHAVEZ","SIMS","AUSTIN","PETERS","KELLEY","FRANKLIN","LAWSON","FIELDS","GUTIERREZ","RYAN","SCHMIDT","CARR","VASQUEZ","CASTILLO","WHEELER",
                    "CHAPMAN","OLIVER","MONTGOMERY","RICHARDS","WILLIAMSON","JOHNSTON","BANKS","MEYER","BISHOP","MCCOY","HOWELL","ALVAREZ","MORRISON","HANSEN",
                    "FERNANDEZ","GARZA","HARVEY","LITTLE","BURTON","STANLEY","NGUYEN","GEORGE","JACOBS","REID","KIM","FULLER","LYNCH","DEAN","GILBERT","GARRETT",
                    "ROMERO","WELCH","LARSON","FRAZIER","BURKE","HANSON","DAY","MENDOZA","MORENO","BOWMAN","MEDINA","FOWLER"]

AnimalNames = [ "aardvark","alligator","alpaca","anteater","antelope","aoudad","ape","argali","armadillo","baboon","badger","basilisk","bat","bear","beaver",
                "bighorn","bison","boar","budgerigar","buffalo","bull","bunny","burro","camel","canary","capybara","cat","chameleon","chamois","cheetah",
                "chimpanzee","chinchilla","chipmunk","civet","coati","colt","cony","cougar","cow","coyote","crocodile","crow","deer","dingo","doe","dog",
                "donkey","dormouse","dromedary","duckbill","dugong","eland","elephant","elk","ermine","ewe","fawn","ferret","finch","fish","fox","frog",
                "gazelle","gemsbok","gila","monster","giraffe","gnu","goat","gopher","gorilla","grizzly","groundhog","guanaco","guineapig","hamster","hare",
                "hartebeest","hedgehog","hippopotamus","hog","horse","hyena","ibex","iguana","impala","jackal","jaguar","jerboa","kangaroo","kid","kinkajou",
                "kitten","koala","koodoo","lamb","lemur","leopard","lion","lizard","llama","lovebird","lynx","mandrill","mare","marmoset","marten","mink","mole",
                "mongoose","monkey","moose","mouse","mule","muskrat","mustang","mynah","bird","newt","ocelot","okapi","opossum","orangutan","oryx","otter","ox",
                "panda","panther","parakeet","parrot","peccary","pig","platypus","pony","porcupine","porpoise","prairie","pronghorn","puma","puppy","rabbit",
                "raccoon","ram","rat","reindeer","reptile","rhinoceros","roebuck","salamander","seal","sheep","shrew","silver","skunk","sloth","snake","springbok",
                "squirrel","stallion","steer","tapir","tiger","toad","turtle","vicuna","walrus","warthog","waterbuck","weasel","whale","wildcat","wolf","wolverine",
                "wombat","woodchuck","yak","zebra"]

                
def AnimalIndex(animal):
    animal = animal.strip()
    for i in range(len(AnimalNames)):
        if( AnimalNames[i] == animal.lower() ):
            return i
    return False

def HouseholdIndex(household):
    household = household.strip()
    for i in range(len(HouseholdNames)):
        if( HouseholdNames[i] == household.upper() ):
            return i
    return False
                
def String2Int(strng):
    'StrToNum(strng) -> integer'
    val = ""
    for i in range(len(strng)):
        val += str( ord( strng[i] ) )
    return eval(val)

APM = LcgRand( String2Int( username.lower() ) )

def ImputationProblem(Username, nr = 25, nc = 10, ne = 50 ):
    "Returns an imputation problem"
    APM = LcgRand( String2Int( Username.lower() ) )
    
    dta = APM.randint( 0, 10, ( 3, nc ) )
    dta = dta.astype(float)
    DataKey = zeros( (nr,nc) )
    for i in range(nr):
        DataKey[i] = dta[ APM.randint(3) ]
        for j in range(nc):
            if( APM.rand() < 0.1 ):
                DataKey[i,j] += 3*cos(APM.randint(1,3)*pi)
        
    DataKey = DataKey.astype(int)
    
    # create data
    
    DataKey = DataKey.astype(float)
    Data = DataKey.copy()
    
    # replace entries with nan
    
    rows = APM.randint(0,nr,ne)
    #cols = APM.randint(0,nc,ne)
    cols = array( [ i % nc for i in range(ne) ] )
    
    for i in range(ne):
        Data[rows[i], cols[i]] = nan
    
    return Data, DataKey, ne

Data, AssnImputeKey, AssnImpCnt = ImputationProblem(username)    

def Score(Candidate):
    'Score(Candidate) -> score for Candidate as a percentage'
    
    Tmp = Candidate - AssnImputeKey
    Errors = Tmp[ Tmp != 0].flatten()
    
    Scre = AssnImpCnt - len(Errors)
    
    for er in Errors:
        if( abs(er) <= 1 ):
            Scre += 0.8
        elif( abs(er) <= 2):
            Scre += 0.4
            
    return Scre/AssnImpCnt
    
def RecommenderProblem(Username):
    'Returns Recommender Problem Data'
    
    APM = LcgRand( String2Int( Username.lower() ) )
    PreData = APM.randint(0,7,(25,177))
    for i in range(25):
        for j in range(177):
            if( not (1 <= PreData[i,j] <= 5 ) ):
                PreData[i,j] = 0
            if( j in [130] and PreData[i,j] > 0 ):
                PreData[i,j] = APM.randint(4,6) #Everyone Loves the Penguins
                
    Data = zeros( (250,177) )
    
    inds = APM.choose(0,250,250)
    ic = 0
    for i in range(25):
        for ii in range(10):
            for j in range(177):
                if( APM.rand( ) < 0.10 ): # change 10% of the entries
                    Data[ inds[ic], j] = APM.randint(0,6)
                else:
                    Data[ inds[ic], j] = PreData[i,j]
            ic += 1
            
 
    Df = DataFrame( array(Data, dtype=float), index = HouseholdNames, columns = AnimalNames)
                
    # Replace some ratings with zeros 
    REinds = []
    REcnt  = 0
    Key = []
    Prb = []
    for i in range(250):
        for j in range(177):
           if( Data[i,j] > 0  ):
                if( APM.rand() < 0.05 and REcnt < 100 ):
                    REinds.append( [i,j] )
                    REcnt += 1
                    
    for rind in REinds:
        Hh = HouseholdNames[ rind[0] ]
        An = AnimalNames[ rind[1] ]
        Key.append( (Hh, An, Df[An][Hh]) )
        Prb.append( (Hh, An, 0 ) )
        Df[ An ][ Hh ] = 0
                    
    # Add the NA's 
    NAinds = []
    NAcnt  = 0
    for i in range(250):
        for j in range(177):
           if( Data[i,j] > 0  ):
                if( APM.rand() < 0.05 and NAcnt < 500 ):
                    NAinds.append( [i,j] )
                    NAcnt += 1

    #print(len(NAinds))
    
    for nind in NAinds:
        Hh = HouseholdNames[ nind[0] ]
        An = AnimalNames[ nind[1] ]
        Df[ An ][ Hh ] = NaN
        
    return Df, Prb, Key


try:
    if( username == "Replace with Your Username"):
        raise 
    SmallTownZoo, Unrated, FstExkey = RecommenderProblem(username)
except:
    print("Unable to produce the SmallTownZoo data.  Did you enter your username?")



def Grade(Candidate):
    "Grade(Candidate) -> CandidatePercentageCorrect"
    
    Key = FstExkey
    Cand = SmallTownZoo.copy()
    
    if( Cand.shape[0] == 250 ):
        for cnd in Candidate:
            Cand[ cnd[1]][cnd[0]] = cnd[2]
        Cand = Cand.T
    else:
        for cnd in Candidate:
            Cand[ cnd[0]][cnd[1]] = cnd[2]
    Score = 0
    for ky in Key:
        if( Cand[ky[0]][ky[1]] == ky[2] ):
            Score += 1
        elif( abs(Cand[ky[0]][ky[1]] - ky[2]) <= 1  ):
            Score += 0.5
    Score = round(Score)
            
    msgString =  """<div style="border:solid black 2px;width:500px;padding:5px;"><b>Current Score: </b> %s percent  <p>&nbsp;</p>""" % round(Score,2) 
    if( Score < 50): 
        msgString += """<p>You might want to refine your methods.  </p> 

                Be sure that you remove na's first, and it needs to be solid.  Poor handling of na 
                will result in poor cosine similarity step."""
    elif( Score < 70):
        msgString += """<p>You're making progress. </p> 

                  You may still have issues in the na removal step.  Don't be afraid to tweak there also."""
    elif( Score < 90): 
        msgString += """<p>You're almost there.  Probably is <i>k</i> or the method in either Impute or Predict.</p>""" 
    else:
        msgString += """<p>Good Job!</p>""" 
    return HTML(msgString+"</div>")

from scipy import stats

class IG: 
    def norm( my, x, order = 2):
        tmp = logical_not( isnan(x)  ) 
        return norm( x[tmp], order )

    def correlation(my, x, y):
        tmp = logical_not( logical_or(isnan(x), isnan(y) ) ) 
        return corrcoef(x[tmp],y[tmp])[1,0]

    def mean( my, x ):
        tmp = logical_not( isnan(x)  ) 
        return mean( x[tmp] )
    
    def median( my, x):
        tmp = logical_not( isnan(x)  ) 
        return median( x[tmp] )
    
    def mode( my, x):
        tmp = logical_not( isnan(x)  ) 
        return stats.mode( x[tmp], axis=None)[0][0]

IgnoringNan = IG()

figsize(8,6)

def DisplayData2D( ClassData, kNNGraph = None ):
    "DisplayData2D( ClassData ) -> Scatter plot of Classifier 2D Data"
    
    m,n = ClassData.shape
    C0inds = []
    C1inds = []
    CUinds = {}
    ucnt = 0
    
    for i in range(m):
        if( isnan(ClassData[i,2]) ):
            CUinds[i] = chr( ord('A') + ucnt )
            ucnt += 1
        elif( ClassData[i,2] == 0 ):
            C0inds.append(i)
        else:
            C1inds.append(i)
     
    scatter( ClassData[C0inds,0], ClassData[C0inds,1], marker = '$0$', color='g', s=50)
    scatter( ClassData[C1inds,0], ClassData[C1inds,1], marker = '$1$', color='k', s=50)
    for i in CUinds.keys(): 
        scatter( ClassData[i,0], ClassData[i,1], marker = '$%s$' % CUinds[i], color='r', s=100)
    
    if( kNNGraph != None ):
        print("Scores for Unclassified based on mean class of k-nearest neighbors")
        for v in kNNGraph.nodes():
            for r in kNNGraph.neighbors(v):
                dx =  ClassData[r,0] - ClassData[v,0]
                dy =  ClassData[r,1] - ClassData[v,1]
                if( dx**2 + dy**2 > 0):
                    arrow( ClassData[v,0], ClassData[v,1],dx,dy, color='k', alpha=0.2, head_width=0.25, length_includes_head=True)
        for v in CUinds.keys():
            cnt0 = 0
            cnt1 = 0
            for r in kNNGraph.neighbors(v):
                if(not isnan(ClassData[r,2])):
                    if( ClassData[r,2] == 1 ):
                        cnt1 += 1
                    else:
                        cnt0 += 1
            if( cnt0 != cnt1 ):
                if( cnt1 > cnt0 ):
                    cls = 1
                else:
                    cls = 0
                
                print( "kNN prediction of %s for unclassified point %s at (%s, %s): votes: class0 = %s, class1 = %s" 
                        % ( cls, CUinds[v], ClassData[v,0], ClassData[v,1], cnt0, cnt1 ) )
            else:
                print( "kNN makes no prediction for unclassified point %s at (%s, %s)" % ( CUinds[v], ClassData[v,0], ClassData[v,1] ) )
             
n0 = 10
n1 = 10
nu =  5

Class0 = array( [ APM.randint(0,10, n0),    randint(0,10,n0), [0 for i in range(n0) ] ] )
Class1 = array( [ APM.randint(0,10, n1)+10, randint(0,10,n1), [1 for i in range(n1) ] ] )
ClassU = array( [ APM.randint(5,15,nu), randint(0,10,nu), [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+n1)] = Class1
Exdat[:,(n0+n1):] = ClassU

Example1 = DataFrame( Exdat.T, columns = ['x','y','class'] )

n0 = 20
n1 = 20
nu =  5

Class0 = array( [ APM.randint(0,15, n0),    randint(0,10,n0), [0 for i in range(n0) ] ] )
Class1 = array( [ sqrt(APM.randint(0,100, n1)+100), randint(0,10,n1), [1 for i in range(n1) ] ] )
ClassU = array( [ APM.randint(5,15,nu), APM.randint(0,10,nu), [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+n1)] = Class1
Exdat[:,(n0+n1):] = ClassU

Example2 = DataFrame( Exdat.T, columns = ['x','y','class'] )


n0 = 50
n1 = 50
nu =  5

DoubleDensity1 = APM.randint(8,20, 2*n1)-0.5
DoubleDensity1[n1:] = APM.randint( 8,15,n1 )
DDy = [ APM.randint(0,9)+ APM.rand() for i in range(2*n1)]

Class0 = array( [ APM.randint(4,13, n0),    randint(4,9,n0)-0.5, [0 for i in range(n0) ] ] )
Class1 = array( [ DoubleDensity1, DDy, [1 for i in range(2*n1) ] ] )
ClassU = array( [ APM.randint(8,12,nu), APM.randint(3,6,nu) + APM.randint(0,5,nu)*0.2 , [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+2*n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+2*n1)] = Class1
Exdat[:,(n0+2*n1):] = ClassU

Example3 = DataFrame( Exdat.T, columns = ['x','y','class'] )
Example3Data = Example3.as_matrix()

n0 = 50
n1 = 200
nu =  5

Class0 = array( [ [ (APM.rand()+ 7)*cos(2*pi*i/n0) for i in range(n0)], [ (APM.rand()+ 7)*sin(2*pi*i/n0) for i in range(n0)], [0 for i in range(n0) ] ] )
Class1 = array( [ [ (4*APM.rand()+ 2)*cos(2*pi*i/n1) for i in range(n1)], [ (4*APM.rand()+ 2)*sin(2*pi*i/n1) for i in range(n1)], [1 for i in range(n1) ] ] )
ClassU = array( [ [ (6.1+i/nu)*cos(2*pi*i/nu) for i in range(nu)], [ (6.1+i/nu)*sin(2*pi*i/nu) for i in range(nu)], [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+n1)] = Class1
Exdat[:,(n0+n1):] = ClassU

Exercise = DataFrame( Exdat.T, columns = ['x','y','class'] )
ExerciseData = Exercise.as_matrix()

    
def NormkNN(data_as_DataFrame, k = 5, order = 2 ):
    """NormkNN(data_as_DataFrame) -> norm distance k Nearest Neighbors directed graph with uniform outdegree of k

    Parameters are 

    k:  number of neighbors

    order: order of the norm
    """
    
    Data = data_as_DataFrame.as_matrix()
    m,n = Data.shape
    DistanceMatrix = zeros( shape = (m,m)  )  
    
    for i in range(m):
        for j in range(m):
            DistanceMatrix[i,j] = IgnoringNan.norm(  Data[i] - Data[j], order )
    
    DistanceData = [ (i,j,DistanceMatrix[i,j] )  for i in range(m) for j in range(i+1,m) ] 
    DistanceData = array( DistanceData, dtype = [ ('row1', int), ('row2', int), ( 'distance', float ) ] )
    ndarray.sort( DistanceData, order='distance' )
    
    ImputekNN = networkx.DiGraph()
    ImputekNN.add_nodes_from( list(range(m)) )
    
    for distdat in DistanceData:
        if ImputekNN.out_degree(distdat[0]) < k:
            ImputekNN.add_edge(distdat[0], distdat[1] )
        if ImputekNN.out_degree(distdat[1]) < k:   
            ImputekNN.add_edge(distdat[1], distdat[0] )
            
    return ImputekNN

def CosinekNN(Data, k = 5 ):
    """CosinekNN(Data) -> Cosine similarity k Nearest Neighbors directed graph with uniform outdegree of k

    Parameters are 

    k:  number of neighbors

    """
    
    m,n = Data.shape
    DistanceMatrix = zeros( shape = (m,m)  )  
    
    for i in range(m):
        for j in range(m):
            DistanceMatrix[i,j] = 1 - dot( Data[i],  Data[j] ) / norm(Data[i])/norm(Data[j])
    
    DistanceData = [ (i,j,DistanceMatrix[i,j] )  for i in range(m) for j in range(i+1,m) ] 
    DistanceData = array( DistanceData, dtype = [ ('row1', int), ('row2', int), ( 'distance', float ) ] )
    ndarray.sort( DistanceData, order='distance' )
    
    kNN = networkx.DiGraph()
    kNN.add_nodes_from( list(range(m)) )
    
    for distdat in DistanceData:
        if kNN.out_degree(distdat[0]) < k:
            kNN.add_edge(distdat[0], distdat[1] )
        if kNN.out_degree(distdat[1]) < k:   
            kNN.add_edge(distdat[1], distdat[0] )
            
    return kNN
 
 
def Impute(data_as_DataFrame, kNNGraph, Method = IgnoringNan.mean):
    """Impute(data_as_DataFrame,Graph) -> pandas DataFrame with nan's imputed
    
    Imputation is via Graph Neighborhoods of kNNGraph
    Method is applied to each neighborhood array of values for a 
    vertex with an nan
    """
    
    DFrame = data_as_DataFrame.copy()
    cols = DFrame.columns
    inds = DFrame.index
    Data = DFrame.as_matrix()
    
    m,n = DFrame.shape
    for i in range(m):
        nbrs = kNNGraph.neighbors(i)
        for j in range(n):
            if( isnan( Data[i,j] ) ):
                 DFrame.set_value( inds[i],cols[j], int( Method( array( [Data[nbr,j] for nbr in nbrs] ) ) ) )
    return DFrame
    
    
def Predict(ImputedData, Unrated, kNNGraph, Method = mean, PrintPredictions = 0 ):
    """Predict(Data, Unrated, kNNGraph) -> Data with Unrated replaced by predictions from using Graph Neighborhoods
    
    Method: Any method which returns a number given an array
    """
    apd = False
    if( ImputedData.shape[0] == 250  ):
        apd = True
     
    Ratings = []
    
    for unr in Unrated:
        unh = HouseholdIndex( unr[0] )
        una = AnimalIndex( unr[1] )
        
        nbrs = kNNGraph.neighbors( unh );
        if(apd):
            pred =  int( Method( array( [ ImputedData[nbr,una] for nbr in nbrs] ) ) )
            if(PrintPredictions > 0):
                PrintPredictions += -1
                print( "Household %s is predicted give animal exhibit %s a rating of %s" %(unr[0], unr[1], pred ) )
            Ratings.append( (unr[0], unr[1], pred ) )
        else:
            pred =  int( Method( array( [ ImputedData[una,nbr] for nbr in nbrs] ) ) )
            if(PrintPredictions > 0 ):
                PrintPredictions += -1
                print( "Household %s is predicted give animal exhibit %s a rating of %s" %(unr[0], unr[1], pred ) )
            Ratings.append( (unr[0], unr[1], pred ) )
        
    return Ratings
        


HTML(""" 
    <p>Several commands and structures have been added, including the following:</p>
    <p>The __View__ command can be used to produce detachable views of data sets</p>
    <p><b>SmallTownZoo</b> data is now loaded <br/>
    <b>HouseholdNames</b> and <b>AnimalNames</b> are loaded as lists of strings</p>
    <p>More details on additional commands within the notebook as needed</p>
    """)
    