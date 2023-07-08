import subprocess


class GitItem:
    def __init__(self,conf: dict[str],*args):

        self.__n_args=len(args)
        self.__state = subprocess.getoutput(conf[args[0]])

        if self.__n_args ==1:
            self.__id = self.__state
        else:
            """
                cmd: str, args[0]
                success: str, args[1]
                failure: str, args[2]
                token_b: str = "tb", args[3]
                token_e: str = "te", args[4]
            """
            self.__succes_msg = conf[args[1]].format(self.__state)
            self.__failure_msg = conf[args[2]].format(self.__state)
            self.__tb = conf["tb"]
            self.__te = conf["te"]
            self.__id = ""

    def state_msg(self) -> (str, bool):
        if self.__n_args != 1:
            if self.__msg_checker(self.__state):
                return self.__succes_msg, True
            return self.__failure_msg, False
        return self.__id,True

    def __msg_checker(self, msg: str) -> bool:
        if msg[0] == "E" and msg[1] == "M":
            pos_begin = msg.find(self.__tb)
            pos_end = msg.rfind(self.__te)
            self.__id = msg[pos_begin + 1 : pos_end]
            if self.__id.isalnum():
                return True
        return False

    def get_output(self) -> str:
        return self.__state

    def get_id(self) -> str:
        return self.__id
