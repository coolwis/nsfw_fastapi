from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi import UploadFile

from app.common.models.response_result import ResponseResult
from app.common.enums import ResponseCodeEnum
from app.file.models.upload_response import ret_file_info

# ai model predict
from app.nsfw_model.nsfw_detector import predict

from pathlib import Path
import hashlib
import os
import zipfile
from datetime import datetime
import subprocess
import sys

from dotenv import load_dotenv


# ENV 환경 변수에서 현재 환경을 가져옵니다. 기본값은 'dev'로 설정합니다.
ENV = os.getenv('ENV', 'dev')
# 로드할 .env 파일의 경로를 설정합니다.
dotenv_path = f'.env.{ENV}'
# 해당 .env 파일을 로드합니다.
load_dotenv(dotenv_path)


# Directory to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ai model predict
# .env.dev 에서 aws url 수정 필요!!

#fastApiServerPath ="/home/ubuntu/python_test/webapp/fastapi-fileserver/"
#ai_model_path ="app/nsfw_model/nsfw_mobilenet2.224x224.h5";
fastApiServerPath = os.getenv("FAST_API_SERVER_PATH")
ai_model_path = os.getenv("AI_MODEL_PATH")

def get_file_list():
    data = os.listdir(UPLOAD_DIR)
    result = ResponseResult(result_code=ResponseCodeEnum.SUCCESS, data=data, exclude_unset=True)
    return result


def upload_file(file: UploadFile):
#    hash_sha256 = hashlib.sha256(file.file.read()).hexdigest()

 #   file_location = Path(UPLOAD_DIR) / hash_sha256
    # ai model predict 
    currtime = datetime.today().strftime("%Y%m%d%H%M%S")
    file_location = str("uploads/") + str(currtime)+".jpg"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

#    data = ret_file_info(file, hash_sha256, file_location)

    # ai model predict
    img_preds_result= get_ai_result(file_location)
    print('img_preds_result>>', img_preds_result)
    #data.img_preds = img_preds_result
    data = {
        "file_name": file.filename,
       # "file_path": file_location,
        "file_size": file.size,
        "upload_type": file.content_type,
        "img_preds": img_preds_result,
    }

    result = ResponseResult(result_code=ResponseCodeEnum.SUCCESS, data=data)
    return result


# ai model predict
def get_ai_result(targetFile):
    modelPath = str(ai_model_path)
    model = predict.load_model(modelPath)
    testFile=fastApiServerPath + str(targetFile)
    print ("get_ai_result> targetFile", testFile)

    # Predict single image
    image_preds = predict.classify(model,testFile)   
    #image_preds = classify(model, config['image_source'], config['image_dim'])
    return image_preds


def download_file(file_hash):
    file_path = Path(UPLOAD_DIR) / file_hash
    if not file_path.exists():
        raise HTTPException(status_code=404)

    media_type = "application/octect-stream"
    return FileResponse(path=file_path, filename=file_hash, media_type=media_type)


def download_files_withzip(hash_list, zip_name, password):
    # zip name
    if zip_name is None:
        zip_name = datetime.now().strftime("%Y%m%d_%H%M%S_fastapi_downloaded")
    zip_name = zip_name + ".zip"
    zip_path = zip_name

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_hash in hash_list:
            file_path = Path(UPLOAD_DIR) / file_hash
            if not file_path.exists():
                raise HTTPException(status_code=404)

            find_file_path = os.path.join(UPLOAD_DIR, file_hash)
            f = open(find_file_path, "rb")
            data = f.read()
            f.close()

            with open(find_file_path, "wb") as f:
                f.write(data)
            zipf.write(find_file_path, arcname=file_hash)

    # ret download response
    media_type = "application/zip"
    return FileResponse(path=zip_path, filename=zip_name, media_type=media_type)
