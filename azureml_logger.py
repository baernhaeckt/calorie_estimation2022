from tensorflow.keras.callbacks import Callback


class AzureMlLogger(Callback):
    def __init__(self, run):
        super().__init__()
        self.run = run

    def on_epoch_end(self, epoch, logs=None):
        for key, value in logs.items():
            self.run.log(key, value)
