<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="13008000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="IOScan.Faults" Type="Str"></Property>
		<Property Name="IOScan.NetVarPeriod" Type="UInt">100</Property>
		<Property Name="IOScan.NetWatchdogEnabled" Type="Bool">false</Property>
		<Property Name="IOScan.Period" Type="UInt">10000</Property>
		<Property Name="IOScan.PowerupMode" Type="UInt">0</Property>
		<Property Name="IOScan.Priority" Type="UInt">9</Property>
		<Property Name="IOScan.ReportModeConflict" Type="Bool">true</Property>
		<Property Name="IOScan.StartEngineOnDeploy" Type="Bool">false</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Controls" Type="Folder">
			<Item Name="Button Refs.ctl" Type="VI" URL="../Controls/Button Refs.ctl"/>
			<Item Name="Control Refs.ctl" Type="VI" URL="../Controls/Control Refs.ctl"/>
			<Item Name="Detected.ctl" Type="VI" URL="../Controls/Detected.ctl"/>
			<Item Name="Indicator Refs.ctl" Type="VI" URL="../Controls/Indicator Refs.ctl"/>
			<Item Name="Network Info.ctl" Type="VI" URL="../Controls/Network Info.ctl"/>
			<Item Name="Network Settings.ctl" Type="VI" URL="../Controls/Network Settings.ctl"/>
			<Item Name="Refs.ctl" Type="VI" URL="../Controls/Refs.ctl"/>
			<Item Name="Slider Refs.ctl" Type="VI" URL="../Controls/Slider Refs.ctl"/>
			<Item Name="Tab Ctl Refs.ctl" Type="VI" URL="../Controls/Tab Ctl Refs.ctl"/>
			<Item Name="Targets.ctl" Type="VI" URL="../Controls/Targets.ctl"/>
		</Item>
		<Item Name="globals" Type="Folder" URL="../globals">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="images" Type="Folder" URL="../images">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="manifests" Type="Folder" URL="../manifests">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="sub" Type="Folder">
			<Item Name="Change Network Settings.vi" Type="VI" URL="../sub/Change Network Settings.vi"/>
			<Item Name="Connect Verify.vi" Type="VI" URL="../sub/Connect Verify.vi"/>
			<Item Name="Deploy.vi" Type="VI" URL="../sub/Deploy.vi"/>
			<Item Name="Detect Failed.vi" Type="VI" URL="../sub/Detect Failed.vi"/>
			<Item Name="Detect.vi" Type="VI" URL="../sub/Detect.vi"/>
			<Item Name="Multi Detected.vi" Type="VI" URL="../sub/Multi Detected.vi"/>
			<Item Name="One Detected.vi" Type="VI" URL="../sub/One Detected.vi"/>
			<Item Name="Reformat Target.vi" Type="VI" URL="../sub/Reformat Target.vi"/>
			<Item Name="RenameDNS.vi" Type="VI" URL="../sub/RenameDNS.vi"/>
			<Item Name="Run Deployment.vi" Type="VI" URL="../sub/Run Deployment.vi"/>
			<Item Name="Run Detection.vi" Type="VI" URL="../sub/Run Detection.vi"/>
			<Item Name="Success.vi" Type="VI" URL="../sub/Success.vi"/>
			<Item Name="Troubleshoot 1.vi" Type="VI" URL="../sub/Troubleshoot 1.vi"/>
			<Item Name="Troubleshoot 2.vi" Type="VI" URL="../sub/Troubleshoot 2.vi"/>
			<Item Name="Update Buttons.vi" Type="VI" URL="../sub/Update Buttons.vi"/>
			<Item Name="Update Progress.vi" Type="VI" URL="../sub/Update Progress.vi"/>
			<Item Name="Video Wait.vi" Type="VI" URL="../sub/Video Wait.vi"/>
		</Item>
		<Item Name="subVIs" Type="Folder" URL="../subVIs">
			<Property Name="NI.DISK" Type="Bool">true</Property>
			<Property Name="NI.SortType" Type="Int">0</Property>
		</Item>
		<Item Name="types" Type="Folder" URL="../types">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="TestCellUtil.vi" Type="VI" URL="../TestCellUtil.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="8.6CompatibleGlobalVar.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/config.llb/8.6CompatibleGlobalVar.vi"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Escape Characters for HTTP.vi" Type="VI" URL="/&lt;vilib&gt;/printing/PathToURL.llb/Escape Characters for HTTP.vi"/>
				<Item Name="Get System Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/sysdir.llb/Get System Directory.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_LVConfig.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/config.llb/NI_LVConfig.lvlib"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="nisyscfg.lvlib" Type="Library" URL="/&lt;vilib&gt;/nisyscfg/nisyscfg.lvlib"/>
				<Item Name="Open URL in Default Browser (path).vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser (path).vi"/>
				<Item Name="Open URL in Default Browser (string).vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser (string).vi"/>
				<Item Name="Open URL in Default Browser core.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser core.vi"/>
				<Item Name="Open URL in Default Browser.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser.vi"/>
				<Item Name="Path to URL.vi" Type="VI" URL="/&lt;vilib&gt;/printing/PathToURL.llb/Path to URL.vi"/>
				<Item Name="Set Busy.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Busy.vi"/>
				<Item Name="Set Cursor (Cursor ID).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor (Cursor ID).vi"/>
				<Item Name="Set Cursor (Icon Pict).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor (Icon Pict).vi"/>
				<Item Name="Set Cursor.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Set Cursor.vi"/>
				<Item Name="System Directory Type.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/sysdir.llb/System Directory Type.ctl"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="Unset Busy.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/cursorutil.llb/Unset Busy.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
			</Item>
			<Item Name="nisyscfg.dll" Type="Document" URL="nisyscfg.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Setup Utility" Type="EXE">
				<Property Name="App_INI_aliasGUID" Type="Str">{7421EA0C-5BD0-4808-B7C1-CB400C29070C}</Property>
				<Property Name="App_INI_GUID" Type="Str">{102B5F6F-204E-4F29-895B-4F814C9C109B}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{C00BC1B8-D6AE-4835-B981-570D8749F779}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Setup Utility</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../Installer/Test Cell Controller (Program Files)</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{F42E5E1A-6831-4D54-AD2E-0E8B3A1B3F65}</Property>
				<Property Name="Bld_version.build" Type="Int">1</Property>
				<Property Name="Bld_version.major" Type="Int">13</Property>
				<Property Name="Destination[0].destName" Type="Str">Setup Test Cell Controller.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../Installer/Test Cell Controller (Program Files)/Setup Test Cell Controller.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../Installer/Test Cell Controller (Program Files)/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/My Computer/images/autorun.ico</Property>
				<Property Name="Source[0].itemID" Type="Str">{9E99CA1B-944D-4570-8FFA-CCBBE6E270F4}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/TestCellUtil.vi</Property>
				<Property Name="Source[1].properties[0].type" Type="Str">Show vertical scroll bar</Property>
				<Property Name="Source[1].properties[0].value" Type="Bool">false</Property>
				<Property Name="Source[1].properties[1].type" Type="Str">Show horizontal scroll bar</Property>
				<Property Name="Source[1].properties[1].value" Type="Bool">false</Property>
				<Property Name="Source[1].properties[2].type" Type="Str">Show toolbar</Property>
				<Property Name="Source[1].properties[2].value" Type="Bool">false</Property>
				<Property Name="Source[1].properties[3].type" Type="Str">Show Abort button</Property>
				<Property Name="Source[1].properties[3].value" Type="Bool">false</Property>
				<Property Name="Source[1].properties[4].type" Type="Str">Allow user to close window</Property>
				<Property Name="Source[1].properties[4].value" Type="Bool">false</Property>
				<Property Name="Source[1].properties[5].type" Type="Str">Window run-time position</Property>
				<Property Name="Source[1].properties[5].value" Type="Str">Centered</Property>
				<Property Name="Source[1].properties[6].type" Type="Str">Show menu bar</Property>
				<Property Name="Source[1].properties[6].value" Type="Bool">false</Property>
				<Property Name="Source[1].propertiesCount" Type="Int">7</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">National Instruments</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2013 NI</Property>
				<Property Name="TgtF_productName" Type="Str">Test Cell Controller</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{F20CC5E0-7964-42E8-A883-3F97BCD22288}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">Setup Test Cell Controller.exe</Property>
			</Item>
		</Item>
	</Item>
</Project>
