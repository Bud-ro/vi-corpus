#pragma once

#ifdef _WIN64

#include "opencv2/core/cuda.hpp"
#include "../../../Interorp/ErrorHandling/ErrorHandling.h"
#include "../../../Interorp/Edvr/EdvrTypes.h"
#include "../../../Interorp/StringHandling/StringHandling.h"

struct CudaDeviceInfo
{
    LStrHandle nameHandle;
    int32_t majorVersion;
    int32_t minorVersion;
    uint64_t totalMemory;
    uint64_t freeMemory;
    LVBoolean isCompatible;
};

extern "C"
{

#pragma region Initialization and Information

    _declspec(dllexport) void CV_CUDA_DEVICE_GetCudaEnabledDeviceCount(lvi::error::ErrorClusterPtr errorCluster,
        int32_t* count);

    _declspec(dllexport) void CV_CUDA_DEVICE_SetDevice(lvi::error::ErrorClusterPtr errorCluster,
        int32_t device);

    _declspec(dllexport) void CV_CUDA_DEVICE_GetDevice(lvi::error::ErrorClusterPtr errorCluster,
        int32_t* device);

    _declspec(dllexport) void CV_CUDA_DEVICE_ResetDevice(lvi::error::ErrorClusterPtr errorCluster);

    _declspec(dllexport) void CV_CUDA_DEVICE_GetDeviceInfo(lvi::error::ErrorClusterPtr errorCluster,
        int32_t device, CudaDeviceInfo* info);

#pragma endregion Initialization and Information

#pragma region TargetArchs

    _declspec(dllexport) void CV_CUDA_DEVICE_TargetArchsHas(lvi::error::ErrorClusterPtr errorCluster,
        int32_t major, int32_t minor, LVBoolean* result);

    _declspec(dllexport) void CV_CUDA_DEVICE_TargetArchsHasBin(lvi::error::ErrorClusterPtr errorCluster,
        int32_t major, int32_t minor, LVBoolean* result);

    _declspec(dllexport) void CV_CUDA_DEVICE_TargetArchsHasPtx(lvi::error::ErrorClusterPtr errorCluster,
        int32_t major, int32_t minor, LVBoolean* result);

#pragma endregion TargetArchs

}

#endif // _WIN64
