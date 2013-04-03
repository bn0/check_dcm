check_dcm.py
============
_Nagios/Icinga plugin to check DICOM services._

The script is a wrapper for the [dcmtk](http://dicom.offis.de/dcmtk.php.en "DCMTK") echoscu command to monitor STORE SCP. It will have to be installed (or the binary built) on the nagios system.  
The easiest way on an ubuntu system is to use apt:  

```sudo apt-get install dcmtk```

Usage:
------
```
check_dcm.py [-h] [-V] [-v] [-t TIMEOUT] [-aet [-aec AETITLE] [-H HOSTNAME] [-p PORT]  
optional arguments:
  -h, --help                        show help message and exit
  -V, --version                     display plugin version
  -v, --verbosity                   increase output verbosity.
  -t TIMEOUT, --timeout TIMEOUT     seconds before request timeout
  -aet AETITLE, --aetitle AETITLE   calling AE Title (default: ECHOSCU)
  -aec AETITLE, --call AETITLE      ae title of modality (default: ANY-SCP)
  -H HOSTNAME, --hostname HOSTNAME  hostname of modality
  -p PORT, --port PORT              tcp/ip port number of modality  
```

Nagios Usage:
-------------
You can hard code your port/ae_title but I prefer to use [object variables](http://nagios.sourceforge.net/docs/3_0/customobjectvars.html "Object Variables") as below:

```
define command {
        command_name    check_dcm
        command_line    $USER1$/check_dcm.py -H $HOSTADDRESS$ -p $_HOSTPORT$ -a $_HOSTAE_TITLE$ -v
        }  
```