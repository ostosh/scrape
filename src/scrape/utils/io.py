import io


class BufferedReader:
    def __init__(self):
        self.sio = io.BytesIO()
        self.cur_size = 0

    def buffer_data(self, data):
        self.cur_size += len(data)
        self.sio.write(data)

    def save_file(self, callback):
        self.sio.seek(0)
        callback(self.sio)
        self.sio.close()

    def get_buffered_size(self):
        return self.cur_size
