
## Readme

This is a PoC to create Software Bill of Materials (SBOM) from Snyk using the Snyk API.
The SBOM generator works by getting all the dependencies of a project. 

A simple config file (sbom_generator.json) should accompany this.  

As this is just a PoC, the "Org token" can be obtained from the Snyk UI for a particular "organization". An org token can be taken by going to the settings for that org and copying it. The snyk_sbom_generator can then be run like this:

### Usage
python3 snyk_sbom_generator.py

### Requires
requires requests
