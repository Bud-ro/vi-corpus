#pragma once

#ifdef _WIN64

#include "opencv2/core/cuda.hpp"
#include "../../../../Interorp/Edvr/EdvrTypes.h"
#include "../../../../Interorp/Edvr/EdvrObject.hpp"
#include "../../../../Interorp/MatHandling/MatHandling.h"
#include "../../../../Interorp/ErrorHandling/ErrorHandling.h"
#include "../../../../Interorp/ArrayHandling/Array1D.hpp"
#include "../../../../Interorp/Points.hpp"
#include "../Stream/Stream.h"

#include "opencv2/cudaarithm.hpp"

struct GpuMatInfo
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

    _declspec(dllexport) void CV_CUDA_GPUMAT_CreateEmpty(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef);

    _declspec(dllexport) void CV_CUDA_GPUMAT_CreateSized(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int32_t rows, int32_t cols,int32_t cvType,
        lvi::array::LV_1DArrayHandle<double_t> constantHandle);

    _declspec(dllexport) void CV_CUDA_GPUMAT_CreateRoi(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        lvi::point::PointI32* size,
        lvi::point::PointI32* topLeft);

    _declspec(dllexport) void CV_CUDA_GPUMAT_ReCreate(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int32_t rows, int32_t cols,
        int32_t cvType);

#pragma endregion Create / Destroy

#pragma region Upload / Download HostMem

    _declspec(dllexport) void CV_CUDA_GPUMAT_UploadFromHostMem(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr gpuMatRef,
        lvi::edvr::ReferencePtr hostMemRef,
        lvi::edvr::ReferencePtr streamRef);

    _declspec(dllexport) void CV_CUDA_GPUMAT_DownloadToHostMem(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr gpuMatRef,
        lvi::edvr::ReferencePtr hostMemRef,
        lvi::edvr::ReferencePtr streamRef);

#pragma endregion Upload / Download HostMem

#pragma region Upload / Download LV Buffer

    _declspec(dllexport) void CV_CUDA_GPUMAT_UploadFromLvMat(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr gpuMatRef,
        void* addressSrc, lvi::mat::MatInfo* matInfoSrc);

    _declspec(dllexport) void CV_CUDA_GPUMAT_DownloadToLvMat(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr gpuMatRef,
        void* addressDst, lvi::mat::MatInfo* matInfoDst);

#pragma endregion Upload / Download LV Buffer

#pragma region Data Operations

    _declspec(dllexport) void CV_CUDA_GPUMAT_SetTo(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        lvi::edvr::ReferencePtr MaskRef,
        lvi::edvr::ReferencePtr streamRef,
        lvi::array::LV_1DArrayHandle<double_t> constantHandle);

    _declspec(dllexport) void CV_CUDA_GPUMAT_ConvertTo(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        int32_t rtype, double alpha, double beta,
        lvi::edvr::ReferencePtr streamRef);

    _declspec(dllexport) void CV_CUDA_GPUMAT_CopyTo(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        lvi::edvr::ReferencePtr streamRef,
        lvi::edvr::ReferencePtr maskRef);

    _declspec(dllexport) void CV_CUDA_GPUMAT_Clone(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef);

    _declspec(dllexport) void CV_CUDA_GPUMAT_Reshape(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        int32_t cn, int32_t rows);

    _declspec(dllexport) void CV_CUDA_GPUMAT_Swap(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr refA,
        lvi::edvr::ReferencePtr refB);

    _declspec(dllexport) void CV_CUDA_GPUMAT_Row(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        int32_t y);

    _declspec(dllexport) void CV_CUDA_GPUMAT_Col(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        int32_t x);

    _declspec(dllexport) void CV_CUDA_GPUMAT_RowRange(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        int32_t startrow, int32_t endrow);

    _declspec(dllexport) void CV_CUDA_GPUMAT_ColRange(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr srcRef,
        lvi::edvr::ReferencePtr dstRef,
        int32_t startcol, int32_t endcol);

    _declspec(dllexport) void CV_CUDA_GPUMAT_AdjustROI(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int32_t dtop, int32_t dbottom, int32_t dleft, int32_t dright);

    _declspec(dllexport) void CV_CUDA_GPUMAT_LocateROI(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        lvi::point::PointI32* size,
        lvi::point::PointI32* topLeft);

#pragma endregion Data Operations

#pragma region Pointer Access (for external DLLs)

    struct GpuMat_PointerData 
    {
        uintptr_t cudaPtr;
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
  
    _declspec(dllexport) void CV_CUDA_GPUMAT_GetPointer(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        GpuMat_PointerData* PointerData);

    _declspec(dllexport) void CV_CUDA_GPUMAT_ReleasePointerExternal(void* handle);

    _declspec(dllexport) void CV_CUDA_GPUMAT_ReleasePointer(lvi::error::ErrorClusterPtr errorCluster,
        void* handle);  

#pragma endregion Pointer Access

#pragma region Info / Properties

    _declspec(dllexport) void CV_CUDA_GPUMAT_ReadInfo(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        GpuMatInfo* info);

    _declspec(dllexport) void CV_CUDA_GPUMAT_Empty(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        LVBoolean* result);

    _declspec(dllexport) void CV_CUDA_GPUMAT_IsContinuous(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        LVBoolean* result);

    _declspec(dllexport) void CV_CUDA_GPUMAT_GetElemSize(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* elemSize);

    _declspec(dllexport) void CV_CUDA_GPUMAT_GetElemSize1(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* elemSize1);

    _declspec(dllexport) void CV_CUDA_GPUMAT_GetStep(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* step);

    _declspec(dllexport) void CV_CUDA_GPUMAT_GetStep1(lvi::error::ErrorClusterPtr errorCluster,
        lvi::edvr::ReferencePtr edvrRef,
        int64_t* step1);

#pragma endregion Info / Properties

}

#endif
