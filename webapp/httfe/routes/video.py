from typing import Annotated
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from httfe.services.camera import CameraService, get_cam_srv
from httfe.services.text import TextService, get_text_srv
from httfe.schemas.camera import CameraResponse

router = APIRouter()


@router.get("/feed")
async def video_feed(
    camera_service: Annotated[CameraService, Depends(get_cam_srv)],
    text_service: Annotated[TextService, Depends(get_text_srv)],
):
    return StreamingResponse(
        camera_service.generate_frames(text_service),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.put("/camera", response_model=CameraResponse)
async def manage_camera(
    camera_service: Annotated[CameraService, Depends(get_cam_srv)],
    action: str = Query(..., enum=["start", "stop"]),
):
    if action == "start":
        if camera_service.start_camera():
            return CameraResponse(status="success")
        return CameraResponse(status="error", message="Cannot open camera")
    if action == "stop":
        camera_service.stop_camera()
        return CameraResponse(status="success")
