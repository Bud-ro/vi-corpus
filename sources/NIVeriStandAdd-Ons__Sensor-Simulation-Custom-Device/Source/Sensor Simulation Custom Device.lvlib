<?xml version='1.0' encoding='UTF-8'?>
<Library LVVersion="11008008">
	<Property Name="NI.Lib.Icon" Type="Bin">%1#!#!!!!!)!"1!&amp;!!!-!%!!!@````]!!!!"!!%!!!(]!!!*Q(C=\&gt;8"=&gt;MQ%!8143;(8.6"2CVM#WJ",7Q,SN&amp;(N&lt;!NK!7VM#WI"&lt;8A0$%94UZ2$P%E"Y.?G@I%A7=11U&gt;M\7P%FXB^VL\`NHV=@X&lt;^39O0^N(_&lt;8NZOEH@@=^_CM?,3)VK63LD-&gt;8LS%=_]J'0@/1N&lt;XH,7^\SFJ?]Z#5P?=F,HP+5JTTF+5`Z&gt;MB$(P+1)YX*RU2DU$(![)Q3YW.YBG&gt;YBM@8'*\B':\B'2Z&gt;9HC':XC':XD=&amp;M-T0--T0-.DK%USWS(H'2\$2`-U4`-U4`/9-JKH!&gt;JE&lt;?!W#%;UC_WE?:KH?:R']T20]T20]\A=T&gt;-]T&gt;-]T?/7&lt;66[UTQ//9^BIHC+JXC+JXA-(=640-640-6DOCC?YCG)-G%:(#(+4;6$_6)]R?.8&amp;%`R&amp;%`R&amp;)^,WR/K&lt;75?GM=BZUG?Z%G?Z%E?1U4S*%`S*%`S'$;3*XG3*XG3RV320-G40!G3*D6^J-(3D;F4#J,(T\:&lt;=HN+P5FS/S,7ZIWV+7.NNFC&lt;+.&lt;GC0819TX-7!]JVO,(7N29CR6L%7,^=&lt;(1M4#R*IFV][.DX(X?V&amp;6&gt;V&amp;G&gt;V&amp;%&gt;V&amp;\N(L@_Z9\X_TVONVN=L^?Y8#ZR0J`D&gt;$L&amp;]8C-Q_%1_`U_&gt;LP&gt;WWPAG_0NB@$TP@4C`%`KH@[8`A@PRPA=PYZLD8Y!#/7SO!!!!!!</Property>
	<Property Name="NI.Lib.Version" Type="Str">1.0.0.0</Property>
	<Property Name="NI.SortType" Type="Int">3</Property>
	<Item Name="Real Time" Type="Folder">
		<Item Name="Utilities" Type="Folder">
			<Item Name="Get Output Channel Registers.vi" Type="VI" URL="../Real-Time/Utility/Get Output Channel Registers.vi"/>
			<Item Name="Get Input Channel Registers.vi" Type="VI" URL="../Real-Time/Utility/Get Input Channel Registers.vi"/>
			<Item Name="FPGA Init.vi" Type="VI" URL="../Real-Time/Utility/FPGA Init.vi"/>
		</Item>
		<Item Name="TypeDefs" Type="Folder">
			<Item Name="OutputChannelTypes.ctl" Type="VI" URL="../Real-Time/TypeDefs/OutputChannelTypes.ctl"/>
			<Item Name="InputChannelTypes.ctl" Type="VI" URL="../Real-Time/TypeDefs/InputChannelTypes.ctl"/>
			<Item Name="EngineSimConfig.ctl" Type="VI" URL="../Real-Time/TypeDefs/EngineSimConfig.ctl"/>
			<Item Name="NTeethConfig.ctl" Type="VI" URL="../Real-Time/TypeDefs/NTeethConfig.ctl"/>
			<Item Name="FullyCustomConfig.ctl" Type="VI" URL="../Real-Time/TypeDefs/FullyCustomConfig.ctl"/>
			<Item Name="FullyCustomProfileConfig.ctl" Type="VI" URL="../Real-Time/TypeDefs/FullyCustomProfileConfig.ctl"/>
			<Item Name="SensorType.ctl" Type="VI" URL="../Real-Time/TypeDefs/SensorType.ctl"/>
			<Item Name="SensorParameters.ctl" Type="VI" URL="../Real-Time/TypeDefs/SensorParameters.ctl"/>
			<Item Name="SensorStateVariables.ctl" Type="VI" URL="../Real-Time/TypeDefs/SensorStateVariables.ctl"/>
			<Item Name="4 Wire xVDT Parameters.ctl" Type="VI" URL="../Real-Time/TypeDefs/4 Wire xVDT Parameters.ctl"/>
			<Item Name="5 Wire xVDT Parameters.ctl" Type="VI" URL="../Real-Time/TypeDefs/5 Wire xVDT Parameters.ctl"/>
			<Item Name="Resolver Parameters.ctl" Type="VI" URL="../Real-Time/TypeDefs/Resolver Parameters.ctl"/>
		</Item>
		<Item Name="SubVIs" Type="Folder">
			<Item Name="Initialize4WirexVDTParameters.vi" Type="VI" URL="../Real-Time/SubVIs/Initialize4WirexVDTParameters.vi"/>
			<Item Name="Initialize5WirexVDTParameters.vi" Type="VI" URL="../Real-Time/SubVIs/Initialize5WirexVDTParameters.vi"/>
			<Item Name="InitializeResolverParameters.vi" Type="VI" URL="../Real-Time/SubVIs/InitializeResolverParameters.vi"/>
			<Item Name="Write4WirexVDTParameters.vi" Type="VI" URL="../Real-Time/SubVIs/Write4WirexVDTParameters.vi"/>
			<Item Name="Write5WirexVDTParameters.vi" Type="VI" URL="../Real-Time/SubVIs/Write5WirexVDTParameters.vi"/>
			<Item Name="WriteResolverParameters.vi" Type="VI" URL="../Real-Time/SubVIs/WriteResolverParameters.vi"/>
			<Item Name="Read User Data.vi" Type="VI" URL="../Real-Time/SubVIs/Read User Data.vi"/>
		</Item>
		<Item Name="Sensor Simulation RT Driver VI.vi" Type="VI" URL="../Real-Time/Sensor Simulation RT Driver VI.vi"/>
	</Item>
	<Item Name="System Explorer" Type="Folder">
		<Item Name="Actions" Type="Folder">
			<Item Name="Main On Compile Action VI.vi" Type="VI" URL="../System Explorer/Actions/Main On Compile Action VI.vi"/>
			<Item Name="Main On Load Action VI.vi" Type="VI" URL="../System Explorer/Actions/Main On Load Action VI.vi"/>
		</Item>
		<Item Name="Pages" Type="Folder">
			<Item Name="Sensor Simulation Main Page.vi" Type="VI" URL="../System Explorer/Pages/Sensor Simulation Main Page.vi"/>
			<Item Name="Resolver Page.vi" Type="VI" URL="../System Explorer/Pages/Resolver Page.vi"/>
			<Item Name="xVDT Page.vi" Type="VI" URL="../System Explorer/Pages/xVDT Page.vi"/>
		</Item>
		<Item Name="Run-Time Menus" Type="Folder">
			<Item Name="RunTimeMenu Change GUID_Disable.vi" Type="VI" URL="../System Explorer/RTMs/RunTimeMenu Change GUID_Disable.vi"/>
			<Item Name="RunTimeMenu Change GUID_Enable.vi" Type="VI" URL="../System Explorer/RTMs/RunTimeMenu Change GUID_Enable.vi"/>
		</Item>
		<Item Name="Utilities" Type="Folder">
			<Item Name="Parse Bitfile Registers" Type="Folder">
				<Item Name="Parse Controls for xVDTs.vi" Type="VI" URL="../System Explorer/Utility/Parse Controls for xVDTs.vi"/>
				<Item Name="Add Found xVDT to Array.vi" Type="VI" URL="../System Explorer/Utility/Add Found xVDT to Array.vi"/>
				<Item Name="Add Found Resolver to Aarray.vi" Type="VI" URL="../System Explorer/Utility/Add Found Resolver to Aarray.vi"/>
				<Item Name="Parse Controls for Resolvers.vi" Type="VI" URL="../System Explorer/Utility/Parse Controls for Resolvers.vi"/>
			</Item>
			<Item Name="Get Bitfile Checksum.vi" Type="VI" URL="../System Explorer/Utility/Get Bitfile Checksum.vi"/>
			<Item Name="Get Available Sensor Sim Components.vi" Type="VI" URL="../System Explorer/Utility/Get Available Sensor Sim Components.vi"/>
			<Item Name="Bitfile Component Check.vi" Type="VI" URL="../System Explorer/Utility/Bitfile Component Check.vi"/>
			<Item Name="Get FPGA Dependent File.vi" Type="VI" URL="../System Explorer/Utility/Get FPGA Dependent File.vi"/>
			<Item Name="Select FPGA.vi" Type="VI" URL="../System Explorer/Utility/Select FPGA.vi"/>
			<Item Name="Get LV Version Year.vi" Type="VI" URL="../System Explorer/Utility/Get LV Version Year.vi"/>
		</Item>
		<Item Name="TypeDefs" Type="Folder">
			<Item Name="Resolver.ctl" Type="VI" URL="../System Explorer/TypeDefs/Resolver.ctl"/>
			<Item Name="SensorSimComps.ctl" Type="VI" URL="../System Explorer/TypeDefs/SensorSimComps.ctl"/>
			<Item Name="xVDT.ctl" Type="VI" URL="../System Explorer/TypeDefs/xVDT.ctl"/>
		</Item>
		<Item Name="Sensor Simulation Initialization VI.vi" Type="VI" URL="../System Explorer/Sensor Simulation Initialization VI.vi"/>
		<Item Name="Sensor Simulation.chm" Type="Document" URL="../System Explorer/Sensor Simulation.chm"/>
	</Item>
	<Item Name="Global.vi" Type="VI" URL="../Global.vi"/>
</Library>
