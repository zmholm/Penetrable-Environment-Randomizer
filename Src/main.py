import PySimpleGUI as sg
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.client import TaskStatus
from pyvcloud.vcd.test import TestCase
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vapp import VApp
import requests
import random
import time
import sys
import os


oslist = ["Windows10", "WinServ2019", "Debian", "Ubuntu"]
vulnlist = []

#the main window
col1 =      [
			[sg.Text("Enter the ip address of your organizations vCloud:"), sg.InputText("138.247.115.7", key="vcd_host", size=(15,4)), sg.Text("VDC:"), sg.InputText("Projects_Default", key="VDC", size=(15,4))],
			[sg.Text("Enter your credentials for your organization:"), sg.Text("Username:"), sg.InputText(key="Username", size=(15,4)), sg.Text("Password:"), sg.InputText(key='Password', size=(15,4), password_char='*'), sg.Text("Org:"), sg.InputText("Projects", key="Org", size=(15,4))],
            [sg.Text("Enter the name of the template of your vms:"), sg.InputText("Penenv project templates zmholmgren", key="template")],
			[sg.Text("Enter the name of the catalog that the template is found in:"), sg.InputText("Projects", key="catalog")],
			[sg.Text("Name of the vapp going to be created?"), sg.InputText(key="vappname")],
			[sg.Text("Number of VM's going to be created:"), sg.InputText(key="numvms", size=(4,4))],
			
			#[sg.Text("Select any aditional specific Server machines to the environment")],
            #[sg.Text("(This will add to the total number of machines in the environment)")],
            #[sg.Checkbox('DHCP'), sg.Checkbox('Active Directory'), sg.Checkbox('DNS'), sg.Checkbox('Webserver IIS'), sg.Checkbox('Webserver using Apache (Linux)'), sg.Checkbox('SQL')] #add further options after getting these done
            ]
col2 =      [
            [sg.Text("Select the VM's you want in the environment that are located in template:")],
            [sg.Listbox(values=oslist, size=(55,4), enable_events=True, key="oslistenv")],
            [sg.Button("Add OS"), sg.Input(key="oslistinput"), sg.Button("Remove OS")],
			[sg.Text("Select the vulnerabilites you want in the environment:")],
			[sg.Listbox(values=vulnlist, size=(55,4), enable_events=True, key="vulnlistenv")],
			[sg.Button("Add Script"), sg.Input(key="vulnlistinput"), sg.FileBrowse(), sg.Button("Remove Script")],
            ]
layout =    [
            [sg.Text("Welcome to the Penetrable Environment Randomizer",  justification='center', font=('helvetica', 20))],
            [sg.Column(col1), sg.Column(col2, element_justification='c')]
            ]
layout +=   [
            [sg.Button("Create Environment"), sg.Button("Test Connection"), sg.Button("Info"), sg.Button("Cancel")]
            ]

# Main window created
window = sg.Window("Penetrable Environment Randomizer", layout, resizable=True)

#disables self-signed certificate warnings
requests.packages.urllib3.disable_warnings()


