# Bioreactor HMI – LabVIEW

![LabVIEW](https://img.shields.io/badge/LabVIEW-HMI-blue)
![Control](https://img.shields.io/badge/Control-Process%20Control-orange)
![Instrumentation](https://img.shields.io/badge/Instrumentation-Sensors%20%26%20DAQ-green)
![Process](https://img.shields.io/badge/Process-Bioreactor-lightgrey)
![License](https://img.shields.io/badge/License-MIT-lightgrey)


## 📌 Overview
This repository contains a **LabVIEW-based Human–Machine Interface (HMI)** developed between **2017–2018** for an **academic bioreactor laboratory**, with a strong focus on **process instrumentation, supervision, and operator interaction**.

Although originally developed for a laboratory environment, the system addresses challenges commonly found in **industrial process monitoring**, such as sensor supervision, threshold-based control, data logging, and safe operator operation.

The repository includes the **original LabVIEW code** and a complete **operations manual** used by laboratory users.

## 📂 Contents

- `/App bioreactor` → LabVIEW VIs for HMI, data acquisition, and control logic.
- `/Manual de operaciones bioreactor` → Operation manual and supporting documentation *(Spanish)*.


## 📊 Project Status
Legacy project – developed between 2017–2018, completed and archived.

## 🧪 Process Description
The system centralizes the supervision of **two independent bioreactors**, each instrumented with:

- **pH transmitter**
- **Dissolved Oxygen (DO) transmitter**

The HMI interfaces with **two Emerson Rosemount 1056 transmitters**, used for pH and Dissolved Oxygen measurement, providing a unified monitoring and control interface.

A **National Instruments NI USB-6002** data acquisition device is used to receive pH and Dissolved Oxygen measurements from the transmitters and to control the peristaltic pumps through digital on/off outputs.

## 🧩 System Architecture
The system integrates **Emerson Rosemount 1056** transmitters, a **National Instruments NI USB-6002** data acquisition device, and a supervisory HMI developed in **LabVIEW**.

pH and Dissolved Oxygen signals are acquired via the NI USB-6002, processed in LabVIEW for visualization and data logging, and used to drive the on/off control of peristaltic pumps through digital outputs.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8f1d9158-fb00-4f74-8a13-fca6314abaea" width="650">
</p>

<p align="center">
  <sub>Signal flow and connection overview between transmitters, data acquisition hardware, and HMI.</sub>
</p>


## ⚙️ Control Strategy
- **On/Off control** of peristaltic pumps
- **Manual / Automatic** operation modes
- Threshold-based pH control logic
- Operator-selectable control direction (above or below threshold)

This strategy prioritizes **operational simplicity, safety, and robustness**, which are key requirements in laboratory, pilot-plant, and auxiliary industrial systems.



## 📊 HMI Features
- Centralized monitoring of two **Emerson Rosemount 1056** transmitters
- Real-time visualization of pH and Dissolved Oxygen
- Trend plots for both variables
- Threshold and parameter configuration
- Sensor calibration using linear adjustment
- Data acquisition with logging to `.xlsx` files
- Centralized operator control panel
- Visual indicators for pump status and operating mode



## 🖥️ HMI and System Setup

### HMI – Idle State & Operating Mode
Interface layout without active signals (idle) and HMI operating with live pH and Dissolved Oxygen signals.

<table>
  <tr>
    <td align="center">
      <img alt="HMI idle" src="https://github.com/user-attachments/assets/24695724-24d8-4f2b-8b6d-e7cc1d836732" width="450">
    </td>
    <td align="center">
      <img alt="HMI operating" src="https://github.com/user-attachments/assets/a7027afc-d1ae-4bf2-975e-af85b3a8788c" width="400">
    </td>
  </tr>
</table>

### Instrumentation and Laboratory Setup

<table>
  <tr>
    <td align="center">
      <img alt="field wiring" src="https://github.com/user-attachments/assets/c219355d-0021-4c7e-a5d7-fa0b0e8aa629" width="300">
    </td>
    <td align="center">
      <img alt="lab setup" src="https://github.com/user-attachments/assets/d669b75a-4d24-4f3a-985b-30b17107657b" width="480">
    </td>
  </tr>
</table>


## 📘 Documentation
A complete **Operations Manual** is included in this repository, originally developed for laboratory deployment.

The manual covers:
- System overview and application purpose
- Detailed HMI description
- General operating procedures
- Parameter configuration and sensor calibration
- Sampling period configuration
- Data logging workflow
- Manual and automatic pH control operation

All figures and interface captures included in the manual correspond to the **original application used in a real academic laboratory environment**.

📄 See:  
**Manual_Operaciones_Biorreactor.pdf** *(Spanish)*

## 🧰 Software
- **LabVIEW 2013**

## 🏭 Industrial Relevance
The concepts and architecture implemented in this project are directly transferable to industrial environments, including:

- Process instrumentation and sensor supervision
- Operator-focused HMI design
- Threshold-based control strategies
- Manual / automatic operation modes
- Data acquisition and historical logging
- Safe handling of process actuators

These principles are commonly applied in **mining, chemical processing, water treatment, and energy systems**, particularly in pilot plants, test benches, and auxiliary process units.

## 📚 Lessons Learned
- Importance of clear operator-focused HMI design
- Robust handling of industrial transmitter signals
- Benefits of centralized supervision for multiple process units
- Practical considerations for threshold-based control in laboratory systems


## ⚠️ Disclaimer
This project is provided for **documentation and reference purposes only**.

- Originally developed for an academic laboratory environment.
- Not intended for direct industrial deployment without further engineering, validation, and safety assessment.
- Hardware references correspond to the original experimental setup.

The repository aims to showcase **instrumentation, control logic, and HMI design practices**, rather than a production-ready system.

## 🤝 Support projects
 Support me on Patreon [https://www.patreon.com/c/CrissCCL](https://www.patreon.com/c/CrissCCL)

## 📜 License
MIT License
