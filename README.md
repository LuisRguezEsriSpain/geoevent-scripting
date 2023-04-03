# geoevent-scripting

This reporitory includes several Python scripts to automate GeoEvent Tasks.

## ExtractGEComponents.py

This script extracts labels and names of inputs, outpus and GeoEvent services from a [GeoEvent configuration saved in XML file](https://enterprise.arcgis.com/es/geoevent/latest/administer/managing-configurations.htm).   
The output of this script can be used in next scripts.

You should change the variable *geoEventBackupFile* value to point to your GeoEvent configuration file.

## StartGEComponents.py

This script provides an automatic way to start GeoEvent inputs, outpus and services.

I got ideas from https://github.com/eironside/GeoEventRESTScripting to implement this script.

Changin the following line in StartGEComponent function   
   
`
inputURL = 'https://{0}:6143/geoevent/admin/{1}/{2}/start'.format(geoeventServer, component, geoeventComponent)
`  
    
to 
     
`
inputURL = 'https://{0}:6143/geoevent/admin/{1}/{2}/stop'.format(geoeventServer, component, geoeventComponent)
`   
   
you can develop an script to stop GeoEvent inputs, outpus and services.




