<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="20008000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
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
		<Item Name="Documentation" Type="Folder">
			<Item Name="AdditionalDescription.vi" Type="VI" URL="../Documentation/AdditionalDescription.vi"/>
			<Item Name="GenerateHtmlDoc.vi" Type="VI" URL="../Documentation/GenerateHtmlDoc.vi"/>
			<Item Name="GernateViDoc.vi" Type="VI" URL="../Documentation/GernateViDoc.vi"/>
			<Item Name="HtmlPrepareHugo.vi" Type="VI" URL="../Documentation/HtmlPrepareHugo.vi"/>
		</Item>
		<Item Name="Install" Type="Folder">
			<Property Name="NI.SortType" Type="Int">3</Property>
			<Item Name="Pre-Install Custom Action.vi" Type="VI" URL="../OpenLvVision_OpenCv/Install/Pre-Install Custom Action.vi"/>
			<Item Name="Post-Install Custom Action.vi" Type="VI" URL="../OpenLvVision_OpenCv/Install/Post-Install Custom Action.vi"/>
		</Item>
		<Item Name="OpenLvVision_OpenCv.lvlib" Type="Library" URL="../OpenLvVision_OpenCv/OpenLvVision_OpenCv.lvlib"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Assert Array Dimension Count.vim" Type="VI" URL="/&lt;vilib&gt;/Utility/TypeAssert/Assert Array Dimension Count.vim"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Color (U64)" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Color (U64)"/>
				<Item Name="Create Directory Recursive.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Create Directory Recursive.vi"/>
				<Item Name="Create NI GUID.vi" Type="VI" URL="/&lt;vilib&gt;/string/Create NI GUID.vi"/>
				<Item Name="Delimited String to 1D String Array.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Delimited String to 1D String Array.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Escape Characters for HTTP.vi" Type="VI" URL="/&lt;vilib&gt;/printing/PathToURL.llb/Escape Characters for HTTP.vi"/>
				<Item Name="ex_CorrectErrorChain.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_CorrectErrorChain.vi"/>
				<Item Name="Get File Extension.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Get File Extension.vi"/>
				<Item Name="Image Type" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Image Type"/>
				<Item Name="Image Unit" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Image Unit"/>
				<Item Name="IMAQ Copy Overlay" Type="VI" URL="/&lt;vilib&gt;/vision/Overlay.llb/IMAQ Copy Overlay"/>
				<Item Name="IMAQ Create" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Create"/>
				<Item Name="IMAQ Dispose" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Dispose"/>
				<Item Name="IMAQ Get Custom Keys" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Get Custom Keys"/>
				<Item Name="IMAQ GetImageInfo" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ GetImageInfo"/>
				<Item Name="IMAQ GetImagePixelPtr" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ GetImagePixelPtr"/>
				<Item Name="IMAQ GetImageSize" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ GetImageSize"/>
				<Item Name="IMAQ Image Bit Depth" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Image Bit Depth"/>
				<Item Name="IMAQ Image.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/IMAQ Image.ctl"/>
				<Item Name="IMAQ Read Custom Data" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Read Custom Data"/>
				<Item Name="IMAQ SetImageSize" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ SetImageSize"/>
				<Item Name="IMAQ Write Custom Data" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Write Custom Data"/>
				<Item Name="LabVIEWHTTPClient.lvlib" Type="Library" URL="/&lt;vilib&gt;/httpClient/LabVIEWHTTPClient.lvlib"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_Matrix.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/Matrix/NI_Matrix.lvlib"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="NI_Unzip.lvlib" Type="Library" URL="/&lt;vilib&gt;/zip/NI_Unzip.lvlib"/>
				<Item Name="OLV_InstallerOpenCV.lvlib" Type="Library" URL="/&lt;vilib&gt;/OpenLvVision/OpenLvVision_OpenCv/Installer/OLV_InstallerOpenCV.lvlib"/>
				<Item Name="OLV_VisionCore_AVX2_X64.dll" Type="Document" URL="/&lt;vilib&gt;/OpenLvVision/OpenLvVision_Image/DLLs/OLV_VisionCore_AVX2_X64.dll"/>
				<Item Name="OLV_VisionCore_AVX2_X86.dll" Type="Document" URL="/&lt;vilib&gt;/OpenLvVision/OpenLvVision_Image/DLLs/OLV_VisionCore_AVX2_X86.dll"/>
				<Item Name="Open URL in Default Browser (path).vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser (path).vi"/>
				<Item Name="Open URL in Default Browser (string).vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser (string).vi"/>
				<Item Name="Open URL in Default Browser core.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser core.vi"/>
				<Item Name="Open URL in Default Browser.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/browser.llb/Open URL in Default Browser.vi"/>
				<Item Name="Path To Command Line String.vi" Type="VI" URL="/&lt;vilib&gt;/AdvancedString/Path To Command Line String.vi"/>
				<Item Name="Path to URL inner.vi" Type="VI" URL="/&lt;vilib&gt;/printing/PathToURL.llb/Path to URL inner.vi"/>
				<Item Name="Path to URL.vi" Type="VI" URL="/&lt;vilib&gt;/printing/PathToURL.llb/Path to URL.vi"/>
				<Item Name="PathToUNIXPathString.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/CFURL.llb/PathToUNIXPathString.vi"/>
				<Item Name="Space Constant.vi" Type="VI" URL="/&lt;vilib&gt;/dlg_ctls.llb/Space Constant.vi"/>
				<Item Name="subFile Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/express/express input/FileDialogBlock.llb/subFile Dialog.vi"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
			</Item>
			<Item Name="cublas64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cublas64_12.dll"/>
			<Item Name="cublasLt64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cublasLt64_12.dll"/>
			<Item Name="cudart64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudart64_12.dll"/>
			<Item Name="cudnn64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn64_9.dll"/>
			<Item Name="cudnn_adv64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn_adv64_9.dll"/>
			<Item Name="cudnn_cnn64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn_cnn64_9.dll"/>
			<Item Name="cudnn_engines_precompiled64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn_engines_precompiled64_9.dll"/>
			<Item Name="cudnn_engines_runtime_compiled64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn_engines_runtime_compiled64_9.dll"/>
			<Item Name="cudnn_graph64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn_graph64_9.dll"/>
			<Item Name="cudnn_heuristic64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn_heuristic64_9.dll"/>
			<Item Name="cudnn_ops64_9.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cudnn_ops64_9.dll"/>
			<Item Name="cufft64_11.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cufft64_11.dll"/>
			<Item Name="cufftw64_11.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cufftw64_11.dll"/>
			<Item Name="curand64_10.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/curand64_10.dll"/>
			<Item Name="cusolver64_11.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cusolver64_11.dll"/>
			<Item Name="cusolverMg64_11.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cusolverMg64_11.dll"/>
			<Item Name="cusparse64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/cusparse64_12.dll"/>
			<Item Name="nivision.dll" Type="Document" URL="nivision.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="nivissvc.dll" Type="Document" URL="nivissvc.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="nppc64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppc64_12.dll"/>
			<Item Name="nppial64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppial64_12.dll"/>
			<Item Name="nppicc64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppicc64_12.dll"/>
			<Item Name="nppidei64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppidei64_12.dll"/>
			<Item Name="nppif64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppif64_12.dll"/>
			<Item Name="nppig64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppig64_12.dll"/>
			<Item Name="nppim64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppim64_12.dll"/>
			<Item Name="nppist64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppist64_12.dll"/>
			<Item Name="nppisu64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppisu64_12.dll"/>
			<Item Name="nppitc64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nppitc64_12.dll"/>
			<Item Name="npps64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/npps64_12.dll"/>
			<Item Name="nvblas64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nvblas64_12.dll"/>
			<Item Name="nvfatbin_120_0.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nvfatbin_120_0.dll"/>
			<Item Name="nvJitLink_120_0.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nvJitLink_120_0.dll"/>
			<Item Name="nvjpeg64_12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nvjpeg64_12.dll"/>
			<Item Name="nvrtc-builtins64_129.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nvrtc-builtins64_129.dll"/>
			<Item Name="nvrtc64_120_0.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/nvrtc64_120_0.dll"/>
			<Item Name="opencv_world4130.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/opencv_world4130.dll"/>
			<Item Name="openvino.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino.dll"/>
			<Item Name="openvino_auto_batch_plugin.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_auto_batch_plugin.dll"/>
			<Item Name="openvino_auto_plugin.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_auto_plugin.dll"/>
			<Item Name="openvino_c.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_c.dll"/>
			<Item Name="openvino_hetero_plugin.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_hetero_plugin.dll"/>
			<Item Name="openvino_intel_cpu_plugin.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_intel_cpu_plugin.dll"/>
			<Item Name="openvino_intel_gpu_plugin.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_intel_gpu_plugin.dll"/>
			<Item Name="openvino_intel_npu_plugin.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_intel_npu_plugin.dll"/>
			<Item Name="openvino_ir_frontend.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_ir_frontend.dll"/>
			<Item Name="openvino_onnx_frontend.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_onnx_frontend.dll"/>
			<Item Name="openvino_paddle_frontend.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_paddle_frontend.dll"/>
			<Item Name="openvino_pytorch_frontend.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_pytorch_frontend.dll"/>
			<Item Name="openvino_tensorflow_frontend.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/openvino_tensorflow_frontend.dll"/>
			<Item Name="tbb12.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/tbb12.dll"/>
			<Item Name="tbbbind_2_5.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/tbbbind_2_5.dll"/>
			<Item Name="tbbmalloc.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/tbbmalloc.dll"/>
			<Item Name="tbbmalloc_proxy.dll" Type="Document" URL="../OpenLvVision_OpenCv/Dlls/tbbmalloc_proxy.dll"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
