<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="19008000">
	<Property Name="CCSymbols" Type="Str">STRICT,ERROR_HANDLING;RELAXED,ERROR_HANDLING;</Property>
	<Property Name="NI.LV.All.SaveVersion" Type="Str">19.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Property Name="utf.calculate.project.code.coverage" Type="Bool">true</Property>
	<Property Name="utf.create.arraybrackets" Type="Str">[]</Property>
	<Property Name="utf.create.arraythreshold" Type="UInt">100</Property>
	<Property Name="utf.create.captureinputvalues" Type="Bool">true</Property>
	<Property Name="utf.create.captureoutputvalues" Type="Bool">true</Property>
	<Property Name="utf.create.codecoverage.flag" Type="Bool">false</Property>
	<Property Name="utf.create.codecoverage.value" Type="UInt">100</Property>
	<Property Name="utf.create.editor.flag" Type="Bool">false</Property>
	<Property Name="utf.create.editor.path" Type="Path"></Property>
	<Property Name="utf.create.nameseparator" Type="Str">/</Property>
	<Property Name="utf.create.precision" Type="UInt">6</Property>
	<Property Name="utf.create.repetitions" Type="UInt">1</Property>
	<Property Name="utf.create.testpath.flag" Type="Bool">false</Property>
	<Property Name="utf.create.testpath.path" Type="Path"></Property>
	<Property Name="utf.create.timeout.flag" Type="Bool">false</Property>
	<Property Name="utf.create.timeout.value" Type="UInt">0</Property>
	<Property Name="utf.create.type" Type="UInt">0</Property>
	<Property Name="utf.enable.RT.VI.server" Type="Bool">false</Property>
	<Property Name="utf.passwords" Type="Bin">*1#!!!!!!!)!%%!Q`````Q:4&gt;(*J&lt;G=!!":!1!!"`````Q!!#6"B=X.X&lt;X*E=Q!"!!%!!!!"!!!!#F652E&amp;-4&amp;.516)!!!!!</Property>
	<Property Name="utf.report.atml.create" Type="Bool">false</Property>
	<Property Name="utf.report.atml.path" Type="Path">ATML report.xml</Property>
	<Property Name="utf.report.atml.view" Type="Bool">false</Property>
	<Property Name="utf.report.details.errors" Type="Bool">false</Property>
	<Property Name="utf.report.details.failed" Type="Bool">false</Property>
	<Property Name="utf.report.details.passed" Type="Bool">false</Property>
	<Property Name="utf.report.errors" Type="Bool">true</Property>
	<Property Name="utf.report.failed" Type="Bool">true</Property>
	<Property Name="utf.report.html.create" Type="Bool">false</Property>
	<Property Name="utf.report.html.path" Type="Path">HTML report.html</Property>
	<Property Name="utf.report.html.view" Type="Bool">false</Property>
	<Property Name="utf.report.passed" Type="Bool">true</Property>
	<Property Name="utf.report.skipped" Type="Bool">true</Property>
	<Property Name="utf.report.sortby" Type="UInt">1</Property>
	<Property Name="utf.report.stylesheet.flag" Type="Bool">false</Property>
	<Property Name="utf.report.stylesheet.path" Type="Path"></Property>
	<Property Name="utf.report.summary" Type="Bool">true</Property>
	<Property Name="utf.report.txt.create" Type="Bool">false</Property>
	<Property Name="utf.report.txt.path" Type="Path">ASCII report.txt</Property>
	<Property Name="utf.report.txt.view" Type="Bool">false</Property>
	<Property Name="utf.run.changed.days" Type="UInt">1</Property>
	<Property Name="utf.run.changed.outdated" Type="Bool">false</Property>
	<Property Name="utf.run.changed.timestamp" Type="Bin">*1#!!!!!!!%!%%"5!!9*2'&amp;U:3^U;7VF!!%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!</Property>
	<Property Name="utf.run.days.flag" Type="Bool">false</Property>
	<Property Name="utf.run.includevicallers" Type="Bool">false</Property>
	<Property Name="utf.run.logfile.flag" Type="Bool">false</Property>
	<Property Name="utf.run.logfile.overwrite" Type="Bool">false</Property>
	<Property Name="utf.run.logfile.path" Type="Path">test execution log.txt</Property>
	<Property Name="utf.run.modified.last.run.flag" Type="Bool">true</Property>
	<Property Name="utf.run.priority.flag" Type="Bool">false</Property>
	<Property Name="utf.run.priority.value" Type="UInt">5</Property>
	<Property Name="utf.run.statusfile.flag" Type="Bool">false</Property>
	<Property Name="utf.run.statusfile.path" Type="Path">test status log.txt</Property>
	<Property Name="utf.run.timestamp.flag" Type="Bool">false</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="devtools" Type="Folder">
			<Item Name="Add Licence Information.vi" Type="VI" URL="../devtools/Add Licence Information.vi"/>
			<Item Name="documentation-howto.txt" Type="Document" URL="../devtools/documentation-howto.txt"/>
			<Item Name="VI-Analyzer-Config.viancfg" Type="Document" URL="../devtools/VI-Analyzer-Config.viancfg"/>
			<Item Name="VI-Analyzer-Custom-Dict.txt" Type="Document" URL="../devtools/VI-Analyzer-Custom-Dict.txt"/>
		</Item>
		<Item Name="examples" Type="Folder">
			<Item Name="exampledata" Type="Folder">
				<Item Name="mosquitto.org.crt" Type="Document" URL="../examples/exampledata/mosquitto.org.crt"/>
			</Item>
			<Item Name="subvis" Type="Folder">
				<Item Name="Exec Every X ms.vi" Type="VI" URL="../examples/subvis/Exec Every X ms.vi"/>
				<Item Name="HMI State Machine.vi" Type="VI" URL="../examples/subvis/HMI State Machine.vi"/>
				<Item Name="HMI-States.ctl" Type="VI" URL="../examples/subvis/HMI-States.ctl"/>
				<Item Name="Insert Into TreeView.vi" Type="VI" URL="../examples/subvis/Insert Into TreeView.vi"/>
			</Item>
			<Item Name="Example - Hello Properties.vi" Type="VI" URL="../examples/Example - Hello Properties.vi"/>
			<Item Name="Example - Hello World.vi" Type="VI" URL="../examples/Example - Hello World.vi"/>
			<Item Name="Example - Interactive MQTT Client.vi" Type="VI" URL="../examples/Example - Interactive MQTT Client.vi"/>
			<Item Name="Example - MQTT performance test.vi" Type="VI" URL="../examples/Example - MQTT performance test.vi"/>
			<Item Name="Example - Publish to localhost.vi" Type="VI" URL="../examples/Example - Publish to localhost.vi"/>
			<Item Name="Example - Simple MQTT client.vi" Type="VI" URL="../examples/Example - Simple MQTT client.vi"/>
		</Item>
		<Item Name="src" Type="Folder">
			<Item Name="KoRE-MQTT.lvlib" Type="Library" URL="../src/KoRE-MQTT.lvlib"/>
		</Item>
		<Item Name="logo.ico" Type="Document" URL="../examples/exampledata/logo.ico"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Example - Interactive MQTT Client" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{C9D379CE-F75F-11EF-8669-88AEDD0F38F5}</Property>
				<Property Name="App_INI_GUID" Type="Str">{C9D378F0-F75F-11EF-8669-88AEDD0F38F5}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{C9D380A8-F75F-11EF-8669-88AEDD0F38F5}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Example - Interactive MQTT Client</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeTypedefs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">/C/builds/Example - Interactive MQTT Client</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{C9D380DF-F75F-11EF-8669-88AEDD0F38F5}</Property>
				<Property Name="Bld_supportedLanguage[0]" Type="Str">English</Property>
				<Property Name="Bld_supportedLanguageCount" Type="Int">1</Property>
				<Property Name="Bld_version.build" Type="Int">24</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">CoRE-MQTT-Example-Interactive.exe</Property>
				<Property Name="Destination[0].path" Type="Path">/C/builds/Example - Interactive MQTT Client/CoRE-MQTT-Example-Interactive.exe</Property>
				<Property Name="Destination[0].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">/C/builds/Example - Interactive MQTT Client/exampledata</Property>
				<Property Name="Destination[1].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/My Computer/logo.ico</Property>
				<Property Name="Source[0].itemID" Type="Str">{E1CBB0C1-352B-40BB-894E-6D9A03DC5962}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/examples/Example - Interactive MQTT Client.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[2].itemID" Type="Ref">/My Computer/examples/exampledata/mosquitto.org.crt</Property>
				<Property Name="Source[2].sourceInclusion" Type="Str">Include</Property>
				<Property Name="SourceCount" Type="Int">3</Property>
				<Property Name="TgtF_fastFileFormat" Type="Bool">true</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Example - Interactive MQTT Client</Property>
				<Property Name="TgtF_internalName" Type="Str">Example - Interactive MQTT Client</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright 2025 </Property>
				<Property Name="TgtF_productName" Type="Str">Example - Interactive MQTT Client</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{C9D37F57-F75F-11EF-8669-88AEDD0F38F5}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">CoRE-MQTT-Example-Interactive.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
			<Item Name="Example - MQTT performance test" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{F40F73BD-BB36-4196-9F25-12DC3A9B23E6}</Property>
				<Property Name="App_INI_GUID" Type="Str">{7CDCC608-819E-4C6A-9686-034B042BD2E9}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{E3E69A73-976E-40A0-A228-7DFE6636577B}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Example - MQTT performance test</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeTypedefs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">/C/builds/Example - MQTT performance test</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{ABF49296-89F9-45A6-B1AD-80E5F663BE30}</Property>
				<Property Name="Bld_supportedLanguage[0]" Type="Str">English</Property>
				<Property Name="Bld_supportedLanguageCount" Type="Int">1</Property>
				<Property Name="Bld_version.build" Type="Int">16</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">CoRE-MQTT-Perf-Test.exe</Property>
				<Property Name="Destination[0].path" Type="Path">/C/builds/Example - MQTT performance test/CoRE-MQTT-Perf-Test.exe</Property>
				<Property Name="Destination[0].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">/C/builds/Example - MQTT performance test/data</Property>
				<Property Name="Destination[1].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/</Property>
				<Property Name="Source[0].itemID" Type="Str">{97BB0BF3-923A-41DF-87F0-F805D5F9C721}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_fastFileFormat" Type="Bool">true</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Example - Interactive MQTT Browser</Property>
				<Property Name="TgtF_internalName" Type="Str">Example - Interactive MQTT Browser</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright 2025 </Property>
				<Property Name="TgtF_productName" Type="Str">Example - Interactive MQTT Browser</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{102F61BF-6E98-47F3-AE53-012D0CAA0479}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">CoRE-MQTT-Perf-Test.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
			<Item Name="Example - Publish to localhost" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{64E52E68-B0F5-4FB9-84F7-5DFBDDC3CC74}</Property>
				<Property Name="App_INI_GUID" Type="Str">{47EF7D0F-E5BA-4F50-AE48-0691B2BF59FC}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="App_winsec.description" Type="Str">http://www.Consultant.com</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{E915C600-E0C0-424C-8E48-01BF12AB05A8}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Example - Publish to localhost</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">/C/builds/Example - Publish to localhost</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{426A1966-4558-49F1-ACF8-4FD4B51D3A3B}</Property>
				<Property Name="Bld_version.build" Type="Int">2</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">Example - Publish to localhost.exe</Property>
				<Property Name="Destination[0].path" Type="Path">/C/builds/Example - Publish to localhost/Example - Publish to localhost.exe</Property>
				<Property Name="Destination[0].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">/C/builds/Example - Publish to localhost/data</Property>
				<Property Name="Destination[1].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{200E56FF-0DBB-42F9-836B-65DD8077DAFC}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">Consultant</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Example - Publish to localhost</Property>
				<Property Name="TgtF_internalName" Type="Str">Example - Publish to localhost</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2025 Consultant</Property>
				<Property Name="TgtF_productName" Type="Str">Example - Publish to localhost</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{4351591A-CFE2-4990-B9E7-9501E6B2C4FA}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">Example - Publish to localhost.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
			<Item Name="Example - Simple MQTT client" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{55F3D2D1-0A59-45E7-9B61-81FCB280E878}</Property>
				<Property Name="App_INI_GUID" Type="Str">{65FA25D1-76FC-4F8E-B028-FD16E92BFACE}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{B598696F-0C0B-460A-A280-242D525544AD}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Example - Simple MQTT client</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeTypedefs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">/C/builds/Example - Simple MQTT client</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{7B9D2AB8-CFCA-4BB5-8B10-9D8923BA5FFF}</Property>
				<Property Name="Bld_supportedLanguage[0]" Type="Str">English</Property>
				<Property Name="Bld_supportedLanguageCount" Type="Int">1</Property>
				<Property Name="Bld_version.build" Type="Int">15</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">CoRE-MQTT-Example-Simple.exe</Property>
				<Property Name="Destination[0].path" Type="Path">/C/builds/Example - Simple MQTT client/CoRE-MQTT-Example-Simple.exe</Property>
				<Property Name="Destination[0].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">/C/builds/Example - Simple MQTT client/data</Property>
				<Property Name="Destination[1].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/</Property>
				<Property Name="Source[0].itemID" Type="Str">{F1538728-4452-4FB9-B907-C5737042F102}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_fastFileFormat" Type="Bool">true</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Example - Interactive MQTT Browser</Property>
				<Property Name="TgtF_internalName" Type="Str">Example - Interactive MQTT Browser</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright 2025 </Property>
				<Property Name="TgtF_productName" Type="Str">Example - Interactive MQTT Browser</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{059323E0-F032-4926-AF7F-EA1BDC2BB19B}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">CoRE-MQTT-Example-Simple.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
			<Item Name="My Source Distribution" Type="Source Distribution">
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{FD07C6DB-3431-4DBA-A2CE-D2E854B45726}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">My Source Distribution</Property>
				<Property Name="Bld_excludedDirectory[0]" Type="Path">vi.lib</Property>
				<Property Name="Bld_excludedDirectory[0].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[1]" Type="Path">resource/objmgr</Property>
				<Property Name="Bld_excludedDirectory[1].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[2]" Type="Path">/C/ProgramData/National Instruments/InstCache/25.0</Property>
				<Property Name="Bld_excludedDirectory[3]" Type="Path">/C/Users/kare_2/Documents/LabVIEW Data/2025(32-bit)/ExtraVILib</Property>
				<Property Name="Bld_excludedDirectory[4]" Type="Path">instr.lib</Property>
				<Property Name="Bld_excludedDirectory[4].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[5]" Type="Path">user.lib</Property>
				<Property Name="Bld_excludedDirectory[5].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectoryCount" Type="Int">6</Property>
				<Property Name="Bld_localDestDir" Type="Path">/C/builds/LV-KoRE-MQTT/NI_AB_PROJECTNAME/src/Public</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{56D98C06-D808-46A4-AEEA-72BE6614AF98}</Property>
				<Property Name="Bld_removeVIObj" Type="Int">2</Property>
				<Property Name="Bld_version.build" Type="Int">2</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">Destination Directory</Property>
				<Property Name="Destination[0].libraryName" Type="Str">PUBLIC.lvlib</Property>
				<Property Name="Destination[0].path" Type="Path">/C/builds/LV-KoRE-MQTT/NI_AB_PROJECTNAME/src/Public</Property>
				<Property Name="Destination[0].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">/C/builds/LV-KoRE-MQTT/NI_AB_PROJECTNAME/src/Public/data</Property>
				<Property Name="Destination[1].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="Destination[2].destName" Type="Str">Private</Property>
				<Property Name="Destination[2].libraryName" Type="Str">Private.lvlib</Property>
				<Property Name="Destination[2].path" Type="Path">/C/builds/LV-KoRE-MQTT/NI_AB_PROJECTNAME/src/Private</Property>
				<Property Name="Destination[2].path.type" Type="Str">&lt;none&gt;</Property>
				<Property Name="DestinationCount" Type="Int">3</Property>
				<Property Name="Source[0].itemID" Type="Str">{1F2B3A98-5BF4-4A5F-B1A5-757B6A5AE5DF}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">1</Property>
				<Property Name="Source[1].itemID" Type="Ref">/</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">1</Property>
				<Property Name="Source[2].itemID" Type="Ref">/</Property>
				<Property Name="Source[3].Container.applyInclusion" Type="Bool">true</Property>
				<Property Name="Source[3].Container.depDestIndex" Type="Int">0</Property>
				<Property Name="Source[3].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[3].itemID" Type="Ref">/</Property>
				<Property Name="Source[3].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[3].type" Type="Str">Container</Property>
				<Property Name="Source[4].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[4].Container.applyInclusion" Type="Bool">true</Property>
				<Property Name="Source[4].Container.depDestIndex" Type="Int">0</Property>
				<Property Name="Source[4].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[4].itemID" Type="Ref">/</Property>
				<Property Name="Source[4].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[4].type" Type="Str">Container</Property>
				<Property Name="SourceCount" Type="Int">5</Property>
			</Item>
		</Item>
	</Item>
</Project>
