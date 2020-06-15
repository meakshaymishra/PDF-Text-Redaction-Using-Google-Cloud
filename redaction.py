# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample app that uses the Data Loss Prevent API to redact the contents of
an image file."""

from __future__ import print_function

import argparse
import fitz
from shutil import rmtree

# [START dlp_redact_image]
import mimetypes

# [END dlp_redact_image]
import os




# [START dlp_redact_image]
credential_path = "..\Google-Account-Key\Project-VisionAPI-a180ff956953.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
#os.environ['PROJECT_ID']="project-visionapi"


def redact_image(
    project,
    filename,
    #output_filename,
    info_types,
    custom_regexes=None,
    min_likelihood=None,
    mime_type=None,
):
    """Uses the Data Loss Prevention API to redact protected data in an image.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        filename: The path to the file to inspect.
        output_filename: The path to which the redacted image will be written.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        mime_type: The MIME type of the file. If not specified, the type is
            inferred via the Python standard library's mimetypes module.
    Returns:
        None; the response from the API is printed to the terminal.
    """


    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
            "regex": {"pattern": "[\d]"},
        }
        for i, custom_regex in enumerate(custom_regexes)
    ]
    

    # Prepare image_redaction_configs, a list of dictionaries. Each dictionary
    # contains an info_type and optionally the color used for the replacement.
    # The color is omitted in this sample, so the default (black) will be used.
    image_redaction_configs = []

    if info_types is not None:
        for info_type in info_types:
            image_redaction_configs.append({"info_type": info_type})

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "min_likelihood": min_likelihood,
        "info_types": info_types,
        "custom_info_types":[
    {
                        "info_type":{
                        "name":"PONumber"
                        },
                        "regex":{
                        "pattern":"[\d]"
                        },
                        "likelihood":"POSSIBLE",
                                               
                    }
    ]
    }

    pdffile = filename
    fileName = os.path.basename(pdffile)
    doc = fitz.open(pdffile)
    os.makedirs("output/"+fileName+"/pdftoImage",exist_ok = True)
    os.makedirs("output/"+fileName+"/redactedImage", exist_ok = True)
    numPages = doc.pageCount    #number of page
    print("Your document has "+str(numPages)+" pages.")
    for pageNum in range(numPages):
        page = doc.loadPage(pageNum) 
        pix = page.getPixmap()
        output = "output/"+fileName+"/pdftoImage/page"+str(pageNum).zfill(3)+".png"
        pix.writePNG(output)
        pageNum = pageNum+1

    # If mime_type is not specified, guess it from the filename.
    imgdir = "output/"+fileName+"/pdftoImage"
    imglist = os.listdir(imgdir)
    imgcount = len(imglist)  # pic count

    for i, f in enumerate(imglist):
        filename = os.path.join(imgdir, f)
        #print(filename)
        if mime_type is None:
            mime_guess = mimetypes.MimeTypes().guess_type(str(filename))
            mime_type = mime_guess[0] or "application/octet-stream"

        # Select the content type index from the list of supported types.
        supported_content_types = {
            None: 0,  # "Unspecified"
            "image/jpeg": 1,
            "image/bmp": 2,
            "image/png": 3,
            "image/svg": 4,
            "text/plain": 5,
        }
        content_type_index = supported_content_types.get(mime_type, 0)

        # Construct the byte_item, containing the file's byte data.
        with open(str(filename), mode="rb") as f:
            byte_item = {"type": content_type_index, "data": f.read()}
        #byte_item = encoded_string
        # Convert the project id into a full resource id.
        parent = dlp.project_path(project)

        # Call the API.
        response = dlp.redact_image(
            parent,
            inspect_config=inspect_config,
            image_redaction_configs=image_redaction_configs,
            byte_item=byte_item,
        )

        # Write out the results.
        output_filename = "output/"+fileName+"/redactedImage/"+os.path.basename(filename)
        with open(output_filename, mode="wb") as fn:
            fn.write(response.redacted_image)
        print("Redacted Page : "+str(i+1))

        '''    
        print(
            "Wrote {byte_count} to {filename}".format(
                byte_count=len(response.redacted_image), filename=output_filename
            )
        )
        '''
    doc.close()
    docBuild = fitz.open()
    doc=docBuild
    redactedimgdir = "output/"+fileName+"/redactedImage"
    redactedimglist = os.listdir(redactedimgdir)
    redactedimgcount = len(redactedimglist)  # pic count

    for i, f in enumerate(redactedimglist):
        img = fitz.open(os.path.join(redactedimgdir, f))  # open pic as document
        #print(os.path.join(redactedimgdir, f))
        #print(os.path.join(redactedimgdir, f))
        rect = img[0].rect  # pic dimension
        pdfbytes = img.convertToPDF()  # make a PDF stream
        img.close()  # no longer needed
        imgPDF = fitz.open("pdf", pdfbytes)  # open stream as PDF
        page = doc.newPage(width = rect.width,  # new page with ...
                           height = rect.height)  # pic dimension
        page.showPDFpage(rect, imgPDF, 0)  # image fills the page
    doc.save("output/"+fileName+"/Redacted-"+fileName+".pdf")
    print("Document generated Successfully in "+"output/"+fileName+"/Redacted-"+fileName)
    # If you wish to see redacted images and page images of pdf you can comment or remove below 2 lines
    #rmtree("output/"+fileName+"/redactedImage")
    #rmtree("output/"+fileName+"/pdftoImage")
        



# [END dlp_redact_image]


if __name__ == "__main__":
    default_project = os.environ.get("GCLOUD_PROJECT")

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("filename", help="The path to the file to inspect.")
    '''
    parser.add_argument(
        "output_filename",
        help="The path to which the redacted image will be written.",
    )
    '''
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default="project-visionapi"
,
    )
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS","DATE", "GENDER", "GENERIC_ID", "PHONE_NUMBER"],
    )

    parser.add_argument(
    	"--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default="[0-9]{1-6}",
    )
    parser.add_argument(
        "--min_likelihood",
        choices=[
            "LIKELIHOOD_UNSPECIFIED",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        ],
        help="A string representing the minimum likelihood threshold that "
        "constitutes a match.",
    )
    parser.add_argument(
        "--mime_type",
        help="The MIME type of the file. If not specified, the type is "
        "inferred via the Python standard library's mimetypes module.",
    )

    args = parser.parse_args()

    redact_image(
        args.project,
        args.filename,
        #args.output_filename,
        args.info_types,
        custom_regexes=args.custom_regexes,
        min_likelihood=args.min_likelihood,
        mime_type=args.mime_type,
    )
