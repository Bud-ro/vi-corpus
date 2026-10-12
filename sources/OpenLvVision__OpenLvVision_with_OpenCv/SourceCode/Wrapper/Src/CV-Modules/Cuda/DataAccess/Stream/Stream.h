#pragma once

// CUDA Stream requires x64 — not supported on x86
#ifdef _WIN64

#include "opencv2/core/cuda.hpp"
#include "../../../../Interorp/Edvr/EdvrTypes.h"
#include "../../../../Interorp/Edvr/EdvrObject.hpp"
#include "../../../../Interorp/ErrorHandling/ErrorHandling.h"

cv::cuda::Stream resolveStream(lvi::edvr::ReferencePtr streamRef);

extern "C"
{

#pragma region Create / Destroy

    _declspec(dllexport) void CV_CUDA_STREAM_Create(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef);

    _declspec(dllexport) void CV_CUDA_STREAM_CreateWithFlags(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int32_t cudaFlags);

#pragma endregion Create / Destroy

#pragma region Synchronization

    _declspec(dllexport) void CV_CUDA_STREAM_WaitForCompletion(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef);

    _declspec(dllexport) void CV_CUDA_STREAM_QueryIfComplete(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        LVBoolean* result);

    _declspec(dllexport) void CV_CUDA_STREAM_WaitEvent(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr streamRef,
        lvi::edvr::ReferencePtr eventRef);

#pragma endregion Synchronization

#pragma region Info

    _declspec(dllexport) void CV_CUDA_STREAM_IsNonDefault(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        LVBoolean* result);

#pragma endregion Info

}

#endif
