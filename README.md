# PDF-Text-Redaction-Using-Google-Cloud
Google Cloud DLP does not support document redaction (PDF, DOC, TIFF etc...), We're supposed to redact only images using google cloud api's. In this python program we are going to redact documents using DLP API. 

<b><i>[You are always welcome to collaborate or suggest some changes, I'll be thankful]</i></b>

<b>Approach - </b>
  1. Convert every page of document into images using PyMuPDF(In Output Folder).    
      Output/<PDF_FILENAME>/Page0001.png    
      Output/<PDF_FILENAME>/Page0002.png    
      Output/<PDF_FILENAME>/Page0003.png    
      ...
  2. Redact every Page from that folder and generate output in Redacted Images folder.    
      Output/<PDF_FILENAME>/Redacted Images/Redacted-Page0001.png    
      Output/<PDF_FILENAME>/Redacted Images/Redacted-Page0002.png    
      Output/<PDF_FILENAME>/Redacted Images/Redacted-Page0003.png    
      ...
  3. Create PDF from all images in Redacted Images folder and store in base of Output.    
      Output/<PDF_FILENAME>/Redacted-<FILENAME>    
  
  
<b>Requirements - </b>
  1. PyMuPDF
  2. google.cloud.dlp
  3. Project Credentials (You have to download json from Google Cloud Console)
  4. Project Name (Name of Project on your Google Cloud Console)
  
<b>Installation -  </b>   
  1. PyMuPDF  
    <code>pip install PyMuPDF</code>
  2. Google Cloud DLP    
    <code>pip install google.cloud.dlp</code>
  
  <b>Executing The Program</b>
  <br>
  
  >python redaction.py <PDF_FILE_PATH>
  
  
<br>
That's It. Enjoy !!!
  
  
  
