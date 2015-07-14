## Doesn't yet work in Firefox for every possible argument (waiting for srcdoc -- Probably Oct 2013 in Firefox 25) 

## Tested on Chrome 28, Firefox 22, and Safari 5.1.7 on Windows 7 Home, Professional

from __future__ import division
from IPython.display import HTML
from pandas import DataFrame
import networkx


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



Businesses = ['ThriftyFoods', 'TownFoods', 'RiversAuto', 'ClothesInc', 'SmartMart', 'Acme', 'AceAuto', 'BigDeals', 'SavingsBank', 
              'TownTools', 'BestDeals', 'Wyres', 'JanesPlace', 'Bhardware', 'Biddles', 'Macs', 'Plumbers', 'LendersCU', 'FillerUp', 'GetItToGo']

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


def GraphFromCriteria(Vertices,CriteriaFunction):
    """GraphFromCriteria(Vertices,CriteriaFunction) -> networkx.Graph object
    
    The CriteriaFunction takes as arguments two vertices and returns 
    a boolean (either True or False).  If True, then edge is added to the 
    Graph
    """
    G = networkx.Graph()
    
    for i in range(len(Vertices)):
        for j in range(i+1,len(Vertices)):
            if( CriteriaFunction( Vertices[i],Vertices[j] ) ):
                G.add_edge(Vertices[i],Vertices[j])
    return G
            
def SubeconomyProblem(Username):
    'Returns Subeconomy Problem Data'
    
    if( Username == 'Lecture2'):
        APM = LcgRand( -685032576 )
    else:
        APM = LcgRand( hash( Username.lower() ) )
    Data = APM.randint(0,2,(250,20))
    
    ## Make a Subeconomy
    SubEconomy = []
    All = [i for i in range(250)]
    for i in range(APM.randint(50,80)): #Size of Subeconomy
        SubEconomy.append( All.pop( APM.randint(len(All)) ) )
    
    Se = SubEconomy[0]
    
    for j in SubEconomy:
        Data[j,:] = Data[Se,:]
    
    ## Two Income Households  
    for i in range(250):
        inds = []
        for j in range(20):
           if( Data[i,j] == 1 ): 
                inds.append(j)
        if( len(inds) == 0):
            tmp = APM.randint(1,21)
            Data[i,tmp] = 1
            Data[i, 2 ] = 1
            inds.append(2)
            inds.append(tmp)
         
        TwoIncome = APM.rand() <= 0.4
        
        earn = [ inds.pop( APM.randint( len(inds ) ) ) ]
        if(TwoIncome):
            earn.append( inds.pop( APM.randint( len(inds ) ) ) )
        else:
            earn.append( 40 )
        acc = 0
        for j in inds:
            if( j != earn[0] and j != earn[1] ):
                Data[i,j] = -APM.randint(5,21)*50
                acc += -Data[i,j]
        if( TwoIncome ):
            Data[i,earn[0]] = APM.randint( floor( acc / 40 ), floor( acc / 20 ) )*10
            Data[i,earn[1]] = acc - Data[i,earn[0]]  
        else:
            Data[i,earn[0]] = acc
    
    ## Add small transactions
    
    Smalltrans = 50
    ur = APM.randint(8,15)
    lr = APM.randint(1,4)
    
    for i in range(250):
        if( i in SubEconomy): 
            continue
        inds = []
        for j in range(2,20): #no grocery store changes
           if( Data[i,j] < 0 ): 
              inds.append(j)
        if( Data[i,1]==0 and Data[i,2] == 0 ):
            ind = inds.pop( APM.randint( len(inds) ) )
            Data[i,APM.randint(1,3)] = Data[i, ind ]
            Data[i, ind ] = 0
        if( 100*APM.rand() < Smalltrans and len(inds) > 1 ):
            A = inds.pop( APM.randint( len(inds) ) )
            B = inds.pop( APM.randint( len(inds) ) )
            tmp = -10*APM.randint(lr,ur)
            Data[i,A] = Data[i,A] + Data[i,B] -  tmp
            Data[i,B] = tmp
     
    # Including Subeconomy threshold corruption
         
    for i in SubEconomy:
        inds = []
        for j in range(20):
           if( Data[i,j] == 0 ): 
                inds.append(j) 
           if( Data[i,j] > 0 ):
                inc = j
        tmp1 = -10*APM.randint(3,8)
        tmp2 = -10*APM.randint(3,8)
        Data[i,inds.pop( APM.randint(len(inds) ) ) ] = tmp1  
        Data[i,inds.pop( APM.randint(len(inds) ) ) ] = tmp2
        Data[i,inc] += -(tmp1+tmp2)
        
    return Data, [ HouseholdNames[i] for i in SubEconomy]

FstEx, FstExkey = SubeconomyProblem('Lecture2')
SmallTownData = DataFrame( FstEx, index = HouseholdNames, columns = Businesses)

try:
    if( username == "Replace with Your Username"):
        raise 
    ASSN1, ASSN1key = SubeconomyProblem(username)
    Assignment1 = DataFrame( ASSN1, index = HouseholdNames, columns = Businesses)
    msg = "<b>Assignment1</b> is now loaded<br/>"
except:
    msg = "<b style = 'font-size:larger;color:red;'>ERROR:</b> <b>Assignment1</b> did not load!<br/>"
    print("Unable to produce the Assignment1 data.  Did you enter your username?")


