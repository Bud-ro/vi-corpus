#ifdef _WIN64

#include "HostMem.h"

using namespace cv;
using namespace cv::cuda;
using namespace lvi;
using namespace lvi::mat;
using namespace lvi::error;
using namespace lvi::edvr;

static HostMem::AllocType toAllocType(int32_t allocType)
{
    switch (allocType)
    {
        case 0:  return HostMem::PAGE_LOCKED;
        case 1:  return HostMem::SHARED;
        case 2:  return HostMem::WRITE_COMBINED;
        default: return HostMem::PAGE_LOCKED;
    }
}

#pragma region Create / Destroy

_declspec(dllexport) void CV_CUDA_HOSTMEM_CreateEmpty(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int32_t allocType)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef, new HostMem(toAllocType(allocType)));

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_CreateSized(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int32_t rows, int32_t cols, 
    int32_t cvType, int32_t allocType)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef, new HostMem(rows, cols, cvType, toAllocType(allocType)));

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_CreateFromLvMat(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    void* addressSrc, lvi::mat::MatInfo* matInfoSrc, int32_t allocType)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        Mat srcMat = lvMatToCvMat(addressSrc, matInfoSrc);

        if (srcMat.empty())
        {
            throw std::runtime_error("Source Mat is empty, cannot create HostMem.");
        }

        // HostMem(InputArray, AllocType) constructor copies data into pinned memory
        EdvrObject<HostMem> obj(edvrRef, new HostMem(srcMat, toAllocType(allocType)));

        return mgNoErr;
    });
}

#pragma endregion Create / Destroy

#pragma region Memory Management

_declspec(dllexport) void CV_CUDA_HOSTMEM_Swap(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRefA,
    lvi::edvr::ReferencePtr edvrRefB)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> objA(edvrRefA);
        EdvrObject<HostMem> objB(edvrRefB);

        objA->swap(*objB);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_Clone(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRefSrc,
    lvi::edvr::ReferencePtr edvrRefDst)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> src(edvrRefSrc);
        EdvrObject<HostMem> dst(edvrRefDst, new HostMem(src->clone()));

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_Reshape(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRefSrc,
    lvi::edvr::ReferencePtr edvrRefDst,
    int32_t cn, int32_t rows)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> src(edvrRefSrc);

        EdvrObject<HostMem> dst(edvrRefDst, new HostMem(src->reshape(cn, rows)));

        return mgNoErr;
    });
}

#pragma endregion Memory Management

#pragma region Data Transfer

_declspec(dllexport) void CV_CUDA_HOSTMEM_CopyFromLvMat(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    void* addressSrc, lvi::mat::MatInfo* matInfoSrc)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);
        Mat srcMat = lvMatToCvMat(addressSrc, matInfoSrc);

        if (srcMat.empty())
        {
            throw std::runtime_error("Source Mat is empty.");
        }

        Mat dstMat = obj->createMatHeader();

        if (dstMat.empty())
        {
            throw std::runtime_error("HostMem is empty.");
        }

        if (srcMat.size() != dstMat.size() || srcMat.type() != dstMat.type())
        {
            throw std::runtime_error("Source Mat size/type does not match HostMem.");
        }

        srcMat.copyTo(dstMat);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_CopyToLvMat(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    void* addressDst, lvi::mat::MatInfo* matInfoDst)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);
        Mat dstMat = lvMatToCvMat(addressDst, matInfoDst);

        if (obj->empty())
        {
            throw std::runtime_error("HostMem is empty, nothing to copy.");
        }

        Mat srcMat = obj->createMatHeader();

        if (srcMat.size() != dstMat.size() || srcMat.type() != dstMat.type())
        {
            throw std::runtime_error("Source Mat size/type does not match");
        }        
        srcMat.copyTo(dstMat);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_CreateGpuMatHeader(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr hostMemRef,
    lvi::edvr::ReferencePtr gpuMatRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(hostMemRef);           

        if (obj->empty())
        {
            throw std::runtime_error("HostMem is empty.");
        }      

        EdvrObject<GpuMat> gpuMat(gpuMatRef, new GpuMat(obj->createGpuMatHeader()));

        return mgNoErr;
    });
}



#pragma endregion Data Transfer

#pragma region Pointer Access (for external DLLs)

_declspec(dllexport) void CV_CUDA_HOSTMEM_GetPointer(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    HostMem_PointerData* PointerData)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        if (obj->empty())
        {
            throw std::runtime_error("HostMem is empty, no pointer available.");
        }

        PointerData->dataPtr = reinterpret_cast<uintptr_t>(obj->data);
        PointerData->step = static_cast<int64_t>(obj->step);
        PointerData->rows = obj->rows;
        PointerData->cols = obj->cols;
        PointerData->elemSize = static_cast<int32_t>(obj->elemSize());
        PointerData->cvType = obj->type();
        PointerData->channels = obj->channels();
        PointerData->totalBytes = static_cast<uint64_t>(obj->step * obj->rows);

		//Increase reference count
        cv::cuda::HostMem* externalCopy = new cv::cuda::HostMem(*obj);
        PointerData->handlePtr = reinterpret_cast<uintptr_t>(externalCopy);
        PointerData->releaseCallbackPtr = reinterpret_cast<uintptr_t>(&CV_CUDA_HOSTMEM_ReleasePointerExternal);

        return mgNoErr;
    });
}

//Decrease the reference count
//Can be called by Labview or by the external DLL via the release callback function pointer provided in HostMem_PointerData

_declspec(dllexport) void CV_CUDA_HOSTMEM_ReleasePointer(lvi::error::ErrorClusterPtr errorCluster,
    void* handle)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        if (handle != nullptr)
        {
            cv::cuda::HostMem* mem = static_cast<cv::cuda::HostMem*>(handle);			
            delete mem;
        }

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_ReleasePointerExternal(void* handle)
{
    if (handle != nullptr)
    {
        cv::cuda::HostMem* mem = static_cast<cv::cuda::HostMem*>(handle);
        delete mem;
    }
}

#pragma endregion Pointer Access

#pragma region Info / Properties

_declspec(dllexport) void CV_CUDA_HOSTMEM_ReadInfo(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    HostMatInfo* info)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        info->rows = obj->rows;
        info->cols = obj->cols;
        info->cvType = obj->type();
        info->channels = obj->channels();
        info->depth = obj->depth();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_GetElemSize(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* elemSize)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        *elemSize  = static_cast<int64_t>(obj->elemSize());        

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_GetElemSize1(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* elemSize1)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        *elemSize1 = static_cast<int64_t>(obj->elemSize1());

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_GetStep(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* step1)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        *step1 = static_cast<int64_t>(obj->step);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_GetStep1(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* step1)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        *step1 = static_cast<int64_t>(obj->step1());

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_Empty(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        *result = obj->empty();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_HOSTMEM_IsContinuous(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<HostMem> obj(edvrRef);

        *result = obj->isContinuous();

        return mgNoErr;
    });
}

#pragma endregion Info / Properties

#endif // _WIN64
