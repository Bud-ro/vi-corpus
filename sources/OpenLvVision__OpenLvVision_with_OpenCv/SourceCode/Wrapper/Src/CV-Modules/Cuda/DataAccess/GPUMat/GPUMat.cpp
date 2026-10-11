#ifdef _WIN64

#include "GPUMat.h"

using namespace cv;
using namespace cv::cuda;
using namespace lvi;
using namespace lvi::mat;
using namespace lvi::error;
using namespace lvi::edvr;
using namespace lvi::array;

#pragma region Create / Destroy

_declspec(dllexport) void CV_CUDA_GPUMAT_CreateEmpty(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef, new GpuMat());

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_CreateSized(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int32_t rows, int32_t cols, 
    int32_t cvType,
    lvi::array::LV_1DArrayHandle<double_t> constantHandle)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        Array1D<double_t> constantArray(constantHandle);
        EdvrObject<GpuMat> obj(edvrRef, new GpuMat(rows, cols, cvType, constantArray.toScalar()));

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_CreateRoi(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    lvi::point::PointI32* size,
    lvi::point::PointI32* topLeft)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);

        cv::Rect roi(topLeft->x, topLeft->y, size->x, size->y);
        EdvrObject<GpuMat> obj(dstRef, new GpuMat(*src,roi));

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_ReCreate(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int32_t rows, int32_t cols,
    int32_t cvType)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);
		obj->create(rows, cols, cvType);

        return mgNoErr;
    });
}

#pragma endregion Create / Destroy

#pragma region Upload / Download HostMem

_declspec(dllexport) void CV_CUDA_GPUMAT_UploadFromHostMem(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr gpuMatRef,
    lvi::edvr::ReferencePtr hostMemRef,
    lvi::edvr::ReferencePtr streamRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat>  gpu(gpuMatRef);
        EdvrObject<HostMem> host(hostMemRef);

        Mat hostMat = host->createMatHeader();

        if (isRefNull(streamRef))
        {
            gpu->upload(hostMat);           
        }
        else
        {
            auto stream = resolveStream(streamRef);
            gpu->upload(hostMat, stream);
        }

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_DownloadToHostMem(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr gpuMatRef,
    lvi::edvr::ReferencePtr hostMemRef,
    lvi::edvr::ReferencePtr streamRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat>  gpu(gpuMatRef);
        EdvrObject<HostMem> host(hostMemRef);

        Mat hostMat = host->createMatHeader();

        if(hostMat.size() != gpu->size() || hostMat.type() != gpu->type())
        {
            throw std::runtime_error("HostMat and GpuMat must have the same size and type for download.");
        }

        if (isRefNull(streamRef))
        {
            gpu->download(hostMat);
        }
        else
        {
            auto stream = resolveStream(streamRef);
            gpu->download(hostMat, stream);
        }      

        return mgNoErr;
    });
}

#pragma endregion Upload / Download HostMem

#pragma region Upload / Download LV Buffer

_declspec(dllexport) void CV_CUDA_GPUMAT_UploadFromLvMat(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr gpuMatRef,
    void* addressSrc, lvi::mat::MatInfo* matInfoSrc)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> gpu(gpuMatRef);
        Mat srcMat = lvMatToCvMat(addressSrc, matInfoSrc);

        if (srcMat.empty())
        {
            throw std::runtime_error("Source Mat is empty, cannot upload.");
        }
        gpu->upload(srcMat);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_DownloadToLvMat(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr gpuMatRef,
    void* addressDst, lvi::mat::MatInfo* matInfoDst)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> gpu(gpuMatRef);
        Mat dstMat = lvMatToCvMat(addressDst, matInfoDst);

        if (gpu->empty())
        {
            throw std::runtime_error("GpuMat is empty, nothing to download.");
        }

        if (dstMat.size() != gpu->size() || dstMat.type() != gpu->type())
        {
            throw std::runtime_error("GpuMat must have the same size and type for download.");
        }

        gpu->download(dstMat);

        return mgNoErr;
    });
}

#pragma endregion Upload / Download LV Buffer

#pragma region Data Operations