def Grade(Candidate, IsExample = False):
    "Grade(Candidate) -> CandidatePercentageCorrect"
    
    if(IsExample):
        Key = FstExkey
    else:
        Key = ASSN1key
        
    try:
        tmp1 = set([Cd for Cd in Candidate])
        tmp2 = tmp1.intersection(Key)
        tmp3 = tmp1.intersection(set(range(250)).difference(Key)) # In candidate, but not in key
        Score = max( 10, ( len(tmp2)- max(3,len(tmp3))+3 )/len(Key) * 100 )
    except:
        print("The Candidate should be a list of Households, with each Household name in quotes" )
    
    tmp4 = len(Key) - len(Candidate)
    msgString =  """<div style="border:solid black 2px;width:500px;padding:5px;"><b>Current Score: </b> %s percent  <p>&nbsp;</p>""" % round(Score,2) 
    if( Score < 50): 
        msgString += """<p>You need to refine your methods.  Remember that the first row has index 0. </p> 

                Guessing is not going to help.  There are more than 50 households in the 
                subeconomy you are looking for.  Also, you are penalized for having more than 3 households in the candidate 
                that are not in the SubEconomy."""
    elif( Score < 70):
        msgString += """<p>You're making progress.  You've found more than half of your SubEconomy! </p> 

                  Perhaps your threshold should be higher (but not too high or you will get too many non-SubEconomy households in your answer. """
    elif( Score < 90): 
        msgString += """<p>You only have %s to go. Maybe time to tweak that threshold a bit more!</p>""" % tmp4
    else:
        msgString += """<p>Good Job!</p>""" 
    return HTML(msgString+"</div>")
    
HouseholdNames = array(HouseholdNames)
Businesses = array(Businesses)

formtext = """
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=10; chrome=1;">
<meta name="fragment" content="!">
<base target="_blank">
<title>Lecture2Submission</title>
</head>
<body>

<form action="https://docs.google.com/forms/d/1te99_xl4v54l7fDzPsXQ-urKAD0xruavxk4t3UMTdBU/formResponse" method="POST" id="ss-form" target="_self" onsubmit="">
	<p>
		Enter your username (just username, not entire email address):<br/>
		<input type="text" name="entry.1669260781" value="%s" id="entry_1669260781" >
	</p>
	<p>
		Enter your answer as a comma separated list (square brackets optional). <br/>
		<input type="text" name="entry.769226310" value="%s" class="ss-q-short" id="entry_769226310" >

	</p>
	<p>
		The following is the validation code generated from the enumber E%s.  <br/>
		<input type="text" name="entry.65036768" value="%s" class="ss-q-short" id="entry_65036768" readonly >
	</p>
	<p>
		<input type="hidden" name="draftResponse" value="[]">
		<input type="hidden" name="pageHistory" value="0">
		<input type="submit" name="submit" value="Submit" >
	</p>
</form>
</body>
"""

def Submit(Enumber,Answer):
    "Submit(Enumber,Answer) -> Submission form as popup"
    global username, formtext
    
    if( Enumber[0]=="E" or Enumber[0]=="e" ): #remove the "E"
        Enumber = Enumber[1:]
    
    #Create Validation
    SBM = LcgRand( hash(Enumber) )
    Validation = SBM.randint(0,100000,100)[99]
    
    #Format The Answer as comma separated values
    ans = ''
    for a in Answer:
        ans += '%s, ' % a
    ans = ans[:-2]
    
    FormWithEntries = formtext % (username, ans, Enumber, Validation)
    
    #Split into lines for the win_doc.writeln commands
    HTMLlist = FormWithEntries.split('\n')  
        
    HTMLtext = "' '"
    for line in HTMLlist:
        HTMLtext += ", '%s' " % line
 
    HtmlString  = """
           <script type='text/javascript'> 
                function LaunchForm() {
                   var iStringArray = [ %s ]
                   var win = window.open('about:blank', 'SubmissionForm' ,'height=500,width=800,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');
                   var win_doc = win.document;
                   win_doc.open();
                   win_doc.writeln('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HT'+'ML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><htm' + 'l>');
                   for (var i = 0; i < iStringArray.length; i++) {
                       win_doc.writeln( iStringArray[i] );
                   };
                   win_doc.writeln('</ht' + 'ml>');
                   win_doc.close();
                }
           </script>
           <p>You have entered </p>
           <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Username:</b> %s </p>
           <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Enumber:</b>  %s </p>
           <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Answer:</b> %s </p>
           <p>If this is correct, click on the button below: </p>
           <input type='button' value='Launch Submission Form' onclick='LaunchForm()'> 
        """ % ( HTMLtext, username, Enumber, ans)
               
    return HTML(HtmlString)


HTML("""    
    <p>The <b>View</b> command can be used to produce detachable views of data sets<br/>
    The <b>GraphFromCriteria</b> can be used to create a Networkx graph from a list of vertices and a criteria function.</p>

    <p><b>SmallTownData</b> is now loaded <br/>
    %s
    <b>HouseholdNames</b> and <b>Businesses</b> are loaded as arrays of strings</p>
    <p>The <b>Grade</b> command allows you to determine the grade that your candidate <br/> solution would receive if submitted</p>
    <p>The <b>Submit</b> command allows you to submit your answer. </p>
    <p>See course information (at course website) for details on grading</p>
    """ % msg)
    