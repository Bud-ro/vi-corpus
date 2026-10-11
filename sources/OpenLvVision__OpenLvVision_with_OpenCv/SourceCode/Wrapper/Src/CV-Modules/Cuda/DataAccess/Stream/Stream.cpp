#ifdef _WIN64

#include "Stream.h"

using namespace cv;
using namespace cv::cuda;
using namespace lvi;
using namespace lvi::error;
using namespace lvi::edvr;

cv::cuda::Stream resolveStream(lvi::edvr::ReferencePtr streamRef)
{
    if (isRefNull(streamRef))
    {
        return cv::cuda::Stream::Null();
    }
    else
    {
        EdvrObject<cv::cuda::Stream> obj(streamRef);
        return *obj;
    }
}

#pragma region Create / Destroy

_declspec(dllexport) void CV_CUDA_STREAM_Create(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Stream> obj(edvrRef, new Stream());

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_STREAM_CreateWithFlags(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int32_t cudaFlags)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Stream> obj(edvrRef, new Stream(cudaFlags));

        return mgNoErr;
    });
}

#pragma endregion Create / Destroy

#pragma region Synchronization

_declspec(dllexport) void CV_CUDA_STREAM_WaitForCompletion(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Stream> obj(edvrRef);

        obj->waitForCompletion();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_STREAM_QueryIfComplete(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Stream> obj(edvrRef);

        *result = obj->queryIfComplete();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_STREAM_WaitEvent(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr streamRef,
    lvi::edvr::ReferencePtr eventRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Event> eventObj(eventRef);

        resolveStream(streamRef).waitEvent(*eventObj);

        return mgNoErr;
    });
}

#pragma endregion Synchronization

#pragma region Info

_declspec(dllexport) void CV_CUDA_STREAM_IsNonDefault(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Stream> obj(edvrRef);

        *result = static_cast<bool>(*obj);

        return mgNoErr;
    });
}

#pragma endregion Info

#endif
