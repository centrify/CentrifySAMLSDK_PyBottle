# CentrifySAMLSDK_PyBottle

This is an example on adding SAML to your Python web application (This example uses Bottle but the code will work with any framework). 

This example was created using Python 3.4.3.
To use this demo from Visual Studio you will need to install PTVS (project files included. Other IDE's can be used as well)
This code uses lxml to parse the SAML XML. lxml can be installed via pip (python pip lxml) on Linux and Mac, or by compiling on PC. There are also unoffical binaries compiled with a windows installer that could be used.
This code uses SignXML to validate the SAML Assertions. This can be installed via pip (Windows: python -m pip signxml, Other: python pip signxml) from eiher a console or Visual Studio.

You will need a Signing Certificate from a Centrify Generic SAML Application, and the endpoint URL's from the Centrify Generic SAML Application.

To use this example:

In the Centrify Cloud Manager, click on Apps, New App, Custom, Generic SAML Application.

In the Centrify Cloud Manager, in the Generic SAML Application settings, click Download Certificate under Application Settings.

In the Centrify Cloud Manager, in the Generic SAML Application settings, copy the Identity Provider URL under Application Settings.

In Visual Studio, remove the sample Signing Certificate in the project and replace it with the Certificate downloaded from the Generic SAML Application.

In Visual Studio, modify the SAMLSDK_PyBottle.py file and make sure the ACS Url, Isser, and Identity Provider URL variables match the URL's from the Centrify Cloud Manager.

In the Centrify Cloud Manager, in the Generic SAML Application settings, make the ACS URL the URL to your localhost and the ACS.aspx page (example would be http://localhost:6321/acs). 

In the Centrify Cloud Manager, deploy the Generic SAML Application.

Click debug in Visual Studio. If you navigate to http://localhost:6321/, you will start SP Initiated SAML SSO. If you go the User Portal and click the Generic SAML Application you will start IDP Initiated SAML SSO.
