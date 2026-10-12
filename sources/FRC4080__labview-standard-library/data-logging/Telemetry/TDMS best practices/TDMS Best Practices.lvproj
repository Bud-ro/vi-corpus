<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="10008000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
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
		<Item Name="SubVIs" Type="Folder">
			<Item Name="TDMS Write Single Type.vi" Type="VI" URL="../SubVIs/TDMS Write Single Type.vi"/>
			<Item Name="TDMS Write Standard.vi" Type="VI" URL="../SubVIs/TDMS Write Standard.vi"/>
			<Item Name="TDMS Write with Buffer Prop.vi" Type="VI" URL="../SubVIs/TDMS Write with Buffer Prop.vi"/>
		</Item>
		<Item Name="Test VI.vi" Type="VI" URL="../Test VI.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="TDMS Generate Random Data (DBL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (DBL).vi"/>
				<Item Name="TDMS Generate Random Data (I8).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (I8).vi"/>
				<Item Name="TDMS Generate Random Data (I16).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (I16).vi"/>
				<Item Name="TDMS Generate Random Data (I32).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (I32).vi"/>
				<Item Name="TDMS Generate Random Data (I64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (I64).vi"/>
				<Item Name="TDMS Generate Random Data (SGL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (SGL).vi"/>
				<Item Name="TDMS Generate Random Data (U8).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (U8).vi"/>
				<Item Name="TDMS Generate Random Data (U16).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (U16).vi"/>
				<Item Name="TDMS Generate Random Data (U32).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (U32).vi"/>
				<Item Name="TDMS Generate Random Data (U64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data (U64).vi"/>
				<Item Name="TDMS Generate Random Data.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tdmsutil.llb/TDMS Generate Random Data.vi"/>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
