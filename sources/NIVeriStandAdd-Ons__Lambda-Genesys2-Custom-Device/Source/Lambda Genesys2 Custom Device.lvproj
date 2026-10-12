<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="11008008">
	<Item Name="My Computer" Type="My Computer">
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
		<Item Name="Custom Devices" Type="Folder">
			<Item Name="Lambda Genesys2 Custom Device.lvlib" Type="Library" URL="../Lambda Genesys2 Custom Device.lvlib"/>
			<Item Name="Custom Device Lambda Genesys2.xml" Type="Document" URL="../Custom Device Lambda Genesys2.xml"/>
		</Item>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="instr.lib" Type="Folder">
				<Item Name="GENser Write to Instrument.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Write to Instrument.vi"/>
				<Item Name="GENser Address Select.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/_GENser.llb/GENser Address Select.vi"/>
				<Item Name="GENser Checksum Append.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/_GENser.llb/GENser Checksum Append.vi"/>
				<Item Name="GENser Checksum Verify.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/_GENser.llb/GENser Checksum Verify.vi"/>
				<Item Name="GENser Convert Errors.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/_GENser.llb/GENser Convert Errors.vi"/>
				<Item Name="GENser Formulate VI Call Chain.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/_GENser.llb/GENser Formulate VI Call Chain.vi"/>
				<Item Name="GENser Wait.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Wait.vi"/>
				<Item Name="GENser Revision Query.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Revision Query.vi"/>
				<Item Name="GENser Read Instrument Data.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Read Instrument Data.vi"/>
				<Item Name="GENser Reset.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Reset.vi"/>
				<Item Name="GENser Close.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Close.vi"/>
				<Item Name="GENser Initialize.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Initialize.vi"/>
				<Item Name="GENser Config Voltage Limit.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Config Voltage Limit.vi"/>
				<Item Name="GENser Config Current Limit.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Config Current Limit.vi"/>
				<Item Name="GENser Config Output On-Off.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Config Output On-Off.vi"/>
				<Item Name="GENser Meas Output Voltage.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Meas Output Voltage.vi"/>
				<Item Name="GENser Meas Output Current.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Meas Output Current.vi"/>
				<Item Name="GENser CV-CC Query.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser CV-CC Query.vi"/>
				<Item Name="GENser Output On-Off Query.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Output On-Off Query.vi"/>
				<Item Name="GENser Fault Query.vi" Type="VI" URL="/&lt;instrlib&gt;/GENser/GENser.llb/GENser Fault Query.vi"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="General Error Handler CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler CORE.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="Custom Device API.lvlib" Type="Library" URL="/&lt;vilib&gt;/NI Veristand/Custom Device API/Custom Device API.lvlib"/>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Configuration" Type="Source Distribution">
				<Property Name="App_enableDebugging" Type="Bool">false</Property>
				<Property Name="App_fileVersion.build" Type="Int">0</Property>
				<Property Name="App_fileVersion.major" Type="Int">0</Property>
				<Property Name="App_fileVersion.minor" Type="Int">0</Property>
				<Property Name="App_fileVersion.patch" Type="Int">0</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{7A6DEFDD-E304-4554-B17A-4B576A02440A}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Configuration</Property>
				<Property Name="Bld_compilerOptLevel" Type="Int">0</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../Built/Lambda Genesys2/Lambda Genesys2 Configuration.llb</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{EA2F0375-3D53-4729-BA67-69A4ECAD15BC}</Property>
				<Property Name="Destination[0].destName" Type="Str">Destination Directory</Property>
				<Property Name="Destination[0].path" Type="Path">../Built/Lambda Genesys2/Lambda Genesys2 Configuration.llb</Property>
				<Property Name="Destination[0].type" Type="Str">LLB</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../Built/Lambda Genesys2/data</Property>
				<Property Name="Destination[2].destName" Type="Str">CD Dir</Property>
				<Property Name="Destination[2].path" Type="Path">../Built/Lambda Genesys2</Property>
				<Property Name="DestinationCount" Type="Int">3</Property>
				<Property Name="Source[0].itemID" Type="Str">{E1D36722-D705-4A2F-8F3C-1BD70C795FB5}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/Custom Devices/Lambda Genesys2 Custom Device.lvlib</Property>
				<Property Name="Source[1].Library.allowMissingMembers" Type="Bool">true</Property>
				<Property Name="Source[1].type" Type="Str">Library</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[2].itemID" Type="Ref">/My Computer/Custom Devices/Lambda Genesys2 Custom Device.lvlib/Configuration/Lambda Genesys Main Page.vi</Property>
				<Property Name="Source[2].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[2].type" Type="Str">VI</Property>
				<Property Name="Source[2].VI.LLBtopLevel" Type="Bool">true</Property>
				<Property Name="Source[3].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[3].itemID" Type="Ref">/My Computer/Custom Devices/Lambda Genesys2 Custom Device.lvlib/Configuration/Lambda Genesys Initialization VI.vi</Property>
				<Property Name="Source[3].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[3].type" Type="Str">VI</Property>
				<Property Name="Source[3].VI.LLBtopLevel" Type="Bool">true</Property>
				<Property Name="Source[4].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[4].itemID" Type="Ref">/My Computer/Custom Devices/Lambda Genesys2 Custom Device.lvlib/Shared/Lambda Genesys Device Properties.vi</Property>
				<Property Name="Source[4].type" Type="Str">VI</Property>
				<Property Name="Source[5].destinationIndex" Type="Int">2</Property>
				<Property Name="Source[5].itemID" Type="Ref">/My Computer/Custom Devices/Custom Device Lambda Genesys2.xml</Property>
				<Property Name="Source[5].sourceInclusion" Type="Str">Include</Property>
				<Property Name="SourceCount" Type="Int">6</Property>
			</Item>
			<Item Name="Engine" Type="Source Distribution">
				<Property Name="Bld_buildCacheID" Type="Str">{58953E54-60A8-4429-B3F8-EBC18F45580C}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Engine</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../Built/Lambda Genesys2/Lambda Genesys2 Engine.llb</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{D9122530-46A7-4EC4-BE2C-45EFE01397C6}</Property>
				<Property Name="Destination[0].destName" Type="Str">Destination Directory</Property>
				<Property Name="Destination[0].path" Type="Path">../Built/Lambda Genesys2/Lambda Genesys2 Engine.llb</Property>
				<Property Name="Destination[0].type" Type="Str">LLB</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../Built/Lambda Genesys2/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{A646C734-440F-405F-A8FD-0ACF03581C4C}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/Custom Devices/Lambda Genesys2 Custom Device.lvlib/Engine/Lambda Genesys Engine.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
			</Item>
		</Item>
	</Item>
</Project>
