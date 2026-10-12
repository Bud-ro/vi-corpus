<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="13008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="IOScan.Faults" Type="Str"></Property>
		<Property Name="IOScan.NetVarPeriod" Type="UInt">100</Property>
		<Property Name="IOScan.Period" Type="UInt">10000</Property>
		<Property Name="IOScan.PowerupMode" Type="UInt">0</Property>
		<Property Name="IOScan.Priority" Type="UInt">9</Property>
		<Property Name="IOScan.ReportModeConflict" Type="Bool">false</Property>
		<Property Name="IOScan.StartEngineOnDeploy" Type="Bool">false</Property>
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Test Cell Controller (Program Files)" Type="Folder" URL="../Test Cell Controller (Program Files)">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="Test Cell Controller (ProgramData)" Type="Folder" URL="../Test Cell Controller (ProgramData)">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="NI VeriStand (Documents)" Type="Folder" URL="../NI VeriStand (Documents)">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="XML Writer.exe" Type="Document" URL="../XML Writer.exe"/>
		<Item Name="Post Build VI.vi" Type="VI" URL="../Post Build VI.vi"/>
		<Item Name="Get Latest Scan Build.vi" Type="VI" URL="../Get Latest Scan Build.vi"/>
		<Item Name="Migrate Installer To Current LabVIEW Version.vi" Type="VI" URL="../Migrate Installer To Current LabVIEW Version.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Close Panel.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/victl.llb/Close Panel.vi"/>
				<Item Name="Open Panel.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/victl.llb/Open Panel.vi"/>
				<Item Name="NI_FTP.lvlib" Type="Library" URL="/&lt;vilib&gt;/FTP/NI_FTP.lvlib"/>
				<Item Name="GetNamedSemaphorePrefix.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/GetNamedSemaphorePrefix.vi"/>
				<Item Name="RemoveNamedSemaphorePrefix.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/RemoveNamedSemaphorePrefix.vi"/>
				<Item Name="Semaphore Refnum Core.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Semaphore Refnum Core.ctl"/>
				<Item Name="Semaphore RefNum" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Semaphore RefNum"/>
				<Item Name="Release Semaphore Reference.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Release Semaphore Reference.vi"/>
				<Item Name="Not A Semaphore.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Not A Semaphore.vi"/>
				<Item Name="Semaphore Name &amp; Ref DB Action.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Semaphore Name &amp; Ref DB Action.ctl"/>
				<Item Name="Semaphore Name &amp; Ref DB.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Semaphore Name &amp; Ref DB.vi"/>
				<Item Name="Destroy Semaphore.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Destroy Semaphore.vi"/>
				<Item Name="Validate Semaphore Size.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Validate Semaphore Size.vi"/>
				<Item Name="AddNamedSemaphorePrefix.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/AddNamedSemaphorePrefix.vi"/>
				<Item Name="Obtain Semaphore Reference.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Obtain Semaphore Reference.vi"/>
				<Item Name="Get Semaphore Status.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Get Semaphore Status.vi"/>
				<Item Name="Create Semaphore.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Create Semaphore.vi"/>
				<Item Name="Release Semaphore.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Release Semaphore.vi"/>
				<Item Name="Acquire Semaphore.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/semaphor.llb/Acquire Semaphore.vi"/>
				<Item Name="compatReadText.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatReadText.vi"/>
			</Item>
			<Item Name="user.lib" Type="Folder">
				<Item Name="Build Path - Traditional__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Build Path - Traditional__ogtk.vi"/>
				<Item Name="Build Path - File Names and Paths Arrays - path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Build Path - File Names and Paths Arrays - path__ogtk.vi"/>
				<Item Name="Build Path - File Names Array - path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Build Path - File Names Array - path__ogtk.vi"/>
				<Item Name="Build Path - Traditional - path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Build Path - Traditional - path__ogtk.vi"/>
				<Item Name="Build Path - File Names and Paths Arrays__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Build Path - File Names and Paths Arrays__ogtk.vi"/>
				<Item Name="Build Path - File Names Array__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Build Path - File Names Array__ogtk.vi"/>
				<Item Name="Build Path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Build Path__ogtk.vi"/>
				<Item Name="Strip Path - Traditional__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Strip Path - Traditional__ogtk.vi"/>
				<Item Name="Strip Path - Arrays__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Strip Path - Arrays__ogtk.vi"/>
				<Item Name="Strip Path__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Strip Path__ogtk.vi"/>
				<Item Name="Create Dir if Non-Existant__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Create Dir if Non-Existant__ogtk.vi"/>
				<Item Name="Build Error Cluster__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/error/error.llb/Build Error Cluster__ogtk.vi"/>
				<Item Name="Valid Path - Traditional__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Valid Path - Traditional__ogtk.vi"/>
				<Item Name="Delete Recursive__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Delete Recursive__ogtk.vi"/>
				<Item Name="Compare Two Paths - Scalar__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Compare Two Paths - Scalar__ogtk.vi"/>
				<Item Name="Compare Two Paths - Path2 Array__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Compare Two Paths - Path2 Array__ogtk.vi"/>
				<Item Name="Compare Two Paths - Path1 Array__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Compare Two Paths - Path1 Array__ogtk.vi"/>
				<Item Name="Compare Two Paths - Array__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Compare Two Paths - Array__ogtk.vi"/>
				<Item Name="Compare Two Paths__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Compare Two Paths__ogtk.vi"/>
				<Item Name="Merge Directories__ogtk.vi" Type="VI" URL="/&lt;userlib&gt;/_OpenG.lib/file/file.llb/Merge Directories__ogtk.vi"/>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Vista and Later" Type="Installer">
				<Property Name="Destination[0].name" Type="Str">Users</Property>
				<Property Name="Destination[0].parent" Type="Str">{C63B6F86-C439-4240-9AAE-EC6A9DDD0A29}</Property>
				<Property Name="Destination[0].tag" Type="Str">{66DA7A26-BD22-4E61-88E2-2F904A9CB0C7}</Property>
				<Property Name="Destination[0].type" Type="Str">userFolder</Property>
				<Property Name="Destination[1].name" Type="Str">Public</Property>
				<Property Name="Destination[1].parent" Type="Str">{66DA7A26-BD22-4E61-88E2-2F904A9CB0C7}</Property>
				<Property Name="Destination[1].tag" Type="Str">{F537D938-FEA6-4847-AFB7-9E29A4D85C17}</Property>
				<Property Name="Destination[1].type" Type="Str">userFolder</Property>
				<Property Name="Destination[2].name" Type="Str">Documents</Property>
				<Property Name="Destination[2].parent" Type="Str">{F537D938-FEA6-4847-AFB7-9E29A4D85C17}</Property>
				<Property Name="Destination[2].tag" Type="Str">{60191736-FEAE-4057-A72C-5D3BD8253E03}</Property>
				<Property Name="Destination[2].type" Type="Str">userFolder</Property>
				<Property Name="Destination[3].name" Type="Str">National Instruments</Property>
				<Property Name="Destination[3].parent" Type="Str">{60191736-FEAE-4057-A72C-5D3BD8253E03}</Property>
				<Property Name="Destination[3].tag" Type="Str">{4DBDA4ED-3480-4CD9-912E-57B6791E56A8}</Property>
				<Property Name="Destination[3].type" Type="Str">userFolder</Property>
				<Property Name="Destination[4].name" Type="Str">NI VeriStand 2013</Property>
				<Property Name="Destination[4].parent" Type="Str">{4DBDA4ED-3480-4CD9-912E-57B6791E56A8}</Property>
				<Property Name="Destination[4].tag" Type="Str">{C0556192-6B47-40E5-8EBC-67F518CE03A0}</Property>
				<Property Name="Destination[4].type" Type="Str">userFolder</Property>
				<Property Name="Destination[5].name" Type="Str">National Instruments</Property>
				<Property Name="Destination[5].parent" Type="Str">{3912416A-D2E5-411B-AFEE-B63654D690C0}</Property>
				<Property Name="Destination[5].tag" Type="Str">{715FC321-0035-440A-8F27-18303AB061D5}</Property>
				<Property Name="Destination[5].type" Type="Str">userFolder</Property>
				<Property Name="Destination[6].name" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Destination[6].parent" Type="Str">{715FC321-0035-440A-8F27-18303AB061D5}</Property>
				<Property Name="Destination[6].tag" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Destination[6].type" Type="Str">userFolder</Property>
				<Property Name="Destination[7].name" Type="Str">National Instruments</Property>
				<Property Name="Destination[7].parent" Type="Str">{115F5F59-DED6-42E2-8467-4CD042208C47}</Property>
				<Property Name="Destination[7].tag" Type="Str">{BF726566-5596-47B9-9165-338C491EEFFC}</Property>
				<Property Name="Destination[7].type" Type="Str">userFolder</Property>
				<Property Name="Destination[8].name" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Destination[8].parent" Type="Str">{BF726566-5596-47B9-9165-338C491EEFFC}</Property>
				<Property Name="Destination[8].tag" Type="Str">{75BF8323-FA83-45DC-BD09-72BDC37D4367}</Property>
				<Property Name="Destination[8].type" Type="Str">userFolder</Property>
				<Property Name="DestinationCount" Type="Int">9</Property>
				<Property Name="INST_autoIncrement" Type="Bool">true</Property>
				<Property Name="INST_buildLocation" Type="Path">/C/TempBuilds/TestCellController</Property>
				<Property Name="INST_buildSpecName" Type="Str">Vista and Later</Property>
				<Property Name="INST_defaultDir" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="INST_includeError" Type="Bool">false</Property>
				<Property Name="INST_productName" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="INST_productVersion" Type="Str">1.0.0</Property>
				<Property Name="InstSpecBitness" Type="Str">32-bit</Property>
				<Property Name="InstSpecVersion" Type="Str">13008051</Property>
				<Property Name="MSI_arpCompany" Type="Str">National Instruments</Property>
				<Property Name="MSI_arpURL" Type="Str">http://www.ni.com/veristand</Property>
				<Property Name="MSI_distID" Type="Str">{C00212E5-FD6A-4E94-90A8-FCC1BA94B86B}</Property>
				<Property Name="MSI_osCheck" Type="Int">2</Property>
				<Property Name="MSI_upgradeCode" Type="Str">{876A0980-7124-4B49-8CB1-176FD5D72013}</Property>
				<Property Name="MSI_windowTitle" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="RegDest[0].dirName" Type="Str">Software</Property>
				<Property Name="RegDest[0].dirTag" Type="Str">{DDFAFC8B-E728-4AC8-96DE-B920EBB97A86}</Property>
				<Property Name="RegDest[0].parentTag" Type="Str">2</Property>
				<Property Name="RegDestCount" Type="Int">1</Property>
				<Property Name="Source[0].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[0].name" Type="Str">XML Writer.exe</Property>
				<Property Name="Source[0].runEXE" Type="Bool">true</Property>
				<Property Name="Source[0].tag" Type="Ref">/My Computer/XML Writer.exe</Property>
				<Property Name="Source[0].type" Type="Str">File</Property>
				<Property Name="Source[1].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[1].File[0].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[1].File[0].name" Type="Str">Getting Started with the NI Test Cell Control System.pdf</Property>
				<Property Name="Source[1].File[0].Shortcut[0].destIndex" Type="Int">1</Property>
				<Property Name="Source[1].File[0].Shortcut[0].name" Type="Str">Getting Started with the NI Test Cell Control System</Property>
				<Property Name="Source[1].File[0].Shortcut[0].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[1].File[0].Shortcut[1].destIndex" Type="Int">2</Property>
				<Property Name="Source[1].File[0].Shortcut[1].name" Type="Str">Getting Started with the NI Test Cell Control System</Property>
				<Property Name="Source[1].File[0].Shortcut[1].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[1].File[0].ShortcutCount" Type="Int">2</Property>
				<Property Name="Source[1].File[0].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Help/Getting Started with the NI Test Cell Control System.pdf</Property>
				<Property Name="Source[1].FileCount" Type="Int">1</Property>
				<Property Name="Source[1].name" Type="Str">Help</Property>
				<Property Name="Source[1].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Help</Property>
				<Property Name="Source[1].type" Type="Str">Folder</Property>
				<Property Name="Source[10].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[10].name" Type="Str">Setup Test Cell Controller.exe</Property>
				<Property Name="Source[10].Shortcut[0].destIndex" Type="Int">1</Property>
				<Property Name="Source[10].Shortcut[0].name" Type="Str">Setup Test Cell Controller</Property>
				<Property Name="Source[10].Shortcut[0].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[10].Shortcut[1].destIndex" Type="Int">2</Property>
				<Property Name="Source[10].Shortcut[1].name" Type="Str">Setup Test Cell Controller</Property>
				<Property Name="Source[10].Shortcut[1].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[10].ShortcutCount" Type="Int">2</Property>
				<Property Name="Source[10].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Setup Test Cell Controller.exe</Property>
				<Property Name="Source[10].type" Type="Str">File</Property>
				<Property Name="Source[11].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[11].name" Type="Str">Setup Test Cell Controller.ini</Property>
				<Property Name="Source[11].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Setup Test Cell Controller.ini</Property>
				<Property Name="Source[11].type" Type="Str">File</Property>
				<Property Name="Source[2].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[2].File[0].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[2].File[0].name" Type="Str">Scan Engine.zip</Property>
				<Property Name="Source[2].File[0].Shortcut[0].destIndex" Type="Int">1</Property>
				<Property Name="Source[2].File[0].Shortcut[0].name" Type="Str">NI VeriStand 2012 Hands On</Property>
				<Property Name="Source[2].File[0].Shortcut[0].subDir" Type="Str"></Property>
				<Property Name="Source[2].File[0].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Unzip/Scan Engine.zip</Property>
				<Property Name="Source[2].FileCount" Type="Int">1</Property>
				<Property Name="Source[2].name" Type="Str">Unzip</Property>
				<Property Name="Source[2].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Unzip</Property>
				<Property Name="Source[2].type" Type="Str">Folder</Property>
				<Property Name="Source[3].dest" Type="Str">{C0556192-6B47-40E5-8EBC-67F518CE03A0}</Property>
				<Property Name="Source[3].File[0].dest" Type="Str">{C0556192-6B47-40E5-8EBC-67F518CE03A0}</Property>
				<Property Name="Source[3].File[0].name" Type="Str">IO Test.nivscf</Property>
				<Property Name="Source[3].File[0].tag" Type="Ref">/My Computer/NI VeriStand (Documents)/Examples/Test Cell Controller/IO Test/IO Test.nivscf</Property>
				<Property Name="Source[3].FileCount" Type="Int">1</Property>
				<Property Name="Source[3].name" Type="Str">Examples</Property>
				<Property Name="Source[3].tag" Type="Ref">/My Computer/NI VeriStand (Documents)/Examples</Property>
				<Property Name="Source[3].type" Type="Str">Folder</Property>
				<Property Name="Source[4].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[4].File[0].dest" Type="Str">{C0556192-6B47-40E5-8EBC-67F518CE03A0}</Property>
				<Property Name="Source[4].File[0].name" Type="Str">IO Test.nivscf</Property>
				<Property Name="Source[4].File[0].tag" Type="Ref">/My Computer/NI VeriStand (Documents)/Examples/Test Cell Controller/IO Test/IO Test.nivscf</Property>
				<Property Name="Source[4].FileCount" Type="Int">1</Property>
				<Property Name="Source[4].name" Type="Str">New Test Cell Controller Project.ini</Property>
				<Property Name="Source[4].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/New Test Cell Controller Project.ini</Property>
				<Property Name="Source[4].type" Type="Str">File</Property>
				<Property Name="Source[5].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[5].File[0].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[5].File[0].name" Type="Str">Scan Engine.zip</Property>
				<Property Name="Source[5].File[0].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Unzip/Scan Engine.zip</Property>
				<Property Name="Source[5].FileCount" Type="Int">1</Property>
				<Property Name="Source[5].name" Type="Str">New Test Cell Controller Project.exe</Property>
				<Property Name="Source[5].Shortcut[0].destIndex" Type="Int">1</Property>
				<Property Name="Source[5].Shortcut[0].name" Type="Str">New Test Cell Controller Project</Property>
				<Property Name="Source[5].Shortcut[0].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[5].Shortcut[1].destIndex" Type="Int">2</Property>
				<Property Name="Source[5].Shortcut[1].name" Type="Str">New Test Cell Controller Project</Property>
				<Property Name="Source[5].Shortcut[1].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[5].ShortcutCount" Type="Int">2</Property>
				<Property Name="Source[5].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/New Test Cell Controller Project.exe</Property>
				<Property Name="Source[5].type" Type="Str">File</Property>
				<Property Name="Source[6].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[6].name" Type="Str">New Test Cell Controller Project.aliases</Property>
				<Property Name="Source[6].Shortcut[0].destIndex" Type="Int">1</Property>
				<Property Name="Source[6].Shortcut[0].name" Type="Str">New Test Cell Controller Project</Property>
				<Property Name="Source[6].Shortcut[0].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[6].Shortcut[1].destIndex" Type="Int">2</Property>
				<Property Name="Source[6].Shortcut[1].name" Type="Str">New Test Cell Controller Project</Property>
				<Property Name="Source[6].Shortcut[1].subDir" Type="Str">NI Test Cell Controller 2013</Property>
				<Property Name="Source[6].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/New Test Cell Controller Project.aliases</Property>
				<Property Name="Source[6].type" Type="Str">File</Property>
				<Property Name="Source[7].dest" Type="Str">{75BF8323-FA83-45DC-BD09-72BDC37D4367}</Property>
				<Property Name="Source[7].File[0].dest" Type="Str">{75BF8323-FA83-45DC-BD09-72BDC37D4367}</Property>
				<Property Name="Source[7].File[0].name" Type="Str">Template Project.nivscf</Property>
				<Property Name="Source[7].File[0].tag" Type="Ref">/My Computer/Test Cell Controller (ProgramData)/Template Project/Template Project.nivscf</Property>
				<Property Name="Source[7].FileCount" Type="Int">1</Property>
				<Property Name="Source[7].name" Type="Str">Template Project</Property>
				<Property Name="Source[7].tag" Type="Ref">/My Computer/Test Cell Controller (ProgramData)/Template Project</Property>
				<Property Name="Source[7].type" Type="Str">Folder</Property>
				<Property Name="Source[8].dest" Type="Str">{75BF8323-FA83-45DC-BD09-72BDC37D4367}</Property>
				<Property Name="Source[8].File[0].dest" Type="Str">{75BF8323-FA83-45DC-BD09-72BDC37D4367}</Property>
				<Property Name="Source[8].File[0].name" Type="Str">Template Project - XNET.nivscf</Property>
				<Property Name="Source[8].File[0].tag" Type="Ref">/My Computer/Test Cell Controller (ProgramData)/Template Project - XNET/Template Project - XNET.nivscf</Property>
				<Property Name="Source[8].FileCount" Type="Int">1</Property>
				<Property Name="Source[8].name" Type="Str">Template Project - XNET</Property>
				<Property Name="Source[8].tag" Type="Ref">/My Computer/Test Cell Controller (ProgramData)/Template Project - XNET</Property>
				<Property Name="Source[8].type" Type="Str">Folder</Property>
				<Property Name="Source[9].dest" Type="Str">{A0292411-2FD8-4942-9623-C04BA48E51A0}</Property>
				<Property Name="Source[9].File[0].dest" Type="Str">{75BF8323-FA83-45DC-BD09-72BDC37D4367}</Property>
				<Property Name="Source[9].File[0].name" Type="Str">Template Project - XNET.nivscf</Property>
				<Property Name="Source[9].File[0].tag" Type="Ref">/My Computer/Test Cell Controller (ProgramData)/Template Project - XNET/Template Project - XNET.nivscf</Property>
				<Property Name="Source[9].FileCount" Type="Int">1</Property>
				<Property Name="Source[9].name" Type="Str">Setup Test Cell Controller.aliases</Property>
				<Property Name="Source[9].tag" Type="Ref">/My Computer/Test Cell Controller (Program Files)/Setup Test Cell Controller.aliases</Property>
				<Property Name="Source[9].type" Type="Str">File</Property>
				<Property Name="SourceCount" Type="Int">12</Property>
			</Item>
		</Item>
	</Item>
</Project>
