//function toggleDisplay(obj,togClass,caller) 
//{
//	obj = document.getElementById(obj);
//
//	// Find the child containing the abstract
//	objChildren = obj.getElementsByTagName("div");
//	for(var i=0; i< objChildren.length; i++)
//		if( objChildren[i].className == togClass)
//			abstract = objChildren[i];
//
//	// Find the child node than needs to toggle
//	togTextNode = caller.getElementsByTagName("a")[0];
//
//
//	if(abstract.style.display == 'block'){
//		abstract.style.display = 'none';
//		togTextNode.className = "toggle_off";
//	}
//	else{
//		abstract.style.display = 'block';
//		togTextNode.className = "toggle_on";	
//	}
//
//}

//function readFile(file_path)
//{
//    //Retrieve the first (and only!) File from the FileList object
//    document.write("entering readFile");
//    document.write(file_path);
//    
//    var fileDisplayArea = document.getElementById('fileDisplayArea');
//    
////    var file = file_path.files[0];
//    
//    document.write("here0");
//    
//	var textType = /text.*/;
//    
//    document.write(file);
//
//	if (file.type.match(textType)) {
//        document.write("here0");
//        var reader = new FileReader();
//
//		reader.onload = function(e) {
//             document.write("here1");
//			fileDisplayArea.innerText = reader.result;
//		}
//        document.write("here2");
//        reader.readAsText(file);	
//    } 
//    else 
//    {
//	   fileDisplayArea.innerText = "File not supported!";
//    }
//    document.write("here3");
//}

function parse_paper_xml()
{  
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET","papers.xml",false,null,null);
    xmlhttp.send();

    xmlDoc=xmlhttp.responseXML;         
    
    var x=xmlDoc.getElementsByTagName("paper");
    var year = 0;
    for (i=0;i<x.length;i++)
    { 
        var key = x[i].getElementsByTagName("key")[0].childNodes[0].nodeValue; 
//        var abskey = "abs_";
//        abskey = abskey.concat(key);
//        var bibkey = "bib_";
//        bibkey.concat(key);
        
//        document.write(key);
        
        if(year != x[i].getElementsByTagName("year")[0].childNodes[0].nodeValue)
        {			
            year = x[i].getElementsByTagName("year")[0].childNodes[0].nodeValue;
            document.write("<h3>");
            document.write(x[i].getElementsByTagName("year")[0].childNodes[0].nodeValue);
            document.write("</h3>");
        }
        
        document.write("<div id=paper>");

        //document.write("<table><tr>"); 
        
                
        if(x[i].getElementsByTagName("img").length != 0)
        {            
			document.write("<td>");
			document.write("<img src='");
            document.write(x[i].getElementsByTagName("img")[0].childNodes[0].nodeValue);
			document.write("' width=100px />")
            document.write("</td>");
        }
//        else
//        {
//            document.write("images/index.png");
//        }
        
        document.write("<td><p><b>");
        document.write(x[i].getElementsByTagName("title")[0].childNodes[0].nodeValue);
        document.write("</b><br>");
        document.write(x[i].getElementsByTagName("author")[0].childNodes[0].nodeValue);
        document.write("<br>");  
        
        if(x[i].getElementsByTagName("conf").length != 0)
        {
            document.write("<em>");
            document.write(x[i].getElementsByTagName("conf")[0].childNodes[0].nodeValue);    
            document.write("</em><br>");        
        }
        
        if(x[i].getElementsByTagName("journ").length != 0)
        {
            document.write("<em>");
            document.write(x[i].getElementsByTagName("journ")[0].childNodes[0].nodeValue);    
            document.write("</em><br>");        
        }  
        
        if(x[i].getElementsByTagName("pdf").length != 0)
        {
            document.write("[<a target='_blank' href='");
            document.write(x[i].getElementsByTagName("pdf")[0].childNodes[0].nodeValue);
            document.write("'>paper</a>]");    
        }
        
        if(x[i].getElementsByTagName("pres").length != 0)
        {
            document.write("[<a target='_blank' href='");
            document.write(x[i].getElementsByTagName("pres")[0].childNodes[0].nodeValue);
            document.write("'>presentation</a>]");    
        }
        
        if(x[i].getElementsByTagName("poster").length != 0)
        {
            document.write("[<a target='_blank' href='");
            document.write(x[i].getElementsByTagName("poster")[0].childNodes[0].nodeValue);
            document.write("'>poster</a>]");    
        }
        
        if(x[i].getElementsByTagName("bibtex").length != 0)
        {
            document.write("[<a target='_blank' href='");
            document.write(x[i].getElementsByTagName("bibtex")[0].childNodes[0].nodeValue);
            document.write("'>bibtex</a>]");    
        }
        
        if(x[i].getElementsByTagName("doi").length != 0)
        {
            document.write("[<a target='_blank' href='");
            document.write(x[i].getElementsByTagName("doi")[0].childNodes[0].nodeValue);
            document.write("'>doi</a>]");    
        }
        
        if(x[i].getElementsByTagName("confsite").length != 0)
        {
            document.write("[<a target='_blank' href='");
            document.write(x[i].getElementsByTagName("confsite")[0].childNodes[0].nodeValue);
            document.write("'>conference</a>]");    
        }
        //document.write("</td></tr><tr><td>");
        
        if(x[i].getElementsByTagName("abstract").length != 0)
        {           
            document.write("<details><summary>Abstract</summary>");
//            readFile(x[i].getElementsByTagName("abstract")[0].childNodes[0].nodeValue);
            document.write(x[i].getElementsByTagName("abstract")[0].childNodes[0].nodeValue);            
            document.write("</details>");
        }
        
        //document.write("</td></tr>");
        //document.write("</table>");
        
        document.write("</div>");
    }
    
//    }    
}
