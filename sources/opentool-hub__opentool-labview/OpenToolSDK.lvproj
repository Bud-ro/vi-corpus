<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="17008000">
	<Item Name="我的电脑" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">我的电脑/VI服务器</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">我的电脑/VI服务器</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Client" Type="Folder">
			<Item Name="AddAuth.vi" Type="VI" URL="../Client/AddAuth.vi"/>
			<Item Name="GET-Load.vi" Type="VI" URL="../Client/GET-Load.vi"/>
			<Item Name="GET-Version.vi" Type="VI" URL="../Client/GET-Version.vi"/>
			<Item Name="ParseResponseStatus.vi" Type="VI" URL="../Client/ParseResponseStatus.vi"/>
			<Item Name="POST-Call.vi" Type="VI" URL="../Client/POST-Call.vi"/>
		</Item>
		<Item Name="Daemon" Type="Folder">
			<Item Name="GetPID.vi" Type="VI" URL="../Daemon/GetPID.vi"/>
			<Item Name="Register.vi" Type="VI" URL="../Daemon/Register.vi"/>
		</Item>
		<Item Name="Example" Type="Folder">
			<Item Name="Main.vi" Type="VI" URL="../Example/Main.vi"/>
			<Item Name="MockTool.lvclass" Type="LVClass" URL="../Example/MockTool.lvclass"/>
		</Item>
		<Item Name="Model" Type="Folder">
			<Item Name="FunctionCall.ctl" Type="VI" URL="../Model/FunctionCall.ctl"/>
			<Item Name="JsonRPCHttpRequestBody.ctl" Type="VI" URL="../Model/JsonRPCHttpRequestBody.ctl"/>
			<Item Name="JsonRPCHttpResponseBody.ctl" Type="VI" URL="../Model/JsonRPCHttpResponseBody.ctl"/>
			<Item Name="JsonRPCHttpResponseBodyError.ctl" Type="VI" URL="../Model/JsonRPCHttpResponseBodyError.ctl"/>
			<Item Name="ToolReturn.ctl" Type="VI" URL="../Model/ToolReturn.ctl"/>
			<Item Name="Version.ctl" Type="VI" URL="../Model/Version.ctl"/>
		</Item>
		<Item Name="Server" Type="Folder">
			<Item Name="Private" Type="Folder">
				<Item Name="CheckAuth.vi" Type="VI" URL="../Server/CheckAuth.vi"/>
				<Item Name="FunctionCallToJsonRpcRequestCluster.vi" Type="VI" URL="../Private/FunctionCallToJsonRpcRequestCluster.vi"/>
				<Item Name="IToolFGV.vi" Type="VI" URL="../Private/IToolFGV.vi"/>
				<Item Name="JsonRpcRequestClusterToString.vi" Type="VI" URL="../Private/JsonRpcRequestClusterToString.vi"/>
				<Item Name="JsonRpcRequestStringToCluster.vi" Type="VI" URL="../Private/JsonRpcRequestStringToCluster.vi"/>
				<Item Name="JsonRpcResponseClusterToString.vi" Type="VI" URL="../Private/JsonRpcResponseClusterToString.vi"/>
				<Item Name="JsonRpcResponseClusterToToolReturn.vi" Type="VI" URL="../Private/JsonRpcResponseClusterToToolReturn.vi"/>
				<Item Name="JsonRpcResponseStringToCluster.vi" Type="VI" URL="../Private/JsonRpcResponseStringToCluster.vi"/>
				<Item Name="RespondUnauth.vi" Type="VI" URL="../Server/RespondUnauth.vi"/>
				<Item Name="ToolReturnToJsonRpcResponseCluster.vi" Type="VI" URL="../Private/ToolReturnToJsonRpcResponseCluster.vi"/>
			</Item>
			<Item Name="GetITool.vi" Type="VI" URL="../Server/GetITool.vi"/>
			<Item Name="GetLoad.vi" Type="VI" URL="../Server/GetLoad.vi"/>
			<Item Name="ITool.lvclass" Type="LVClass" URL="../Server/ITool/ITool.lvclass"/>
			<Item Name="PostCall.vi" Type="VI" URL="../Server/PostCall.vi"/>
		</Item>
		<Item Name="opentool" Type="Web Service">
			<Property Name="ws.autoIncrementVersion" Type="Bool">false</Property>
			<Property Name="ws.disconnectInline" Type="Bool">true</Property>
			<Property Name="ws.disconnectTypeDefs" Type="Bool">false</Property>
			<Property Name="ws.guid" Type="Str">{3FCDAD58-CDF0-4B21-813D-CC24A88C55C7}</Property>
			<Property Name="ws.modifyLibraryFile" Type="Bool">true</Property>
			<Property Name="ws.remoteDebugging" Type="Bool">false</Property>
			<Property Name="ws.removeLibraryItems" Type="Bool">true</Property>
			<Property Name="ws.removePolyVIs" Type="Bool">true</Property>
			<Property Name="ws.serveDefaultDoc" Type="Bool">false</Property>
			<Property Name="ws.SSE2" Type="Bool">false</Property>
			<Property Name="ws.static_permissions" Type="Str"></Property>
			<Property Name="ws.version.build" Type="Int">0</Property>
			<Property Name="ws.version.fix" Type="Int">0</Property>
			<Property Name="ws.version.major" Type="Int">0</Property>
			<Property Name="ws.version.minor" Type="Int">1</Property>
			<Item Name="Web资源" Type="HTTP WebResources Container">
				<Item Name="call.vi" Type="VI" URL="../Server/call.vi">
					<Property Name="ws.buffered" Type="Bool">true</Property>
					<Property Name="ws.includeNameInURL" Type="Bool">true</Property>
					<Property Name="ws.keepInMemory" Type="Bool">true</Property>
					<Property Name="ws.loadAtStartup" Type="Bool">true</Property>
					<Property Name="ws.method" Type="Int">3</Property>
					<Property Name="ws.outputFormat" Type="Int">4</Property>
					<Property Name="ws.outputType" Type="Int">1</Property>
					<Property Name="ws.permissions" Type="Str"></Property>
					<Property Name="ws.requireAPIKey" Type="Bool">false</Property>
					<Property Name="ws.type" Type="Int">1</Property>
					<Property Name="ws.uri" Type="Str"></Property>
					<Property Name="ws.useHeaders" Type="Bool">true</Property>
					<Property Name="ws.useStandardURL" Type="Bool">true</Property>
				</Item>
				<Item Name="load.vi" Type="VI" URL="../Server/load.vi">
					<Property Name="ws.buffered" Type="Bool">true</Property>
					<Property Name="ws.includeNameInURL" Type="Bool">true</Property>
					<Property Name="ws.keepInMemory" Type="Bool">true</Property>
					<Property Name="ws.loadAtStartup" Type="Bool">true</Property>
					<Property Name="ws.method" Type="Int">1</Property>
					<Property Name="ws.outputFormat" Type="Int">4</Property>
					<Property Name="ws.outputType" Type="Int">1</Property>
					<Property Name="ws.permissions" Type="Str"></Property>
					<Property Name="ws.requireAPIKey" Type="Bool">false</Property>
					<Property Name="ws.type" Type="Int">1</Property>
					<Property Name="ws.uri" Type="Str"></Property>
					<Property Name="ws.useHeaders" Type="Bool">true</Property>
					<Property Name="ws.useStandardURL" Type="Bool">true</Property>
				</Item>
				<Item Name="version.vi" Type="VI" URL="../Server/version.vi">
					<Property Name="ws.buffered" Type="Bool">true</Property>
					<Property Name="ws.includeNameInURL" Type="Bool">true</Property>
					<Property Name="ws.keepInMemory" Type="Bool">true</Property>
					<Property Name="ws.loadAtStartup" Type="Bool">true</Property>
					<Property Name="ws.method" Type="Int">1</Property>
					<Property Name="ws.outputFormat" Type="Int">4</Property>
					<Property Name="ws.outputType" Type="Int">1</Property>
					<Property Name="ws.permissions" Type="Str"></Property>
					<Property Name="ws.requireAPIKey" Type="Bool">false</Property>
					<Property Name="ws.type" Type="Int">1</Property>
					<Property Name="ws.uri" Type="Str"></Property>
					<Property Name="ws.useHeaders" Type="Bool">true</Property>
					<Property Name="ws.useStandardURL" Type="Bool">true</Property>
				</Item>
			</Item>
			<Item Name="启动VI" Type="Startup VIs Container">
				<Item Name="Startup.vi" Type="VI" URL="../Server/Startup.vi">
					<Property Name="ws.type" Type="Int">2</Property>
				</Item>
			</Item>
		</Item>
		<Item Name="依赖关系" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="i3-json.lvlib" Type="Library" URL="/&lt;vilib&gt;/LVH/i3 JSON/i3-json.lvlib"/>
				<Item Name="LabVIEWHTTPClient.lvlib" Type="Library" URL="/&lt;vilib&gt;/httpClient/LabVIEWHTTPClient.lvlib"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="NI_WebServices.lvlib" Type="Library" URL="/&lt;vilib&gt;/wsapi/NI_WebServices.lvlib"/>
				<Item Name="Path To Command Line String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Path To Command Line String.vi"/>
				<Item Name="PathToUNIXPathString.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/CFURL.llb/PathToUNIXPathString.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
			</Item>
			<Item Name="GetApiKeys.vi" Type="VI" URL="../Server/ITool/GetApiKeys.vi"/>
			<Item Name="SetApiKeys.vi" Type="VI" URL="../Server/ITool/SetApiKeys.vi"/>
			<Item Name="System" Type="VI" URL="System">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="ws_runtime.dll" Type="Document" URL="ws_runtime.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="程序生成规范" Type="Build"/>
	</Item>
</Project>
