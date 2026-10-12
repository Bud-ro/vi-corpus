#pragma once

#ifdef _WIN64

#include "opencv2/core/cuda.hpp"
#include "../../../../Interorp/Edvr/EdvrTypes.h"
#include "../../../../Interorp/ErrorHandling/ErrorHandling.h"

extern "C"
{

#pragma region Create / Destroy

    _declspec(dllexport) void CV_CUDA_EVENT_Create(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int32_t createFlags);

#pragma endregion Create / Destroy

#pragma region Record / Synchronize

    _declspec(dllexport) void CV_CUDA_EVENT_Record(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr eventRef,
        lvi::edvr::ReferencePtr streamRef);

    _declspec(dllexport) void CV_CUDA_EVENT_WaitForCompletion(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef);

    _declspec(dllexport) void CV_CUDA_EVENT_QueryIfComplete(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        LVBoolean* result);

#pragma endregion Record / Synchronize

#pragma region Timing

    _declspec(dllexport) void CV_CUDA_EVENT_ElapsedTime(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr startRef,
        lvi::edvr::ReferencePtr endRef,
        float* elapsedMs);

#pragma endregion Timing

}

#endif
