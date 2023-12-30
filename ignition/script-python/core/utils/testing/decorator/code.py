class DecoratedValue:
    def __init__(self, dec, value, exc=None):
        self.dec = dec
        self.value = value
        self.exc = exc
    
    def is_exc(self):
        return self.exc is not None
    
    def __str__(self):
        if self.is_exc():
            return 'Operation returned exception:\n%s' % (self.exc)
        else:
            return 'Operation returned %s.\nDecorated value: %s' % (self.value, self.dec)
    
    def __repr__(self):
        if self.is_exc():
            return 'Operation returned exception:\n%s' % (self.exc)
        else:
            return 'Operation returned %s.\nDecorated value: %s' % (self.value, self.dec)


def timed(f):
    def wrapper(*args, **kwargs):
        start = system.date.now()
        try:
            ret = f(*args, **kwargs)
            exc = None
        except:
            import traceback
            ret = None
            exc = traceback.format_exc()
            
        end = system.date.now()
        millis = system.date.millisBetween(start, end)
        return DecoratedValue(millis, ret, exc)
    
    return wrapper


def avg_exec_time(f):
	def wrapper(*args, **kwargs):
		returns = []
		deltas = []
        for i in range(0, 10):
        	start = system.date.now()
        	try:
	    		returns.append(f(*args, **kwargs))
	        	exc = None
       		except:
	        	import traceback
	        	returns.append(None)
	        	exc = traceback.format_exc()
	        end = system.date.now()
	        deltas.append(system.date.millisBetween(start, end))
		millis = system.math.mean(deltas)
		return DecoratedValue(millis, returns, exc)

	return wrapper


def logged(f):
    def wrapper(*args, **kwargs):
        frwk.framework.log.info('framework', 'Calling function %s with args: %s; kwargs: %s' % (f.func_name, str(args), str(kwargs)))
        try:
            ret = f(*args, **kwargs)
            frwk.framework.log.info('framework', 'Function %s executed with return value %s' % (f.func_name, str(ret)))
            exc = None
        except:
            import traceback
            ret = None
            exc = traceback.format_exc()
            frwk.framework.log.error('framework', 'Function %s executed with errors: %s' % (f.func_name, exc))
        
        # Use this if you want to use the actual return value of the function
        return ret
        # Use this if you want to use the decoreted value
        # return frwk.framework.classes.DecoratedValue(None, ret, exc)
    
    return wrapper


def audited(f):
    def wrapper(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            exc = None
            session = frwk.framework.perspective.get_current_session_info()
            if session is not None:
                action = f.func_name
                actor = session['username']
                host = session['clientAddress']
                value = str(ret)
                target = str({'args': args, 'kwargs': kwargs})
                frwk.framework.audit.add_audit(action, target, value=value, actor=actor, host=host)
        except:
            import traceback
            ret = None
            exc = traceback.format_exc()
            frwk.framework.log.error('framework', 'Function %s with args %s executed with errors: %s' % (f.func_name, str(kwargs), exc))
        
        # Use this if you want to use the actual return value of the function
        return ret
        # Use this if you want to use the decoreted value
        # return frwk.framework.classes.DecoratedValue(None, ret, exc)
    
    return wrapper