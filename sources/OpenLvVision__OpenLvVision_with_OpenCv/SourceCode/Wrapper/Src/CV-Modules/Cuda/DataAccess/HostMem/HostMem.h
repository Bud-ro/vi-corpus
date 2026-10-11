#pragma once

#ifdef _WIN64

#include "opencv2/core/cuda.hpp"
#include "../../../../Interorp/Edvr/EdvrTypes.h"
#include "../../../../Interorp/MatHandling/MatHandling.h"
#include "../../../../Interorp/ErrorHandling/ErrorHandling.h"


struct HostMatInfo
{
    int32_t rows;
    int32_t cols;
    uint32_t cvType;
    int32_t channels;
    int32_t depth;
};


extern "C"
{

#pragma region Create / Destroy

    _declspec(dllexport) void CV_CUDA_HOSTMEM_CreateEmpty(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int32_t allocType);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_CreateSized(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int32_t rows, int32_t cols, 
        int32_t cvType, int32_t allocType);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_CreateFromLvMat(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        void* addressSrc, lvi::mat::MatInfo* matInfoSrc, int32_t allocType);

#pragma endregion Create / Destroy

#pragma region Memory Management

    _declspec(dllexport) void CV_CUDA_HOSTMEM_Swap(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRefA,
        lvi::edvr::ReferencePtr edvrRefB);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_Clone(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRefSrc,
        lvi::edvr::ReferencePtr edvrRefDst);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_Reshape(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRefSrc,
        lvi::edvr::ReferencePtr edvrRefDst,
        int32_t cn, int32_t rows);

#pragma endregion Memory Management

#pragma region Data Transfer

    _declspec(dllexport) void CV_CUDA_HOSTMEM_CopyFromLvMat(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        void* addressSrc, lvi::mat::MatInfo* matInfoSrc);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_CopyToLvMat(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        void* addressDst, lvi::mat::MatInfo* matInfoDst);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_CreateGpuMatHeader(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr hostMemRef,
        lvi::edvr::ReferencePtr gpuMatRef);

#pragma endregion Data Transfer

#pragma region Pointer Access (for external DLLs)

    struct HostMem_PointerData 
    {
        uintptr_t dataPtr;
        int64_t   step;
        uint64_t  totalBytes;
        int32_t   cols;
        int32_t   rows;
        int32_t   elemSize;
        int32_t   cvType;
        int32_t   channels;
        uintptr_t handlePtr;
        uintptr_t releaseCallbackPtr;
    };
  
    _declspec(dllexport) void CV_CUDA_HOSTMEM_GetPointer(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        HostMem_PointerData* PointerData);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_ReleasePointerExternal(void* handle);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_ReleasePointer(lvi::error::ErrorClusterPtr errorCluster,
        void* handle);    

#pragma endregion Pointer Access

#pragma region Info / Properties

    _declspec(dllexport) void CV_CUDA_HOSTMEM_ReadInfo(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        HostMatInfo* info);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_GetElemSize(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* elemSize);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_GetElemSize1(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* elemSize1);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_GetStep(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* step);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_GetStep1(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* step1);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_Empty(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        LVBoolean* result);

    _declspec(dllexport) void CV_CUDA_HOSTMEM_IsContinuous(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        LVBoolean* result);

#pragma endregion Info / Properties

}

#endif
