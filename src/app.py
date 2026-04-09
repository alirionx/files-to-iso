import os
import uuid
import base64
from io import BytesIO
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from settings import settings
import tools
from models import (
    ApiStatus,
    TxtFile,
    TxtFileWithData,
    IsoFile,
    TxtFileAppend
)


#-Build and prep the App--------------------------------------------
tags_metadata = [
    {
        "name": "api-control",
        "description": "API status and testing",
    },
    {
        "name": "helpers",
        "description": "little helpers you may use to...",
    },
    {
        "name": "files",
        "description": "manage file objects",
    },
    {
        "name": "isos",
        "description": "manage iso objects",
    },
    {
        "name": "downloads",
        "description": "download iso and file objects",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

#-Custom Middleware Functions----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
) 

#-The Routes--------------------------------------------------------
@app.get("/api/status", tags=["api-control"], response_model=ApiStatus)
async def api_status_get(request:Request):
    item = ApiStatus(
        hostname=request.url.hostname,
        method=request.method,
        base_url=str(request.base_url),
        url_path=request.url.path,
        message="Hello from the 'Files to Iso Rest API'"
    )
    return item

#----------------------------------------------
@app.post("/api/helpers/base64-encode", tags=["helpers"], response_class=PlainTextResponse)
async def api_helpers_base64enc_post(text: str = Body(..., media_type="text/plain")):
    b64str = base64.b64encode(text.encode()).decode("utf-8")
    return b64str

@app.post("/api/helpers/base64-decode", tags=["helpers"], response_class=PlainTextResponse)
async def api_helpers_base64dec_post(b64: str = Body(..., media_type="text/plain")):
    try:
        text = base64.b64decode(b64).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return text

#----------------------------------------------
@app.get("/api/files", tags=["files"], response_model=list[TxtFileWithData])
async def api_files_get():
    try:
        items = tools.get_files()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return items

#--------
@app.get("/api/file/{id}", tags=["files"], response_model=TxtFileWithData)
async def api_file_get(id:uuid.UUID):
    try:
        items = tools.get_file_by_id(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return items

#--------
@app.post("/api/file", tags=["files"], response_model=TxtFileWithData)
async def api_file_post(item:TxtFileWithData):
    try:
        tools.insert_file(item=item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return item

#--------
@app.put("/api/file/{id}", tags=["files"], response_model=TxtFileWithData)
async def api_file_put(id:uuid.UUID, item:TxtFileWithData):
    try:
        tools.update_file(id=id, item=item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return item

#--------
@app.delete("/api/file/{id}", tags=["files"], response_model=uuid.UUID)
async def api_file_delete(id:uuid.UUID):
    try:
        tools.delete_file_by_id(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return id


#----------------------------------------------
@app.get("/api/isos", tags=["isos"], response_model=list[IsoFile])
async def api_isos_get():
    try:
        items = tools.get_isos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return items

#--------
@app.get("/api/iso/{id}", tags=["isos"], response_model=IsoFile)
async def api_iso_get(id:uuid.UUID):
    try:
        items = tools.get_iso_by_id(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return items

#--------
@app.post("/api/iso", tags=["isos"], response_model=IsoFile)
async def api_iso_post(item:IsoFile):
    try:
        tools.insert_iso(item=item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return item

#--------
@app.put("/api/iso/{id}", tags=["isos"], response_model=IsoFile)
async def api_iso_put(id:uuid.UUID, item:IsoFile):
    try:
        tools.update_iso(id=id, item=item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return item

#--------
@app.patch("/api/iso/{id}/add_file", tags=["isos"], response_model=TxtFileAppend)
async def api_iso_add_file_patch(id:uuid.UUID, tfappend:TxtFileAppend):
    try:
        tools.patch_iso_add_text_file(id=id, tfappend=tfappend)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return tfappend

#--------
@app.patch("/api/iso/{id}/del_file", tags=["isos"], response_model=TxtFileAppend)
async def api_iso_del_file_patch(id:uuid.UUID, tfappend:TxtFileAppend):
    try:
        tools.patch_iso_del_text_file(id=id, tfappend=tfappend)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return tfappend

#--------
@app.delete("/api/iso/{id}", tags=["isos"], response_model=uuid.UUID)
async def api_iso_delete(id:uuid.UUID):
    try:
        tools.delete_iso_by_id(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return id


#----------------------------------------------
@app.get("/api/download/file/{id}", tags=["downloads"])
async def download_file_get(id:uuid.UUID):
    try:
        item = tools.get_file_by_id(id=id)
        file_like = tools.generate_file_object(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return StreamingResponse(
        file_like,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{item.filename}"'
        }
    )

#--------
@app.get("/api/download/iso/{id}", tags=["downloads"])
async def download_iso_get(id:uuid.UUID):
    try:
        item = tools.get_iso_by_id(id=id)
        file_like = tools.generate_iso_object(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return StreamingResponse(
        file_like,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{item.name}.iso"'
        }
    )

#----------------------------------
if not os.path.isdir(settings.static_html_folder):
    os.makedirs(settings.static_html_folder)
app.mount("/", StaticFiles(directory="static", html=True), name="spa")


#----------------------------------------------



#-The Runner----------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        app="__main__:app", 
        host="0.0.0.0", 
        port=settings.app_port, 
        reload=settings.app_debug
    )