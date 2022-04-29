Created By Zane Holmgren in credit for completion of studies at DSU
With the help of and under guidance of Andrew Kramer

----INSTRUCTIONS----

This application was built as a training/testing tool as well as for competitions.

-This application can be run using the penenv executable or penenv.exe
-Fill out correct information in the fields (most of the standard information for DSU students are automatically filled)
-Click "Test Connection" to see if you have the corrent information and have the right user privledges
-Add or remove vms from the choice of template vapp (one vm name can create multiple or no vms, this program chooses randomly from the list)
-Add scripts to be applied on specific vms (scripts are currently required for the program to work, if you want blank vms use a blank script)
-Click "Create Environment" to create the vapp (Please be patient, this can take several minutes depending on how many vms are being created)
-After a few minutes you should get a popup that the environment has been created successfully

DSU Users - Please refrain from spamming this tool or clogging university resources. Once done with usage, please shutdown and delete the vapps created by you.
If the script has not ran or changed the new vm during its first power on, then you will have to shutdown the vm and run "Power On, Force Recustomization" on the vcloud site.

----CREATING TEMPLATE VMS----

This program is run by taking templates and adding a script to them.

When making your own template
-Make sure to install fully and add or customize the template overall
-Make sure to install vmware tools, otherwise scripts will not run
-For linux machines, sometimes the scripting customization is not enabled by default. The command to view the status is 'vmware-toolbox-cmd config get deployPkg enable-custom-scripts', if it needs to be enables use the command 'vmware-toolbox-cmd config set deployPkg enable-custom-scripts true'
-Make sure that the machine will work with all selected script types
-Make sure that the vm and template are able to be customized

----EDITING----

This program is open source, allowing users to see and modify source code.

packages used and needed for editing and testing yourself:
-pysimplegui  -  can be installed using the command "py -m pip install pysimplegui"
-pyvcloud - can be installed using the command "py -m pip install pyvcloud"
These commands can differ on python versions as well as differnt OS's

The source code can be found in the Src foulder as main.py.

----ADDING SCRIPTS----

For more information on creating your own scripts look at the ReadMe Scripts in the scripts folder.

more to come soon!