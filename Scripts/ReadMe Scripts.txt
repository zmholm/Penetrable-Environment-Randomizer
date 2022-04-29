----INFORMATION----

VMware allows users to add custom scripts to the guest OS when it is powered on. This useful feature is the backbone on adding randomized vulnerabilities to the VMs in this Program. Custom scripts can be made and used by this program, just add the file path to the scripts listbox. There are a few format constrants that follows. The word in the filename should be related to the system. Use the following variables to indicate what system the script is to function with:

1. WinServ - Script that is only ment for Windows Server systems
2. WinAll -  Script that is ment to work with both regular Windows systems and Windows Server systems
3. Win - Script that is only ment to function with regular windows systems
4. Linux - Script that functions with Linux Debian/Ubuntu systems

There are some simple example scripts found in the scripts folder in this directory. Custom scripts will only work if vmware tools is installed on the VM's. VMware custom scripts also do not work with NetWare, Windows NT, Windows ME, Windows 95, and Windows 98. Recommended to test and see if a custom script will run on the VM to see if it is supported. It is also important to note that there is a character limit for these scripts of 1,500. To get around this I recommend downloading a script from the internet and running it that way. Another limit is that the script has a timeout of 100 seconds. For DSU students, to get past the internet capcha, use these scripts made by mcutshaw : https://github.com/mcutshaw/cap-port-auth. Make sure to have the cap-port-auth on your templates before copying templates.

If you take a look at the blank templates, you can see two stages that are used in the customization script process with pre and post customization. The precustomizaiton variable happens before out-of-box customization begins. The postcustomization happens when the out-of-box customization finishes. The big factors at play are that there is no internet and some devices attached to the machine are not available in precustomization. In summary, postcustomization is favoriable in most cases and can do most of the same tasks.

----SOME HELPFUL RESOURCES----

- https://docs.vmware.com/en/VMware-Cloud-Director/9.7/com.vmware.vcloud.user.doc/GUID-655D00F0-CA72-48AB-BE8B-0FEACD84951A.html
- https://kb.vmware.com/s/article/1026614
- VMware vCloud Director Cookbook by Daniel Langenhan ISBN: 9781782177661

If you have made any scripts that you want to share, email me at zaneholmgren@live.com and I'll add it to the scripts on github