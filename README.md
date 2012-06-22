check_dcm.py
============
_Nagios/Icinga plugin to check DICOM services._

The script is a wrapper for dcmtk's (http://dicom.offis.de/dcmtk.php.en) echoscu
to monitor STORE SCP.  It will have to be installed (or the binary built) on the
nagios system. Easiest way on an ubuntu system is to use apt:

```sudo apt-get install dcmtk```

Usage:
You can hard code your port/ae_title but I prefer to use object variables as below
(http://nagios.sourceforge.net/docs/3_0/customobjectvars.html)

```
define command {
        command_name    check_dcm
        command_line    $USER1$/check_dcm -H $HOSTADDRESS$ -p $_HOSTPORT$ -a $_HOSTAE_TITLE$ -v
        }  
```