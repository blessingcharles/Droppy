import logging

class DroppyLogger:
    def __init__(self , 
                logger_name : str , 
                log_file : str , 
                log_format : str = "[%(levelname)s] %(asctime)s : %(message)s" ,
                log_level = logging.INFO 
                ) -> None:
        self.logger = logging.getLogger(logger_name)

        formatter = logging.Formatter(log_format)
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        self.logger.setLevel(log_level)
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)    
