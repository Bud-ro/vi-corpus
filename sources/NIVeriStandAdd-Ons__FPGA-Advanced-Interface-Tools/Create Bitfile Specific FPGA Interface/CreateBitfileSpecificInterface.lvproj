<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="10008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="IOScan.Faults" Type="Str"></Property>
		<Property Name="IOScan.NetVarPeriod" Type="UInt">100</Property>
		<Property Name="IOScan.NetWatchdogEnabled" Type="Bool">false</Property>
		<Property Name="IOScan.Period" Type="UInt">10000</Property>
		<Property Name="IOScan.PowerupMode" Type="UInt">0</Property>
		<Property Name="IOScan.Priority" Type="UInt">9</Property>
		<Property Name="IOScan.ReportModeConflict" Type="Bool">true</Property>
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
		<Item Name="SubVIs" Type="Folder">
			<Item Name="Update Ring Controls.vi" Type="VI" URL="../Update Ring Controls.vi"/>
			<Item Name="Get Control Data.vi" Type="VI" URL="../Get Control Data.vi"/>
			<Item Name="CreateLibrary ReturnTypeDefs.vi" Type="VI" URL="../CreateLibrary ReturnTypeDefs.vi"/>
			<Item Name="Convert Bitfile Data to RingTypeDef Data.vi" Type="VI" URL="../Convert Bitfile Data to RingTypeDef Data.vi"/>
			<Item Name="Add Default Menu.vi" Type="VI" URL="../Add Default Menu.vi"/>
			<Item Name="Replace MNU Files.vi" Type="VI" URL="../Replace MNU Files.vi"/>
		</Item>
		<Item Name="TypeDefs" Type="Folder">
			<Item Name="FpgaItemToSelect.ctl" Type="VI" URL="../TypeDefs/FpgaItemToSelect.ctl"/>
		</Item>
		<Item Name="No UI" Type="Folder">
			<Item Name="SubVIs" Type="Folder">
				<Item Name="Get TypeDef Info From Bitfile.vi" Type="VI" URL="../Get TypeDef Info From Bitfile.vi"/>
			</Item>
			<Item Name="Create BitfileSpecific FpgaInterface.vi" Type="VI" URL="../Create BitfileSpecific FpgaInterface.vi"/>
		</Item>
		<Item Name="Bitfile" Type="Folder">
			<Item Name="FPGA Bitfile Utility.lvlib" Type="Library" URL="/&lt;userlib&gt;/_FPGA Interface Advanced Tools/FPGA Bitfile Utility/FPGA Bitfile Utility.lvlib"/>
		</Item>
		<Item Name="Interface Base" Type="Folder">
			<Item Name="FPGA Interface Base.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/_FPGA Interface Advanced Tools/FPGA Interface Base/FPGA Interface Base.lvclass"/>
		</Item>
		<Item Name="Interface TypeDef" Type="Folder">
			<Item Name="FPGA Interface By TypeDefs.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/_FPGA Interface Advanced Tools/FPGA Interface By TypeDefs/FPGA Interface By TypeDefs.lvclass"/>
		</Item>
		<Item Name="Interface Wrapper" Type="Folder">
			<Item Name="FPGA Interface Wrapper.lvlib" Type="Library" URL="/&lt;userlib&gt;/_FPGA Interface Advanced Tools/FPGA Interface Wrapper/FPGA Interface Wrapper.lvlib"/>
		</Item>
		<Item Name="BitfileSpecific FpgaInterface Creation UserInterface.vi" Type="VI" URL="../BitfileSpecific FpgaInterface Creation UserInterface.vi"/>
		<Item Name="BSD License.rtf" Type="Document" URL="../../../../../Users/mlyons/Desktop/BSD License.rtf"/>
		<Item Name="dir.mnu" Type="Document" URL="/&lt;vilib&gt;/addons/FPGA Interfaces/dir.mnu"/>
		<Item Name="niFpgaGetSinkWriteWindowName.vi" Type="VI" URL="../../../../../Program Files (x86)/National Instruments/LabVIEW 2010/resource/RVI/CommunicationInterface/Utilities/niFpgaGetSinkWriteWindowName.vi"/>
		<Item Name="niLvFpgaGetDmaChannelInfoFromXML.vi" Type="VI" URL="../../../../../Program Files (x86)/National Instruments/LabVIEW 2010/resource/RVI/compilationResultUtilities/niLvFpgaGetDmaChannelInfoFromXML.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="VariantType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/VariantDataType/VariantType.lvlib"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="Get File Extension.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Get File Extension.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="General Error Handler CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler CORE.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Palette Menu.lvlib" Type="Library" URL="/&lt;vilib&gt;/Palette API/Palette Menu/Palette Menu.lvlib"/>
				<Item Name="FixBadRect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pictutil.llb/FixBadRect.vi"/>
				<Item Name="imagedata.ctl" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/imagedata.ctl"/>
				<Item Name="Draw Flattened Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Flattened Pixmap.vi"/>
				<Item Name="Empty Picture" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Empty Picture"/>
				<Item Name="Read Palette.vi" Type="VI" URL="/&lt;vilib&gt;/Palette API/Read Palette.vi"/>
				<Item Name="Picture to Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pictutil.llb/Picture to Pixmap.vi"/>
				<Item Name="Write Palette.vi" Type="VI" URL="/&lt;vilib&gt;/Palette API/Write Palette.vi"/>
				<Item Name="System Directory Type.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/sysdir.llb/System Directory Type.ctl"/>
				<Item Name="Get System Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/sysdir.llb/Get System Directory.vi"/>
				<Item Name="LVFixedPointRepRangeTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/fxp/LVFixedPointRepRangeTypeDef.ctl"/>
				<Item Name="LVFixedPointRepBitsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/fxp/LVFixedPointRepBitsTypeDef.ctl"/>
				<Item Name="UnescapeChar.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/xml.llb/UnescapeChar.vi"/>
			</Item>
			<Item Name="NiFpga.dll" Type="Document" URL="NiFpga.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="niFpgaDataTypeControl.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/DataTransferAndStorage/Container/Common/niFpgaDataTypeControl.ctl"/>
			<Item Name="niFpgaGenCallStack.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/errors/niFpgaGenCallStack.vi"/>
			<Item Name="nirviFillInErrorInfo.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/errors/nirviFillInErrorInfo.vi"/>
			<Item Name="niLvFpgaReportInternalErrorWithAdditionalInfo.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/errors/niLvFpgaReportInternalErrorWithAdditionalInfo.vi"/>
			<Item Name="nirviXML_TagType.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_TagType.ctl"/>
			<Item Name="nirviXML_FindTag.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_FindTag.vi"/>
			<Item Name="nirviXML_GetValueWithName.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValueWithName.vi"/>
			<Item Name="niFpgaCreateFxpVariantTypeFromAttributes.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/Variants/niFpgaCreateFxpVariantTypeFromAttributes.vi"/>
			<Item Name="nirviXML_GetValue_String.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_String.vi"/>
			<Item Name="nirviXML_GetValue_Double.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_Double.vi"/>
			<Item Name="nirviXML_GetValue_Boolean.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_Boolean.vi"/>
			<Item Name="nirviXML_GetValue_U32.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_U32.vi"/>
			<Item Name="nirviXML_GetValue_I32.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_I32.vi"/>
			<Item Name="nirviXML_GetNameAttribute.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetNameAttribute.vi"/>
			<Item Name="nirviXML_GetValue_String_Escaped.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_String_Escaped.vi"/>
			<Item Name="niFpgaDecodeBase64.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/niFpgaDecodeBase64.vi"/>
			<Item Name="nirviXML_GetValue_ArrayU32base64.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_ArrayU32base64.vi"/>
			<Item Name="nirviXML_GetValue_ArrayU8base64.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_ArrayU8base64.vi"/>
			<Item Name="nirviXML_GetValue_ArrayU8hex.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue_ArrayU8hex.vi"/>
			<Item Name="nirviXML_GetValue.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetValue.vi"/>
			<Item Name="nirviXML_Element.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_Element.ctl"/>
			<Item Name="nirviXML_GetChildren.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Utilities/XML/nirviXML_GetChildren.vi"/>
			<Item Name="niFpgaDmaChannelVisibilityFilter.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/ClientSDK/Host Interface/DMA/public/niFpgaDmaChannelVisibilityFilter.ctl"/>
			<Item Name="niFpgaDmaChannelImplementation.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/ClientSDK/Core/ModuleGeneration/CommunicationInterfaceUtility/niFpgaDmaChannelImplementation.ctl"/>
			<Item Name="Fifo_DMA_Config.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/FIFO/Fifo_Types/Fifo_DMA_Config.ctl"/>
			<Item Name="nirviTypdefDescription.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/Bitfile/nirviTypdefDescription.ctl"/>
			<Item Name="nirviClusterElementControl.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/Bitfile/nirviClusterElementControl.ctl"/>
			<Item Name="nirviSubControlStructure.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/Bitfile/nirviSubControlStructure.ctl"/>
			<Item Name="niFpgaReadBitfileXml_VIRegisterMapSubControls.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Bitfile/niFpgaReadBitfileXml_VIRegisterMapSubControls.vi"/>
			<Item Name="nirviMechanicalAction.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/Bitfile/nirviMechanicalAction.ctl"/>
			<Item Name="nirviControlStructure.ctl" Type="VI" URL="/&lt;vilib&gt;/rvi/Bitfile/nirviControlStructure.ctl"/>
			<Item Name="niFpgaReadBitfileXml_VIRegisterMap.vi" Type="VI" URL="/&lt;vilib&gt;/rvi/Bitfile/niFpgaReadBitfileXml_VIRegisterMap.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Create FPGA Interface" Type="Source Distribution">
				<Property Name="Bld_buildSpecName" Type="Str">Create FPGA Interface</Property>
				<Property Name="Bld_excludedDirectory[0]" Type="Path">vi.lib</Property>
				<Property Name="Bld_excludedDirectory[0].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[1]" Type="Path">resource/objmgr</Property>
				<Property Name="Bld_excludedDirectory[1].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[2]" Type="Path">/C/Users/mlyons/Documents/LabVIEW Data/InstCache</Property>
				<Property Name="Bld_excludedDirectory[3]" Type="Path">instr.lib</Property>
				<Property Name="Bld_excludedDirectory[3].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[4]" Type="Path">user.lib</Property>
				<Property Name="Bld_excludedDirectory[4].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectoryCount" Type="Int">5</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/CreateBitfileSpecificInterface/Create FPGA Interface.llb</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Destination[0].destName" Type="Str">Destination Directory</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/Create FPGA Interface.llb</Property>
				<Property Name="Destination[0].type" Type="Str">LLB</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{2E3EEFB4-DF91-48BD-9188-399D32939E10}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/BitfileSpecific FpgaInterface Creation UserInterface.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="Source[1].VI.LLBtopLevel" Type="Bool">true</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
			</Item>
			<Item Name="FPGA Adv Int Tools Source Dist" Type="Source Distribution">
				<Property Name="Bld_buildSpecName" Type="Str">FPGA Adv Int Tools Source Dist</Property>
				<Property Name="Bld_excludedDirectory[0]" Type="Path">vi.lib</Property>
				<Property Name="Bld_excludedDirectory[0].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[1]" Type="Path">resource/objmgr</Property>
				<Property Name="Bld_excludedDirectory[1].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[2]" Type="Path">/C/Users/mlyons/Documents/LabVIEW Data/InstCache</Property>
				<Property Name="Bld_excludedDirectory[3]" Type="Path">instr.lib</Property>
				<Property Name="Bld_excludedDirectory[3].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[4]" Type="Path">user.lib</Property>
				<Property Name="Bld_excludedDirectory[4].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectoryCount" Type="Int">5</Property>
				<Property Name="Bld_localDestDir" Type="Path">../_FPGA Interface Advanced Tools</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Destination[0].destName" Type="Str">Destination Directory</Property>
				<Property Name="Destination[0].path" Type="Path">../_FPGA Interface Advanced Tools</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../_FPGA Interface Advanced Tools/data</Property>
				<Property Name="Destination[10].destName" Type="Str">FPGA Interface Wrapper TypeDefs</Property>
				<Property Name="Destination[10].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Interface Wrapper/TypeDefs</Property>
				<Property Name="Destination[2].destName" Type="Str">FPGA Bitfile Utility</Property>
				<Property Name="Destination[2].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Bitfile Utility</Property>
				<Property Name="Destination[3].destName" Type="Str">FPGA Interface Base</Property>
				<Property Name="Destination[3].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Interface Base</Property>
				<Property Name="Destination[4].destName" Type="Str">FPGA Interface By TypeDefs</Property>
				<Property Name="Destination[4].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Interface By TypeDefs</Property>
				<Property Name="Destination[5].destName" Type="Str">FPGA Interface Wrapper</Property>
				<Property Name="Destination[5].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Interface Wrapper</Property>
				<Property Name="Destination[6].destName" Type="Str">FPGA Bitfile TypeDefs</Property>
				<Property Name="Destination[6].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Bitfile Utility/TypeDefs</Property>
				<Property Name="Destination[7].destName" Type="Str">FPGA Interface Base Accessors</Property>
				<Property Name="Destination[7].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Interface Base/Accessors</Property>
				<Property Name="Destination[8].destName" Type="Str">FPGA Interface Base TypeDefs</Property>
				<Property Name="Destination[8].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Interface Base/TypeDefs</Property>
				<Property Name="Destination[9].destName" Type="Str">FPGA Interface By TypeDefs TypeDefs</Property>
				<Property Name="Destination[9].path" Type="Path">../_FPGA Interface Advanced Tools/FPGA Interface By TypeDefs/TypeDefs</Property>
				<Property Name="DestinationCount" Type="Int">11</Property>
				<Property Name="Source[0].itemID" Type="Str">{7992FFC5-97B3-405B-A9CA-C59B86F00472}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib</Property>
				<Property Name="Source[1].Library.allowMissingMembers" Type="Bool">true</Property>
				<Property Name="Source[1].type" Type="Str">Library</Property>
				<Property Name="Source[10].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[10].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Get FIFO Offsets by Name and DataType.vi</Property>
				<Property Name="Source[10].type" Type="Str">VI</Property>
				<Property Name="Source[11].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[11].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Get FIFO Data.vi</Property>
				<Property Name="Source[11].type" Type="Str">VI</Property>
				<Property Name="Source[12].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[12].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/dir.mnu</Property>
				<Property Name="Source[12].lvfile" Type="Bool">true</Property>
				<Property Name="Source[13].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[13].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/advanced.mnu</Property>
				<Property Name="Source[13].lvfile" Type="Bool">true</Property>
				<Property Name="Source[14].Container.applyInclusion" Type="Bool">true</Property>
				<Property Name="Source[14].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[14].itemID" Type="Ref">/My Computer/Bitfile</Property>
				<Property Name="Source[14].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[14].type" Type="Str">Container</Property>
				<Property Name="Source[15].Container.applyInclusion" Type="Bool">true</Property>
				<Property Name="Source[15].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[15].itemID" Type="Ref">/My Computer/Interface Base</Property>
				<Property Name="Source[15].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[15].type" Type="Str">Container</Property>
				<Property Name="Source[16].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[16].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass</Property>
				<Property Name="Source[16].type" Type="Str">Library</Property>
				<Property Name="Source[17].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[17].destinationIndex" Type="Int">8</Property>
				<Property Name="Source[17].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/TypeDefs</Property>
				<Property Name="Source[17].type" Type="Str">Container</Property>
				<Property Name="Source[18].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[18].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[18].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Palette Files</Property>
				<Property Name="Source[18].type" Type="Str">Container</Property>
				<Property Name="Source[19].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[19].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[19].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Read\/Write</Property>
				<Property Name="Source[19].type" Type="Str">Container</Property>
				<Property Name="Source[2].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">6</Property>
				<Property Name="Source[2].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/TypeDefs</Property>
				<Property Name="Source[2].type" Type="Str">Container</Property>
				<Property Name="Source[20].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[20].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[20].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/FIFO</Property>
				<Property Name="Source[20].type" Type="Str">Container</Property>
				<Property Name="Source[21].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[21].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[21].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/IRQs</Property>
				<Property Name="Source[21].type" Type="Str">Container</Property>
				<Property Name="Source[22].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[22].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[22].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Utilities</Property>
				<Property Name="Source[22].type" Type="Str">Container</Property>
				<Property Name="Source[23].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[23].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/FPGA Open Reference.vi</Property>
				<Property Name="Source[23].type" Type="Str">VI</Property>
				<Property Name="Source[24].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[24].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/FPGA Close Reference.vi</Property>
				<Property Name="Source[24].type" Type="Str">VI</Property>
				<Property Name="Source[25].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[25].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Palette Files/dir.mnu</Property>
				<Property Name="Source[25].lvfile" Type="Bool">true</Property>
				<Property Name="Source[26].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[26].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Palette Files/FIFO Utility.mnu</Property>
				<Property Name="Source[26].lvfile" Type="Bool">true</Property>
				<Property Name="Source[27].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[27].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Palette Files/Utility.mnu</Property>
				<Property Name="Source[27].lvfile" Type="Bool">true</Property>
				<Property Name="Source[28].Container.applyInclusion" Type="Bool">true</Property>
				<Property Name="Source[28].destinationIndex" Type="Int">4</Property>
				<Property Name="Source[28].itemID" Type="Ref">/My Computer/Interface TypeDef</Property>
				<Property Name="Source[28].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[28].type" Type="Str">Container</Property>
				<Property Name="Source[29].destinationIndex" Type="Int">4</Property>
				<Property Name="Source[29].itemID" Type="Ref">/My Computer/Interface TypeDef/FPGA Interface By TypeDefs.lvclass</Property>
				<Property Name="Source[29].type" Type="Str">Library</Property>
				<Property Name="Source[3].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[3].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[3].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Uses RVI Top-Level</Property>
				<Property Name="Source[3].type" Type="Str">Container</Property>
				<Property Name="Source[30].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[30].destinationIndex" Type="Int">9</Property>
				<Property Name="Source[30].itemID" Type="Ref">/My Computer/Interface TypeDef/FPGA Interface By TypeDefs.lvclass/TypeDefs</Property>
				<Property Name="Source[30].type" Type="Str">Container</Property>
				<Property Name="Source[31].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[31].destinationIndex" Type="Int">4</Property>
				<Property Name="Source[31].itemID" Type="Ref">/My Computer/Interface TypeDef/FPGA Interface By TypeDefs.lvclass/Palette Files</Property>
				<Property Name="Source[31].type" Type="Str">Container</Property>
				<Property Name="Source[32].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[32].destinationIndex" Type="Int">4</Property>
				<Property Name="Source[32].itemID" Type="Ref">/My Computer/Interface TypeDef/FPGA Interface By TypeDefs.lvclass/Read\/Write</Property>
				<Property Name="Source[32].type" Type="Str">Container</Property>
				<Property Name="Source[33].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[33].destinationIndex" Type="Int">4</Property>
				<Property Name="Source[33].itemID" Type="Ref">/My Computer/Interface TypeDef/FPGA Interface By TypeDefs.lvclass/FIFO</Property>
				<Property Name="Source[33].type" Type="Str">Container</Property>
				<Property Name="Source[34].destinationIndex" Type="Int">4</Property>
				<Property Name="Source[34].itemID" Type="Ref">/My Computer/Interface TypeDef/FPGA Interface By TypeDefs.lvclass/FPGA Open Reference By TypeDef.vi</Property>
				<Property Name="Source[34].type" Type="Str">VI</Property>
				<Property Name="Source[35].Container.applyInclusion" Type="Bool">true</Property>
				<Property Name="Source[35].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[35].itemID" Type="Ref">/My Computer/Interface Wrapper</Property>
				<Property Name="Source[35].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[35].type" Type="Str">Container</Property>
				<Property Name="Source[36].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[36].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib</Property>
				<Property Name="Source[36].Library.allowMissingMembers" Type="Bool">true</Property>
				<Property Name="Source[36].type" Type="Str">Library</Property>
				<Property Name="Source[37].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[37].destinationIndex" Type="Int">10</Property>
				<Property Name="Source[37].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/TypeDefs</Property>
				<Property Name="Source[37].type" Type="Str">Container</Property>
				<Property Name="Source[38].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[38].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[38].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/Palette Files</Property>
				<Property Name="Source[38].type" Type="Str">Container</Property>
				<Property Name="Source[39].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[39].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[39].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/Read\/Write</Property>
				<Property Name="Source[39].type" Type="Str">Container</Property>
				<Property Name="Source[4].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[4].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[4].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/XML Utilities</Property>
				<Property Name="Source[4].type" Type="Str">Container</Property>
				<Property Name="Source[40].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[40].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[40].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/FIFO</Property>
				<Property Name="Source[40].type" Type="Str">Container</Property>
				<Property Name="Source[41].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[41].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[41].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/IRQs</Property>
				<Property Name="Source[41].type" Type="Str">Container</Property>
				<Property Name="Source[42].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[42].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[42].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/Utilities</Property>
				<Property Name="Source[42].type" Type="Str">Container</Property>
				<Property Name="Source[43].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[43].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/NiFPGA Open.vi</Property>
				<Property Name="Source[43].type" Type="Str">VI</Property>
				<Property Name="Source[44].destinationIndex" Type="Int">5</Property>
				<Property Name="Source[44].itemID" Type="Ref">/My Computer/Interface Wrapper/FPGA Interface Wrapper.lvlib/NiFPGA Close.vi</Property>
				<Property Name="Source[44].type" Type="Str">VI</Property>
				<Property Name="Source[45].destinationIndex" Type="Int">7</Property>
				<Property Name="Source[45].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Accessors/FPGA Session/FPGA Read Session.vi</Property>
				<Property Name="Source[45].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[45].type" Type="Str">VI</Property>
				<Property Name="Source[46].destinationIndex" Type="Int">7</Property>
				<Property Name="Source[46].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Accessors/IRQ Context Queue/FPGA Read IRQ Context Queue.vi</Property>
				<Property Name="Source[46].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[46].type" Type="Str">VI</Property>
				<Property Name="Source[47].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[47].destinationIndex" Type="Int">7</Property>
				<Property Name="Source[47].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Accessors/Address Accessors By Name</Property>
				<Property Name="Source[47].type" Type="Str">Container</Property>
				<Property Name="Source[48].Container.applyDestination" Type="Bool">true</Property>
				<Property Name="Source[48].destinationIndex" Type="Int">7</Property>
				<Property Name="Source[48].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Accessors/Address Accessors By Index</Property>
				<Property Name="Source[48].type" Type="Str">Container</Property>
				<Property Name="Source[49].destinationIndex" Type="Int">3</Property>
				<Property Name="Source[49].itemID" Type="Ref">/My Computer/Interface Base/FPGA Interface Base.lvclass/Accessors/FPGA Initialize Session.vi</Property>
				<Property Name="Source[49].type" Type="Str">VI</Property>
				<Property Name="Source[5].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[5].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Get Control Data.vi</Property>
				<Property Name="Source[5].type" Type="Str">VI</Property>
				<Property Name="Source[50].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[50].itemID" Type="Ref">/My Computer/niFpgaGetSinkWriteWindowName.vi</Property>
				<Property Name="Source[50].sourceInclusion" Type="Str">Exclude</Property>
				<Property Name="Source[50].type" Type="Str">VI</Property>
				<Property Name="Source[51].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[51].itemID" Type="Ref">/My Computer/niLvFpgaGetDmaChannelInfoFromXML.vi</Property>
				<Property Name="Source[51].sourceInclusion" Type="Str">Exclude</Property>
				<Property Name="Source[51].type" Type="Str">VI</Property>
				<Property Name="Source[6].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[6].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Get Control Data - Sorted by Name.vi</Property>
				<Property Name="Source[6].type" Type="Str">VI</Property>
				<Property Name="Source[7].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[7].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Get Control Offsets by Name.vi</Property>
				<Property Name="Source[7].type" Type="Str">VI</Property>
				<Property Name="Source[8].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[8].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Get Control Offsets by Name and DataType.vi</Property>
				<Property Name="Source[8].type" Type="Str">VI</Property>
				<Property Name="Source[9].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[9].itemID" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib/Get FIFO Offsets by Name.vi</Property>
				<Property Name="Source[9].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">52</Property>
			</Item>
			<Item Name="FPGA Adv Int Tools Installer" Type="Installer">
				<Property Name="Destination[0].name" Type="Str">project</Property>
				<Property Name="Destination[0].parent" Type="Str">{E20B5188-6575-4366-9109-D4EA9AB7500C}</Property>
				<Property Name="Destination[0].tag" Type="Str">{C2517DEB-9AF1-4A3D-8E77-729F85E01407}</Property>
				<Property Name="Destination[0].type" Type="Str">userFolder</Property>
				<Property Name="Destination[1].name" Type="Str">vi.lib</Property>
				<Property Name="Destination[1].parent" Type="Str">{E20B5188-6575-4366-9109-D4EA9AB7500C}</Property>
				<Property Name="Destination[1].tag" Type="Str">{CB277C01-81D8-4DFF-A873-DF4C280DFF45}</Property>
				<Property Name="Destination[1].type" Type="Str">userFolder</Property>
				<Property Name="Destination[2].name" Type="Str">addons</Property>
				<Property Name="Destination[2].parent" Type="Str">{CB277C01-81D8-4DFF-A873-DF4C280DFF45}</Property>
				<Property Name="Destination[2].tag" Type="Str">{E642C95E-DCE0-45B6-8256-EC7A0C2FDCBF}</Property>
				<Property Name="Destination[2].type" Type="Str">userFolder</Property>
				<Property Name="Destination[3].name" Type="Str">FPGA Interfaces</Property>
				<Property Name="Destination[3].parent" Type="Str">{E642C95E-DCE0-45B6-8256-EC7A0C2FDCBF}</Property>
				<Property Name="Destination[3].tag" Type="Str">{461A502E-6633-4EFF-AB31-25B2B9D7FAD5}</Property>
				<Property Name="Destination[3].type" Type="Str">userFolder</Property>
				<Property Name="Destination[4].name" Type="Str">_FPGA Interface Advanced Tools</Property>
				<Property Name="Destination[4].parent" Type="Str">{BD1765DB-3210-4900-9237-D82CD1B02148}</Property>
				<Property Name="Destination[4].tag" Type="Str">{5C10D5ED-24EE-4326-8FB2-04616F8A72B5}</Property>
				<Property Name="Destination[4].type" Type="Str">userFolder</Property>
				<Property Name="DestinationCount" Type="Int">5</Property>
				<Property Name="INST_author" Type="Str">NI</Property>
				<Property Name="INST_autoIncrement" Type="Bool">true</Property>
				<Property Name="INST_buildLocation" Type="Path">/C/Tortoise/LabVIEW FPGA Advanced Interface Tools/Source/builds/FPGA Interface Advanced Tools/FPGA Adv Int Tools Installer</Property>
				<Property Name="INST_buildSpecName" Type="Str">FPGA Adv Int Tools Installer</Property>
				<Property Name="INST_defaultDir" Type="Str">{E20B5188-6575-4366-9109-D4EA9AB7500C}</Property>
				<Property Name="INST_includeError" Type="Bool">false</Property>
				<Property Name="INST_productName" Type="Str">LabVIEW FPGA Advanced Interface Tools</Property>
				<Property Name="INST_productVersion" Type="Str">1.0.5</Property>
				<Property Name="INST_requireLVDevSys" Type="Bool">true</Property>
				<Property Name="InstSpecBitness" Type="Str">32-bit</Property>
				<Property Name="MSI_arpCompany" Type="Str">NI</Property>
				<Property Name="MSI_arpContact" Type="Str">Mike Lyons</Property>
				<Property Name="MSI_arpURL" Type="Str">http://www.ni.com/</Property>
				<Property Name="MSI_distID" Type="Str">{A0AE67F8-F8F4-4608-8A39-DB4873F3EDF8}</Property>
				<Property Name="MSI_licenseID" Type="Ref">/My Computer/BSD License.rtf</Property>
				<Property Name="MSI_osCheck" Type="Int">0</Property>
				<Property Name="MSI_upgradeCode" Type="Str">{D3593570-D1C1-4506-9D12-55DF1F98A60E}</Property>
				<Property Name="MSI_windowTitle" Type="Str">LabVIEW FPGA Advanced Interface Tools</Property>
				<Property Name="RegDest[0].dirName" Type="Str">Software</Property>
				<Property Name="RegDest[0].dirTag" Type="Str">{DDFAFC8B-E728-4AC8-96DE-B920EBB97A86}</Property>
				<Property Name="RegDest[0].parentTag" Type="Str">2</Property>
				<Property Name="RegDestCount" Type="Int">1</Property>
				<Property Name="Source[0].dest" Type="Str">{C2517DEB-9AF1-4A3D-8E77-729F85E01407}</Property>
				<Property Name="Source[0].File[0].dest" Type="Str">{C2517DEB-9AF1-4A3D-8E77-729F85E01407}</Property>
				<Property Name="Source[0].File[0].name" Type="Str">Create FPGA Interface.llb</Property>
				<Property Name="Source[0].File[0].tag" Type="Str">{C31F4114-72E8-49D7-8951-CCC304076E3F}</Property>
				<Property Name="Source[0].FileCount" Type="Int">1</Property>
				<Property Name="Source[0].name" Type="Str">Create FPGA Interface</Property>
				<Property Name="Source[0].tag" Type="Ref">/My Computer/Build Specifications/Create FPGA Interface</Property>
				<Property Name="Source[0].type" Type="Str">SDIST</Property>
				<Property Name="Source[1].dest" Type="Str">{461A502E-6633-4EFF-AB31-25B2B9D7FAD5}</Property>
				<Property Name="Source[1].name" Type="Str">dir.mnu</Property>
				<Property Name="Source[1].tag" Type="Ref">/My Computer/dir.mnu</Property>
				<Property Name="Source[1].type" Type="Str">File</Property>
				<Property Name="Source[2].dest" Type="Str">{5C10D5ED-24EE-4326-8FB2-04616F8A72B5}</Property>
				<Property Name="Source[2].File[0].dest" Type="Str">{5C10D5ED-24EE-4326-8FB2-04616F8A72B5}</Property>
				<Property Name="Source[2].File[0].name" Type="Str">FPGA Bitfile Utility.lvlib</Property>
				<Property Name="Source[2].File[0].tag" Type="Ref">/My Computer/Bitfile/FPGA Bitfile Utility.lvlib</Property>
				<Property Name="Source[2].FileCount" Type="Int">1</Property>
				<Property Name="Source[2].name" Type="Str">FPGA Adv Int Tools Source Dist</Property>
				<Property Name="Source[2].tag" Type="Ref">/My Computer/Build Specifications/FPGA Adv Int Tools Source Dist</Property>
				<Property Name="Source[2].type" Type="Str">SDIST</Property>
				<Property Name="SourceCount" Type="Int">3</Property>
			</Item>
		</Item>
	</Item>
</Project>
