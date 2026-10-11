<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="20008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">20.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
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
		<Item Name="Testers" Type="Folder">
			<Item Name="Test Get Project.vi" Type="VI" URL="../Test Get Project.vi"/>
		</Item>
		<Item Name="1.vi" Type="VI" URL="../1.vi"/>
		<Item Name="2.vi" Type="VI" URL="../2.vi"/>
		<Item Name="Boolean Enum.ctl" Type="VI" URL="../Boolean Enum.ctl"/>
		<Item Name="Global.vi" Type="VI" URL="../Global.vi"/>
		<Item Name="Main.vi" Type="VI" URL="../Main.vi"/>
		<Item Name="Not Main.vi" Type="VI" URL="../Not Main.vi"/>
		<Item Name="Silent Main.vi" Type="VI" URL="../Silent Main.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
			</Item>
			<Item Name="Find VI in Project.vi" Type="VI" URL="../../Source/Find VI in Project.vi"/>
			<Item Name="Get Non-Qualified Name.vi" Type="VI" URL="../../Source/Get Non-Qualified Name.vi"/>
			<Item Name="Get Owning Project.vi" Type="VI" URL="../../Source/Get Owning Project.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
