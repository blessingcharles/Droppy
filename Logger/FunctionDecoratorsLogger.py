import time
from functools import wraps
from . import func_logger

def function_logger(decorated_func : function):

    @wraps(decorated_func)
    def wrapper(*args , **kwargs):
    
        func_logger.logger.log(f"function name : {decorated_func.__name__} with args {args} {kwargs} ")
        return decorated_func(*args,**kwargs)
    
    return wrapper

def executed_time(decorated_func : function):
    
    @wraps(decorated_func)
    def wrapper(*args , **kwargs):
    
        started_time = time.time()
        results = decorated_func(*args,**kwargs)
        end_time = time.time()
        execution_time = end_time - started_time 

        #logs it to function log file
        func_logger.logger.log(f"function : {decorated_func.__name__} execution time : {execution_time}")
        return results 
    
    return wrapper