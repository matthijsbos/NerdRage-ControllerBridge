FROM matthijsbos/nerdrage-base
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./nerdrage_controller_bridge .
CMD ["python3", "./NerdRageControllerBridge.py"]
