# DMC VIDoc Documentation

This repository contains the code to generate Confluence Documentation based off of LabVIEW source files.

This uses a g-cli call in the form:

```
g-cli (optional)--lv-ver [LV_Year] (optional)--timeout [ms Timeout] "DMC VIDoc Confluence" -- [arguments]
```

This must be called from the working directory you want to analyze.

## Required Arguments

- **-pageid** | Page ID for the top level Confluence Page that documentation will be generated under

## Optional Arguments
- **-settings** | absolute or relative to working directory relative path to Doc Settings file. Defaults to Default.json included with app
- **-git** | Flag to include Git History in the documentation
- **-gittype** | Indicates which Git repo type the Git History would check. Defaults to GitLab, also allows GitHub and BitBucket
- **-source** | comma separated string of all relative file paths within working directory to include. Recursive search. Defaults to whole working directory
- **-c-settings** | Flag to indicate use the Confluence connection settings from within the Doc Settings File
- **-c-ini** | Flag to indicate using the Login INI file for Confluence connections
- **-c-dc** | Indicates Confluence type. If flag present then uses Data Center, otherwise uses Cloud
- **-url** | Confluence URL
- **-email** | Confluence Email
- **-token** | Confluence Access Token
- **-scoped** | Indicates if Access Token is Scoped or Unscoped
- **-help** | Returns this help information

## Example Use Cases

### Basic on-computer use (GitHub)
Running from a computer command line. Assuming VIDoc Settings file resides in root directory containing Confluence login information. 
```
cd <Root Code Directory>
g-cli "DMC VIDoc Confluence" -- -pageid <Parent Confluence Page ID> -settings "VIDoc Settings.json" -gittype "GitHub" -source "Source" -c-settings
```

### Basic on-computer use with login ini (GitLab)
Running from a computer command line. Assume Confluence Login INI has already been generated. (A prompt will ask for one if it has not yet). Uses default VIDoc Settings file.
```
cd <Root Code Directory>
g-cli "DMC VIDoc Confluence" -- -pageid <Parent Confluence Page ID> -source "Source" -c-ini -url "https://<company name>.atlassian.net/" -email "<user email>"
```

### CI/CD yaml call (GitHub)
Running from a powershell yaml pipeline. Uses an access token saved to a pipeline variable $token. Uses Confluence Data Center
```
g-cli "DMC VIDoc Confluence" -- -pageid $parentpageID -settings "VIDoc Settings.json" -c-dc -url "https://<company name>.atlassian.net/" -token $token
```

# Repo Page Finder Tool
A standalone command line tool to locate a Page ID for a specific named Page under a root Page. Was made for the intention of generating multiple sets of documentation under a single top level Page. Each child page would be the root for its documentation, with the name of the page matching the Repo Name. This would allow for standardizing of documentation location. 

Example:
- LabVIEW Documentation
  - Package 1 Documentation
  - Package 2 Documentation

It uses a g-cli call in the form

```
g-cli (optional)--lv-ver [LV_Year] (optional)--timeout [ms Timeout] "Repo Page Finder" -- [arguments]
```

## Required Arguments
- **-reponame** | Name of the repo to match to the Confluence Page
- **-pageid** | Page ID for the top level Confluence Page that repo page will be generated under

## Optional Arguments
- **-c-ini** | Flag to indicate using the Login INI file for Confluence connections
- **-c-dc** | Indicates Confluence type. If flag present then uses Data Center, otherwise uses Cloud
- **-url** | Confluence URL
- **-email** | Confluence Email
- **-token** | Confluence Access Token
- **-scoped** | Indicates if Access Token is scoped
- **-help** | Returns this help information

## Example Use Cases

### CI/CD Pipeline (GitLab)
Running this command will return the correct child page ID that is found that matches the Repo Name. If that page doesn't exist it will create it. 

```
g-cli "Repo Page Finder" -- -reponame $env:CI_PROJECT_NAME -pageid <top catagory page id> -url "https://<company name>.atlassian.net/" -email <service account email> -token $token
```

## Testing Powershell script
Use this as a powershell script to test out the functionality from a computer. Remove -scoped flag if the Access Token is a non-scoped one. Top Page ID is the parent page ID where all other repo documentation pages will be created under. Repo Name is the name of the Repo (would be replaced by $env:CI_PROJECT_NAME in a yaml).

```
$url = "https://<company>.atlassian.net/"
$email= "<email>>"
$token = "<Scoped Access Token>"
$toppageID = "<top page ID>"
$reponame = "<Repo Name>"

cd "<Repo/Code Root Directory>"
$repopageID = g-cli "Repo Page Finder" -- -reponame $reponame -pageid $toppageID -url $url -email $email -token $token -scoped
echo "Repo Page ID - $repopageID"
g-cli "DMC VIDoc Confluence" -- -pageid $repopageID -source "Source" -url $url -email $email -token $token -scoped
```

### 
# [Wiki Homepage](../../wikis/Home)

# Author(s), Contributors
* Jon Jay


# License
All software in this repository is licensed under the license found in [..\Build\License\](../master/Build/License/). 
