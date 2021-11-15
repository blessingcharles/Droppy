
from Logger.GeneralLogger import DroppyLogger
from env.Logconfig import CONFIG

func_logger = DroppyLogger(
    "func_logger" ,
    log_file=CONFIG["function_execution_logfile"] , 
    log_format="%(message)s" )

