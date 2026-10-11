#ifdef _WIN64

#include "Device.h"
#include <string.h>

using namespace cv;
using namespace cv::cuda;
using namespace lvi;
using namespace lvi::error;
using namespace lvi::string;

#pragma region Initialization and Information

_declspec(dllexport) void CV_CUDA_DEVICE_GetCudaEnabledDeviceCount(lvi::error::ErrorClusterPtr errorCluster,
    int32_t* count)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        *count = getCudaEnabledDeviceCount();
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_DEVICE_SetDevice(lvi::error::ErrorClusterPtr errorCluster,
    int32_t device)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        setDevice(device);
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_DEVICE_GetDevice(lvi::error::ErrorClusterPtr errorCluster,
    int32_t* device)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        *device = getDevice();
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_DEVICE_ResetDevice(lvi::error::ErrorClusterPtr errorCluster)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        resetDevice();
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_DEVICE_GetDeviceInfo(lvi::error::ErrorClusterPtr errorCluster,
    int32_t device, CudaDeviceInfo* info)
{
    handleError(errorCluster, [&]() -> MgErr
    {	

		int targetDevice ;
        if (device < 0)
        {
			targetDevice = getDevice();
        }
        else
        {
			targetDevice = device;
        }
    
        DeviceInfo devInfo(targetDevice);

        setLvStringHandle(info->nameHandle, devInfo.name());
        info->majorVersion = devInfo.majorVersion();
        info->minorVersion = devInfo.minorVersion();
        info->totalMemory = static_cast<uint64_t>(devInfo.totalMemory());
        info->freeMemory = static_cast<uint64_t>(devInfo.freeMemory());
        info->isCompatible = devInfo.isCompatible() ? 1 : 0;

        return mgNoErr;
    });
}

#pragma endregion Initialization and Information

#pragma region TargetArchs

_declspec(dllexport) void CV_CUDA_DEVICE_TargetArchsHas(lvi::error::ErrorClusterPtr errorCluster,
    int32_t major, int32_t minor, LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        *result = TargetArchs::has(major, minor) ? 1 : 0;
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_DEVICE_TargetArchsHasBin(lvi::error::ErrorClusterPtr errorCluster,
    int32_t major, int32_t minor, LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        *result = TargetArchs::hasBin(major, minor) ? 1 : 0;
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_DEVICE_TargetArchsHasPtx(lvi::error::ErrorClusterPtr errorCluster,
    int32_t major, int32_t minor, LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        *result = TargetArchs::hasPtx(major, minor) ? 1 : 0;
        return mgNoErr;
    });
}

#pragma endregion TargetArchs

#endif // _WIN64
