# OpenTool SDK for LabVIEW

English · [中文](README-zh_CN.md)

The OpenTool LabVIEW SDK is used to implement an OpenTool Server within LabVIEW applications.

## Features

* Encapsulates a Web Service that follows the [OpenTool Spec](https://github.com/opentool-hub/opentool-spec)

    * LabVIEW default HTTP port: `8001` for Debug, `8080` for Release
    * To modify the default port, edit the NI WebServer configuration file, typically located on Windows at: `C:\Program Files (x86)\National Instruments\Shared\NI WebServer\NIWebAppServer.ini.defaults`

  ```
  [Default]
  Port = 8080
  ```
* Developers must implement the ITool interface and set it in the WebService's `Startup.vi`

## Usage

1. Create a Tool implementation class, for example `MockTool.lvclass`, which implements the `ITool` interface:

    * **Init.vi**: Used to initialize your tool
    * **Call.vi**: Handles OpenTool function calls and returns the execution result
    * **Load.vi**: Returns the tool description in JSON format according to the OpenSpec, e.g., `/Example/clac_tool.json`
    * **Close.vi**: Handles cleanup when the WebService stops
    * Example implementation can be found in `/Example/MockTool.lvclass`
2. Modify `Startup.vi` to add your Tool implementation class to the WebService, as shown:
   ![customize.png](img/customize.png)

* To verify: after starting the WebService, run `/Example/Main.vi` (ensure the configured port matches the WebService port)
