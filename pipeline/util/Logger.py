class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ChatLogger:
    def __init__(self):
        self.logs = []
        self.error = []

    def info(self, log):
        self.logs.append(log)
        print(log)
    
    def error(self, error_log):
        self.logs.append(error_log)
        print(f"{bcolors.FAIL} error_log {bcolors.ENDC}")

