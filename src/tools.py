import os
import uuid
from io import BytesIO
import base64
from tinydb import TinyDB, Query
import pycdlib
from settings import settings
from models import (
    TxtFile,
    TxtFileWithData,
    IsoFile,
    TxtFileAppend
)

#-----------------------------------------------
db = TinyDB(settings.tinydb_path)
files = db.table("files")
File = Query()
isos = db.table("isos")
Iso = Query()

#-----------------------------------------------
def get_files() -> list[TxtFileWithData]:
    return [ TxtFileWithData(**item) for item in files ]

#----------
def get_file_by_id(id:uuid.UUID) -> TxtFileWithData:
    file = files.get(File.id == str(id))
    item = TxtFileWithData(**file)
    return item

#----------
def insert_file(item:TxtFileWithData):
    file = files.get(File.id == str(item.id))
    if file:
        raise Exception(f"File with id '{item.id}' already exsists.")
    if not item.filename:
        item.filename = item.name
    files.insert(document=item.model_dump(mode="json"))

def update_file(id:uuid.UUID, item:TxtFileWithData):
    file = files.get(File.id == str(id))
    if not file:
        raise Exception(f"File with id '{id}' does not exsists.")
    item.id = id
    files.update(fields=item.model_dump(mode="json"), cond=File.id == str(id))

#----------
def delete_file_by_id(id:uuid.UUID):
    file = files.get(File.id == str(id))
    if not file:
        raise Exception(f"File with id '{id}' does not exsists.")
    for iso in isos.all():
        item = IsoFile(**iso)
        if id in item.text_files:
            raise Exception(f"File with id '{id}' is appended to iso '{item.id}'.")
    files.remove(File.id == str(id))


#--------------------------
def get_isos() -> list[IsoFile]:
    return [ IsoFile(**item) for item in isos ]

#----------
def get_iso_by_id(id:uuid.UUID) -> IsoFile:
    iso = isos.get(Iso.id == str(id))
    item = IsoFile(**iso)
    return item

#----------
def insert_iso(item:IsoFile):
    iso = isos.get(Iso.id == str(item.id))
    if iso:
        raise Exception(f"Iso with id '{item.id}' already exsists.")
    if len(item.text_files):
        for tfappend in item.text_files:
            tf = files.get(File.id == str(tfappend.id))
            if not tf:
                raise Exception(f"file with id '{tfappend.id}' does not exsist.")
    isos.insert(document=item.model_dump(mode="json"))

#----------
def update_iso(id:uuid.UUID, item:IsoFile):
    iso = isos.get(Iso.id == str(id))
    if not iso:
        raise Exception(f"Iso with id '{id}' does not exsists.")
    if len(item.text_files):
        for tfid in item.text_files:
            tf = files.get(File.id == str(tfid.id))
            if not tf:
                raise Exception(f"file with id '{tfid}' does not exsist.")
    item.id = id
    isos.update(fields=item.model_dump(mode="json"), cond=Iso.id == str(id))

#----------
def patch_iso_add_text_file(id:uuid.UUID, tfappend:TxtFileAppend):
    iso = isos.get(Iso.id == str(id))
    if not iso:
        raise Exception(f"Iso with id '{id}' does not exsists.")
    tf = files.get(File.id == str(tfappend.id))
    if not tf:
        raise Exception(f"file with id '{tfappend.id}' does not exsist.")
    item = IsoFile(**iso)
    if tfappend in item.text_files:
         raise Exception(f"file with '{tfappend.model_dump()}' already added to iso.")
    item.text_files.append(tfappend)
    isos.update(fields=item.model_dump(mode="json"), cond=Iso.id == str(id))

#----------
def patch_iso_del_text_file(id:uuid.UUID, tfappend:TxtFileAppend):
    iso = isos.get(Iso.id == str(id))
    if not iso:
        raise Exception(f"Iso with id '{id}' does not exsists.")
    item = IsoFile(**iso)
    if tfappend not in item.text_files:
         raise Exception(f"file with id '{tfappend.model_dump()}' not in 'text_files' of iso.")
    item.text_files.remove(tfappend)
    isos.update(fields=item.model_dump(mode="json"), cond=Iso.id == str(id))

#----------
def delete_iso_by_id(id:uuid.UUID):
    iso = isos.get(Iso.id == str(id))
    if not iso:
        raise Exception(f"Iso with id '{id}' does not exsists.")
    isos.remove(Iso.id == str(id))


#--------------------------
def generate_file_object(id:uuid.UUID) -> BytesIO:
    file = files.get(File.id == str(id))
    if not file:
        raise Exception(f"Iso with id '{id}' does not exsists.")
    item = TxtFileWithData(**file)
    raw = base64.b64decode(item.data)
    bio = BytesIO(raw)
    return bio

#----------
# !!! BRUDAL !!!
def generate_iso_object(id:uuid.UUID) -> BytesIO:
    iso = isos.get(Iso.id == str(id))
    if not iso:
        raise Exception(f"Iso with id '{id}' does not exsists.")
    iso_item = IsoFile(**iso)
    iso = pycdlib.PyCdlib()
    iso.new(
        interchange_level=3, 
        joliet=True, 
        rock_ridge="1.12",
        vol_ident=iso_item.label)
    for text_file_append in iso_item.text_files:
        text_file_item = get_file_by_id(id=text_file_append.id)
        #-----
        parts = text_file_append.path.strip("/").split("/")
        cur = ""
        for p in parts:
            cur += "/" + p
            try:
                iso.get_record(joliet_path=cur)
            except pycdlib.pycdlibexception.PyCdlibInvalidInput:
                iso.add_directory(joliet_path=cur)
        #-----
        raw = base64.b64decode(text_file_item.data)
        fp = BytesIO(raw)
        jp = os.path.join(text_file_append.path, text_file_item.filename)
        iso.add_fp(fp=fp, joliet_path=jp, length=len(raw))
    buf = BytesIO()
    iso.write_fp(buf)
    iso.close()
    buf.seek(0)
    return buf
 
#----------


#----------


#-----------------------------------------------