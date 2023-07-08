import sys
import os
import logging
import logging.handlers

from lnp.utils.notifier import Notifier
from lnp.utils.gitmgr import GitMgr
from lnp.core.file_handler import FileHandler as fl

# todo wrap this in a json file
CHAN = "#photon-repo"
BOT = "PTBOT"
GIT_ARTIFACTS_CONF = "conf/gititem.json"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

#todo allows to pass x args
def execute_predicat(_handler,_arg):
    if not _handler(_arg):
        sys.exit(1)

#todo allows to pass x args
def execute_predicat_with_cond(_cond,_handler,_arg):
    if _cond:
        _handler(_arg)
        sys.exit(1)

if __name__ == "__main__":
    l_notifier = Notifier(CHAN, BOT, os.environ["STK"])
    l_git_mgr = GitMgr(GIT_ARTIFACTS_CONF)
   
    execute_predicat(l_notifier.send_msg,l_git_mgr.current_branch())
    execute_predicat(l_notifier.send_msg,l_git_mgr.commit_msg())

    l_branch = l_git_mgr.current_branch()
    l_commit = l_git_mgr.commit_msg()
    l_author = l_git_mgr.author()

    execute_predicat_with_cond(l_branch.get_id() != l_commit.get_id(),
                               l_notifier.send_raw_msg,
                               "the branch {} & \n the commit {} \n do not point to the same JIRA ticket".format(
                               l_branch.get_output(), l_commit.get_output())
    )

    l_notifier.send_raw_msg("\n {} has been pushed {} succesfully".format(l_author.get_output(),l_branch.get_output()))