# loop for the window events
while True:
	event, values = window.read()
    
	if event == "Cancel" or event == sg.WIN_CLOSED:
		break
	elif event == "Add OS":
		oscheck = values["oslistinput"]
		if oscheck == '':
			sg.popup("The field for the VM Name is blank, please enter a name", title="Please Enter Name of VM")
		else:
			oslist.append(values["oslistinput"])
			window["oslistenv"].update(oslist)
	elif event == "Remove OS":
		removeitem = values["oslistinput"]
		if removeitem == '':
			sg.popup("The field for the VM Name is blank, please enter a name", title="Please Enter Name of VM")
		else:
			oslist.remove(removeitem)
			window["oslistenv"].update(oslist)
	elif event == "Add Script":
		vulncheck = values["vulnlistinput"]
		if vulncheck == '':
			sg.popup("The field for the Script path is blank, please enter a file path", title="Please Enter Path of Script")
		else:
			vulnlist.append(values["vulnlistinput"])
			window["vulnlistenv"].update(vulnlist)
	elif event == "Remove Script":
		removeitem = values["vulnlistinput"]
		if removeitem == '':
			sg.popup("The field for the Script path is blank, please enter a file path", title="Please Enter Path of Script")
		else:
			vulnlist.remove(removeitem)
			window["vulnlistenv"].update(vulnlist)
	elif event == "Info":
		Information = "Created by Zane Holmgren for the completion of studies at DSU\n"
		Information += "PySimpleGUI version: "
		Information += sg.version
		Information += "\n"
		Information += "Current Python version: "
		Information += sys.version
		Information += "\n"
		Information += "Directory of this program: "
		Information += os.path.dirname(__file__)
		Information += "\n"
		sg.popup(Information, title="Information")
	elif event == "Test Connection":
		testitem = values["vcd_host"]
		testitem1 = values["Username"]
		testitem2 = values["Org"]
		testitem3 = values["Password"]
		testitem4 = values["VDC"]
		if testitem == '':
			sg.popup("No IP address entered in please enter the information needed", title="Blank field")
		elif testitem1 == '':
			sg.popup("Username field is blank please enter the information needed", title="Blank field")
		elif testitem2 == '':
			sg.popup("Organizaiton field is blank please enter the information needed", title="Blank field")
		elif testitem3 == '':
			sg.popup("Password field is blank please enter the information needed", title="Blank field")
		elif testitem4 == '':
			sg.popup("VDC field is blank please enter the information needed", title="Blank field")
		else:
			vcd_host = values["vcd_host"]
			username = values["Username"]
			org = values["Org"]
			password = values["Password"]
			vdc = values["VDC"]
			client = Client(vcd_host,
					verify_ssl_certs=False,
					#log_file='pyvcloud.log', Log file disabled
					log_requests=True,
					log_headers=True,
					log_bodies=True)
			while True:
				try:
					client.set_highest_supported_version()
				except:
					sg.popup("Unable to connect to vCloud, check IP address field", title="failed connection")
					break
				try:
					client.set_credentials(BasicLoginCredentials(username, org, password))
				except:
					sg.popup("Unable to login", "please check your credentials", title="Unable to Login")
					break
				org_resource = client.get_org()
				org = Org(client, resource=org_resource)
				vdc_resource = org.get_vdc(vdc)
				vdc = VDC(client, resource=vdc_resource)
				try:
					vdc.create_vapp(name = "testconnect",
					description = 'Created by PenEnv',
					network = 'vCloud_Internet',
					accept_all_eulas = True)
				except:
					sg.popup("Able to login, but unable to create a test vapp", "Either permission is not allowed or a vapp called testconnect is already made", title="Unable to create test vapp")
					break
				time.sleep(15)
				vapp_resource = vdc.get_vapp("testconnect")
				vapp = VApp(client, resource=vapp_resource)
				powerstate = vapp.get_power_state()
				while powerstate == 0:
					vapp.reload()
					powerstate = vapp.get_power_state()
					if powerstate == -1:
						sg.popup("Unable to create the vapp needed", title="Create vapp task failed")
						break
					elif powerstate == 1:
						break
					time.sleep(5)
				try:
					vdc.delete_vapp(name = "testconnect", force=True)
				except:
					sg.popup("Unable to delete the test vapp created", title="Unable to delete vapp")
					break
				sg.popup("Was able to login and create a vapp", title="Test successful")
				client.logout()
				break
	elif event == "Create Environment":
		sg.popup("This will take some time so be patient, do not exit or force exit while this operation is running", title="Creating Environment")
		testitem = values["vappname"]
		testitem1 = values["vcd_host"]
		testitem2 = values["Username"]
		testitem3 = values["Org"]
		testitem4 = values["Password"]
		testitem5 = values["VDC"]
		testitem6 = values["numvms"]
		testitem7 = values["template"]
		testitem8 = values["catalog"]
		if testitem == '':
			sg.popup("No vapp name entered in please enter the information needed", title="Blank field")
		elif testitem1 == '':
			sg.popup("No IP address entered in please enter the information needed", title="Blank field")
		elif testitem2 == '':
			sg.popup("Username field is blank please enter the information needed", title="Blank field")
		elif testitem3 == '':
			sg.popup("Organizaiton field is blank please enter the information needed", title="Blank field")
		elif testitem4 == '':
			sg.popup("Password field is blank please enter the information needed", title="Blank field")
		elif testitem5 == '':
			sg.popup("VDC field is blank please enter the information needed", title="Blank field")
		elif testitem6 == '':
			sg.popup("Number of vms field is blank please enter the information needed", title="Blank field")
		elif testitem7 == '':
			sg.popup("Template field is blank please enter the information needed", title="Blank field")
		elif testitem8 == '':
			sg.popup("Catalog field is blank please enter the information needed", title="Blank field")
		elif len(oslist) == 0:
			sg.popup("No items in the OS list for VMs please enter the information needed", title="Blank field")
		elif len(vulnlist) == 0:
			sg.popup("No items in the vulnerability scripts list, please add scripts appropriate for the OS's chosen", title="Blank field")
		else:
			vappname = values["vappname"]
			vcd_host = values["vcd_host"]
			username = values["Username"]
			org = values["Org"]
			password = values["Password"]
			vdc = values["VDC"]
			numvms = values["numvms"]
			templatename = values["template"]
			catalogname2 = values["catalog"]
			client = Client(vcd_host,
					verify_ssl_certs=False,
					#log_file='pyvcloud.log',
					log_requests=True,
					log_headers=True,
					log_bodies=True)
			while True:
				try:
					client.set_highest_supported_version()
				except:
					sg.popup("Unable to connect to vCloud, check IP address field", title="failed connection")
					break
				try:
					client.set_credentials(BasicLoginCredentials(username, org, password))
				except:
					sg.popup("Unable to login", "please check your credentials", title="Unable to Login")
					break
				org_resource = client.get_org()
				org = Org(client, resource=org_resource)
				vdc_resource = org.get_vdc(vdc)
				vdc = VDC(client, resource=vdc_resource)
				try:
					#creates the vapp
					vdc.create_vapp(name = vappname,
					description = 'Created by PenEnv',
					network = 'vCloud_Internet',
					accept_all_eulas = True)
				except:
					sg.popup("Unable to create the desired vapp, check permissions or for duplicate vapp names", title="Unable to create vapp")
					break
				vapp_resource = vdc.get_vapp(vappname)
				vapp = VApp(client, resource=vapp_resource)
				
				time.sleep(15)
				
				#checks to see if vapp is created successfully
				powerstate = vapp.get_power_state()
				while powerstate == 0:
					vapp.reload()
					powerstate = vapp.get_power_state()
					if powerstate == -1:
						sg.popup("Unable to create the vapp needed", title="Create vapp task failed")
						break
					elif powerstate == 1:
						sg.popup("Vapp was created successfully", title="Vapp created successfuly")
						break
					time.sleep(5)
				
				#create a kali vm
				try:
					catalog_item = org.get_catalog_item(catalogname2,
						templatename)
				except:
					sg.popup("Was unable to find the catalog templete, please check template name and catalog name", title="Unable to find template")
					break
				source_vapp_resource = client.get_resource(
					catalog_item.Entity.get('href'))
				#Required parameters
				spec = {'source_vm_name': "Kali",
					'vapp': source_vapp_resource}
				#Optional parameters
				spec['target_vm_name'] = "Kali"
				spec['hostname'] = "Kali"
				#spec['storage_profile'] = 'vCloud-Cluster (VDC Default)'
				#spec['network'] = None
				vms = [spec]
				try:
					result = vapp.add_vms( vms,
						deploy = True,
						power_on = True,
						all_eulas_accepted = True)
				except:
					sg.popup("Unable to create the kali vm required in environment, make sure the template you are are using has a vm called 'Kali'", title="unable to create kali vm")
					break
				
				time.sleep(60)
				vapp.reload()
				powerstate = vapp.get_power_state()
				while powerstate == 0 or powerstate == 7 or powerstate == 6 or powerstate == 10:
					vapp.reload()
					powerstate = vapp.get_power_state()
					if powerstate == -1:
						sg.popup("Unable to create the Kali VM needed", title="Unable to Create Kali VM")
						break
					elif powerstate == 4:
						sg.popup("Kali VM was created successfully", title="Kali VM created")
						break
					time.sleep(5)
				
				#IN THE FUTURE ADD SPECIAL VMS HERE
				numvms2 = int(numvms)
				numvms2 += 1
				vmnames = []
				for x in range(1, numvms2):
					b = int(x)
					c = str(b)
					temnam = 'vm' + c
			
					oschosen = random.choice(oslist)
				
					if "Windows" in oschosen:
						y = 0
						while y == 0:
							scriptchoice = random.choice(vulnlist)
							if "Windows" in scriptchoice:
								scriptfile = open(scriptchoice, "r")
								scriptdata = scriptfile.read()
								scriptfile.close()
								y += 1
							if "WinAll" in scriptchoice:
								scriptfile = open(scriptchoice, "r")
								scriptdata = scriptfile.read()
								scriptfile.close()
								y += 1
					if "WinServ" in oschosen:
						y = 0
						while y == 0:
							scriptchoice = random.choice(vulnlist)
							if "WinServ" in scriptchoice:
								scriptfile = open(scriptchoice, "r")
								scriptdata = scriptfile.read()
								scriptfile.close()
								y += 1
							if "WinAll" in scriptchoice:
								scriptfile = open(scriptchoice, "r")
								scriptdata = scriptfile.read()
								scriptfile.close()
								y += 1
					if "Debian" in oschosen:
						y = 0
						while y == 0:
							scriptchoice = random.choice(vulnlist)
							if "Linux" in scriptchoice:
								scriptfile = open(scriptchoice, "r")
								scriptdata = scriptfile.read()
								scriptfile.close()
								y += 1
					if "Ubuntu" in oschosen:
						y = 0
						while y == 0:
							scriptchoice = random.choice(vulnlist)
							if "Linux" in scriptchoice:
								scriptfile = open(scriptchoice, "r")
								scriptdata = scriptfile.read()
								scriptfile.close()
								y += 1
		
					#Required parameters
					spec = {'source_vm_name': oschosen,
						'vapp': source_vapp_resource}
					#Optional parameters
					spec['target_vm_name'] = temnam
					spec['hostname'] = temnam
					#spec['storage_profile'] = 'vCloud-Cluster (VDC Default)'
					#spec['network'] = None
					spec['cust_script'] = scriptdata
					#Custom script needs to be in a string format for it to work properly
			
					vms = [spec]
					try:
						result = vapp.add_vms( vms,
							deploy = True,
							power_on = True,
							all_eulas_accepted = True)
					except:
						sg.popup("Was unable to create ", temnam, title="Error creating vm")
					time.sleep(60)
				
					vapp.reload()
					powerstate = vapp.get_power_state()
					while powerstate == 0 or powerstate == 7 or powerstate == 6 or powerstate == 10:
						vapp.reload()
						powerstate = vapp.get_power_state()
						if powerstate == -1:
							popmes = "Unable to create "
							popmes += temnam
							sg.popup(popmes, title=popmes)
							break
						elif powerstate == 4:
							popmes = temnam
							popmes += " was created successfully"
							poptitle = temnam
							poptitle += "created successful"
							sg.popup(popmes, title=poptitle)
							break
						time.sleep(5)

				sg.popup("Task has finished creating the environment", title="Task Completed")
				
				client.logout()
				
				break
		
window.close()