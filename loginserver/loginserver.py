import sys
_path = ('..')
if _path not in sys.path:
    sys.path.append(_path)
from base import PbService
from twisted.python import log
import login_pb2

class LoginService(PbService):
			
    def loginrequest(self, p, request):
        user_name = request.user_name
        log.msg("loginrequest", user_name)

        _msg = login_pb2.LoginResponse()
        _result = '0' if user_name else '1'	
        _msg.result = _result
        _msg.user_name = user_name					
        p.send(_msg)