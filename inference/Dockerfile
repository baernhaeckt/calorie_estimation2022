FROM python:3.9

WORKDIR /app/

COPY . /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#RUN curl --request GET -sL \
#--url "https://casmlguestdiag.blob.core.windows.net/weights/mask_rcnn_custom-food_0049.h5"\
#--output "weights/mask_rcnn_custom-food_0049.h5"

CMD ["./startup.sh"]
