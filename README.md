# auto_osint
quick auto OSINT tool to bring together several other tools


OSINT Script 

Installation 

Copy the “auto_osint_v1.x.x.tar.gz” file to your Kali VM. This ideally needs to be ran locally as running from the AWS boxes causes issues with logging into LinkedIn. Use the tar command to extract the archive to the current directory. 

$ tar xvf ./auto_osint_v1.x.x.tar.gz 

 

Run the installation script to install the OSINT tools and any needed dependencies. Afterwards close and re-open your terminal or restart your current shell. 

$ bash ./setup.sh 

 

Usage 

This script will automatically run each OSINT tool, saving the output into the correct folders and pausing for you to take screenshots of each step. The basic command usage is as follows: 

$ auto_osint --name 'CompanyName' --domain 'companyname.com' --linkedin 'company-name' 

 

The for the name, use the same name used for the Monday.com project. The domain name can often be found in the "About" section of the company LinkedIn profile. The LinkedIn name comes from the URL on the company page. 

Graphical user interface, application

Description automatically generated 

When running the script, the first step (linkedin2username) can sometimes fail on login. If this happens press ctrl+c on your keyboard to kill the script. Then open a browser, sign out and back into the linkedin.com website and try again. 

Once done, copy the newly created OSINT folder along with each of your screenshots into the proper project folder within SharePoint. 
