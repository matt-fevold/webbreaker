# Cheatsheet of WebBreaker Commands

## WebInspect Scan

    Basic WebInspect scan:
    webbreaker webinspect scan --settings important_site_auth

    Basic WebInspect scan using command line auth credentials (only needed if authentication is enable in config.ini):
    webbreaker webinspect scan --settings important_site_auth --username $WEBINSPECT_USER --password $WEBINSPECT_PASSWORD

    WebInspect Scan with Scan overrides:
    webbreaker webinspect scan --settings important_site_auth --allowed_hosts example.com --allowed_hosts m.example.com

    Scan with absolute path to your local WebInspect settings:
    webbreaker webinspect scan --settings /Users/Matt/Documents/important_site_auth
    
## WebInspect List
    # List all WebInspect servers configured in config.ini:
    webbreaker webinspect servers

    # List all WebInspect scans on webinspect-1.example.com and webinspect-2.example.com:
    webbreaker webinspect list --server webinspect-1.example.com:8083 --server webinspect-2.example.com:8083

    # List all WebInspect scans on webinspect-1.example.com and webinspect-2.example.com matching "important_site":
    webbreaker webinspect list --server webinspect-1.example.com:8083 --server webinspect-2.example.com:8083 --scan_name important_site

    # List all WebInspect scans on all servers:
    webbreaker webinspect list

    # List all WebInspect scans on all servers matching "important_site":
    webbreaker webinspect list --scan_name important_site

    # List all WebInspect scans on all servers using command line auth credentials:
    webbreaker webinspect list --username $WEBINSPECT_USER --password $WEBINSPECT_PASSWORD

## WebInspect Download

    # Download WebInspect scan from server or sensor:
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth

    # Download WebInspect scan from server with credentials (only needed if authentication is enable in config.ini):
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth --username $WEBINSPECT_USER --password $WEBINSPECT_PASSWORD

    # Download WebInspect scan as XML:
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth -x xml

    # Download WebInspect scan by ID:
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth --scan_id my_important_scans_id   

## WebInspect Proxy 
    
    # Start a WebInspect proxy called test-proxy on port 9001
    webbreaker webinspect proxy --start --proxy_name test-proxy --port 9001

    # List all the WebInspect proxies
    webbreaker webinspect proxy --list

    # Download the WebInspect proxy webmacro called test-proxy
    webbreaker webinspect proxy --download --webmacro --proxy_name test-proxy

    # Download the WebInspect proxy settings file called test-proxy
    webbreaker webinspect proxy --download --setting --proxy_name test-proxy

    # Upload a WebInspect webmacro proxy for a scan override called
    webbreaker webinspect proxy --upload test-proxy.webmacro --proxy_name test

    webbreaker webinspect proxy --stop --proxy_name test

## Fortify SSC

    # List Fortify SSC Applications/Projects (NOTE: credentials need to be set from the admin commands)
    webbreaker fortify list

    # List Fortify SSC versions by application (case sensitive):
    webbreaker fortify list --application WEBINSPECT

    # Upload scan to Fortify SSC with command-line authentication (NOTE: Application or Project is taken from config.ini):
    webbreaker fortify upload --version important_site_auth --scan_name example_scan

    # Upload scan to Fortify SSC with application/project & version name:
    webbreaker fortify upload --application my_other_app --version important_site_auth --scan_name auth_scan

    # Download lastest .fpr scan from Fortify SSC from a specific application/project & version name:
    webbreaker fortify download --application my_other_app --version important_site_auth

    # Download lastest .fpr scan from Fortify SSC with application/project configured in config.ini:
    webbreaker fortify download --version important_site_auth

    # Download lastest .fpr scan from Fortify SSC with application/project & version name and command-line authentication:
    webbreaker fortify download --fortify_user $FORT_USER --fortify_password $FORT_PASS --application my_other_app --version important_site_auth
    
## ThreadFix

    # List all applications for all teams found in ThreadFix
    webbreaker threadfix list

    # List all applications with names containing 'secret' for all teams with names containing 'Marketing'
    webbreaker threadfix list --team Marketing --application MyApp

    # List all ThreadFix applications for the Marketing team
    webbreaker threadfix list --team Marketing

    # Upload the local file 'my_app_scan.xml' as a scan to the application with ID=345
    webbreaker threadfix upload --application MyApp --scan_file my_app_scan.xml

    # Upload the local file 'my_app_scan.xml' as a scan to the application with name Marketing_App
    webbreaker threadfix upload --application Marketing_App --scan_file my_app_scan.xml

    # Create a new application, with a given name and url, in ThreadFix under the Marketing team
    webbreaker threadfix create --team Marketing --application new_marketing_app --url http://marketing.example.com

## WebBreaker Administrative

    # Encrypt and store new Fortify SSC credentials. User will be prompted for username and password. 
    webbreaker admin credentials --fortify
    
    # Encrypt and store WebInspect credentials. User will be prompted for username and password. 
    webbreaker admin credentials --webinspect

    # Encrypt and store Fortify credentials as environment variables
    webbreaker admin credentials --fortify --username $FORT_USER --password $FORT_PASS

    Clear cuurent stored Fortify credentials.
    webbreaker admin credentials --fortify --clear
