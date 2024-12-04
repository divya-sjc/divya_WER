FROM asia.gcr.io/slangserver/server-base:1.2
# ARG SERVICE_PATH=/src/app
# ENV CODE_PATH=${SERVICE_PATH}
ARG SLANG_ROOT=/polyglot
ENV SLANG_ROOT=${SLANG_ROOT}

ENV GCSFUSE_FLAGS=,key_file=${GOOGLE_APPLICATION_CREDENTIALS}
ENV SLANG_ENV=local
# ENV STORAGE_BUCKET=slang-stage-storage

COPY /tools/data_updation/requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./configs/stage/ ${SLANG_ROOT}/configs/stage
COPY ./tools/data_updation ${SLANG_ROOT}/tools/data_updation
RUN chmod a+x ${SLANG_ROOT}/tools/data_updation/start.sh
WORKDIR ${SLANG_ROOT}
EXPOSE 8501

ENTRYPOINT [ "/bin/bash", "-c" ]
CMD ["${SLANG_ROOT}/tools/data_updation/start.sh"]