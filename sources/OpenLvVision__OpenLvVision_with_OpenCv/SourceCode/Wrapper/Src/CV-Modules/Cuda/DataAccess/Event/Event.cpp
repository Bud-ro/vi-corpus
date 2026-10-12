#ifdef _WIN64

#include "Event.h"
#include "../Stream/Stream.h"

using namespace cv;
using namespace cv::cuda;
using namespace lvi;
using namespace lvi::error;
using namespace lvi::edvr;

#pragma region Create / Destroy

_declspec(dllexport) void CV_CUDA_EVENT_Create(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    int32_t createFlags)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Event> obj(edvrRef, new Event(static_cast<Event::CreateFlags>(createFlags)));

        return mgNoErr;
    });
}

#pragma endregion Create / Destroy

#pragma region Record / Synchronize

_declspec(dllexport) void CV_CUDA_EVENT_Record(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr eventRef,
    lvi::edvr::ReferencePtr streamRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Event> eventObj(eventRef);

        auto stream = resolveStream(streamRef);
        eventObj->record(stream);

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_EVENT_WaitForCompletion(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Event> obj(edvrRef);

        obj->waitForCompletion();

        return mgNoErr;
    });
}

_declspec(dllexport) void CV_CUDA_EVENT_QueryIfComplete(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr edvrRef,
    LVBoolean* result)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Event> obj(edvrRef);

        *result = obj->queryIfComplete();

        return mgNoErr;
    });
}

#pragma endregion Record / Synchronize

#pragma region Timing

_declspec(dllexport) void CV_CUDA_EVENT_ElapsedTime(lvi::error::ErrorClusterPtr errorCluster,
    lvi::edvr::ReferencePtr startRef,
    lvi::edvr::ReferencePtr endRef,
    float* elapsedMs)
{
    handleError(errorCluster, [&]() -> MgErr
    {
        EdvrObject<Event> startObj(startRef);
        EdvrObject<Event> endObj(endRef);

        *elapsedMs = Event::elapsedTime(*startObj, *endObj);

        return mgNoErr;
    });
}

#pragma endregion Timing

#endif