_declspec(dllexport) void CV_CUDA_GPUMAT_SetTo(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    lvi::edvr::ReferencePtr MaskRef,    
    lvi::edvr::ReferencePtr streamRef,
    lvi::array::LV_1DArrayHandle<double_t> constantHandle)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);
        Array1D<double_t> constantArray(constantHandle);

        if (isRefNull(streamRef))
        {
            if (isRefNull(MaskRef))
            {
                obj->setTo(constantArray.toScalar());
            }
            else
            {
                EdvrObject<GpuMat> mask(MaskRef);
                obj->setTo(constantArray.toScalar(), *mask);
            }
        }
        else
        {
            auto stream = resolveStream(streamRef);

            if (isRefNull(MaskRef))
            {
                obj->setTo(constantArray.toScalar(), stream);
            }
            else
            {
                EdvrObject<GpuMat> mask(MaskRef);
                obj->setTo(constantArray.toScalar(), *mask, stream);
            }
        }

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_ConvertTo(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    int32_t rtype, double alpha, double beta,
    lvi::edvr::ReferencePtr streamRef)
{
    handleError(errorCluster, [&]() -> MgErr
        {
            EdvrObject<GpuMat> src(srcRef);
            EdvrObject<GpuMat> dst(dstRef);

        if (alpha == 1.0 && beta == 0.0)
        {
            if (isRefNull(streamRef))
            {
                src->convertTo(*dst, rtype);
            }
            else
            {
                auto stream = resolveStream(streamRef);
                src->convertTo(*dst, rtype, stream);
            }
        }
        else
        {
            if (isRefNull(streamRef))
            {
                src->convertTo(*dst, rtype, alpha, beta);
            }
            else
            {
                auto stream = resolveStream(streamRef);
                src->convertTo(*dst , rtype, alpha, beta, stream);
            }
        }

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_CopyTo(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    lvi::edvr::ReferencePtr streamRef,
    lvi::edvr::ReferencePtr maskRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);
        EdvrObject<GpuMat> dst(dstRef);
        
        if (isRefNull(streamRef))
        {
            if (isRefNull(maskRef))
            {
                src->copyTo(*dst);
            }
            else
            {
                EdvrObject<GpuMat> mask(maskRef);
                src->copyTo(*dst, *mask);
            }
        }
        else
        {
            auto stream = resolveStream(streamRef);

            if (isRefNull(maskRef))
            {
                src->copyTo(*dst, stream);
            }
            else
            {
                EdvrObject<GpuMat> mask(maskRef);
                src->copyTo(*dst, *mask, stream);
            }   
        }

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_Clone(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);
        EdvrObject<GpuMat> dst(dstRef, new GpuMat(src->clone()));

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_Reshape(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    int32_t cn, int32_t rows)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);
        EdvrObject<GpuMat> dst(dstRef, new GpuMat(src->reshape(cn, rows)));

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_Swap(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr refA,
    lvi::edvr::ReferencePtr refB)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> a(refA);
        EdvrObject<GpuMat> b(refB);

        a->swap(*b);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_Row(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    int32_t y)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);
        EdvrObject<GpuMat> dst(dstRef, new GpuMat(src->row(y)));
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_Col(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    int32_t x)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);
        EdvrObject<GpuMat> dst(dstRef, new GpuMat(src->col(x)));
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_RowRange(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    int32_t startrow, int32_t endrow)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);
        EdvrObject<GpuMat> dst(dstRef, new GpuMat(src->rowRange(startrow, endrow)));
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_ColRange(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr srcRef,
    lvi::edvr::ReferencePtr dstRef,
    int32_t startcol, int32_t endcol)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> src(srcRef);
        EdvrObject<GpuMat> dst(dstRef, new GpuMat(src->colRange(startcol, endcol)));
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_AdjustROI(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int32_t dtop, int32_t dbottom, int32_t dleft, int32_t dright)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);
        obj->adjustROI(dtop, dbottom, dleft, dright);
        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_LocateROI(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    lvi::point::PointI32* size,
    lvi::point::PointI32* topLeft)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);
        Size sz;
        Point pt;
        obj->locateROI(sz, pt);
        size->x = sz.width;
        size->y = sz.height;
        topLeft->x = pt.x;
        topLeft->y = pt.y;
        return mgNoErr;
    });
}

#pragma endregion Data Operations

#pragma region Pointer Access (for external DLLs)

_declspec(dllexport) void CV_CUDA_GPUMAT_GetPointer(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    GpuMat_PointerData* PointerData)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        if (obj->empty())
        {
            throw std::runtime_error("GpuMat is empty, no pointer available.");
        }

        PointerData->cudaPtr = reinterpret_cast<uintptr_t>(obj->cudaPtr());
        PointerData->step = static_cast<int64_t>(obj->step);
        PointerData->rows = obj->rows;
        PointerData->cols = obj->cols;
        PointerData->elemSize = static_cast<int32_t>(obj->elemSize());
        PointerData->cvType = obj->type();
        PointerData->channels = obj->channels();
        PointerData->totalBytes = static_cast<uint64_t>(obj->step * obj->rows);

		//Increase reference count
        cv::cuda::GpuMat* externalCopy = new cv::cuda::GpuMat(*obj);
        PointerData->handlePtr = reinterpret_cast<uintptr_t>(externalCopy);
        PointerData->releaseCallbackPtr = reinterpret_cast<uintptr_t>(&CV_CUDA_GPUMAT_ReleasePointerExternal);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_ReleasePointer(lvi::error::ErrorClusterPtr errorCluster,
    void* handle)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        if (handle != nullptr)
        {
            cv::cuda::GpuMat* mem = static_cast<cv::cuda::GpuMat*>(handle);			
            delete mem;
        }

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_ReleasePointerExternal(void* handle)
{
    if (handle != nullptr)
    {
        cv::cuda::GpuMat* mem = static_cast<cv::cuda::GpuMat*>(handle);
        delete mem;
    }
}

#pragma endregion Pointer Access

#pragma region Info / Properties

_declspec(dllexport) void CV_CUDA_GPUMAT_ReadInfo(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    GpuMatInfo* info)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        info->rows     = obj->rows;
        info->cols     = obj->cols;
        info->cvType   = obj->type();
        info->channels = obj->channels();
        info->depth    = obj->depth();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_Empty(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        *result = obj->empty();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_IsContinuous(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        *result = obj->isContinuous();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_GetElemSize(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* elemSize)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        *elemSize = static_cast<int64_t>(obj->elemSize());

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_GetElemSize1(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* elemSize1)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        *elemSize1 = static_cast<int64_t>(obj->elemSize1());

        return mgNoErr;
    });
}


_declspec(dllexport) void CV_CUDA_GPUMAT_GetStep(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* step)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        *step = static_cast<int64_t>(obj->step);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_GPUMAT_GetStep1(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int64_t* step1)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<GpuMat> obj(edvrRef);

        *step1 = static_cast<int64_t>(obj->step1());

        return mgNoErr;
    });
}

#pragma endregion Info / Properties

#endif // _WIN64
