from datetime import datetime

ignore_starts = ["[download]", "[debug]", "[youtube]"]

class Logger:
    def __init__(self, log_file="dl_videos.logs") -> None:
        self.logfile = open(log_file, 'a')

    def debug(self, msg):
        if any([msg.startswith(x) for x in ignore_starts]):
            pass
        else:
            self.info(msg)
            

    def info(self, msg):
        pass

    def warning(self, msg):
        self.logfile.write(datetime.now().strftime("%H:%M:%S") + msg + '\n')

    def error(self, msg):
        self.logfile.write(datetime.now().strftime("%H:%M:%S") + msg + '\n')

