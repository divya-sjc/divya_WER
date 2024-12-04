#!/bin/bash
if [[ ${SLANG_ENV} == "local" ]]
then
    streamlit run ${SLANG_ROOT}/tools/data_updation/server.py -- --env ${SLANG_ENV}
else
    mount -t gcsfuse -o rw,dir_mode=666,file_mode=666,allow_other${GCSFUSE_FLAGS} ${STORAGE_BUCKET} /slang-remote
    streamlit run ${SLANG_ROOT}/tools/data_updation/server.py -- --env ${SLANG_ENV}
fi