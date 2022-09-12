import os
import shutil
import sys
import time

from loguru import logger

from ssrspeed.config import ssrconfig
from ssrspeed.core import SSRSpeedCore
from ssrspeed.paths import KEY_PATH, ROOT_PATH
from ssrspeed.shell import cli as cli_cfg
from ssrspeed.utils import RequirementsCheck, check_platform

LOGS_DIR = KEY_PATH["logs"]
RESULTS_DIR = KEY_PATH["results"]

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)
if not os.path.exists(RESULTS_DIR):
    os.mkdir(RESULTS_DIR)

LOG_FILE = f"{LOGS_DIR}{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}.log"
handlers = [
    {
        "sink": sys.stdout,
        "level": "INFO",
        "format": "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>][<level>{level}</level>]"
        "[<yellow>{file}</yellow>:<cyan>{line}</cyan>]: <level>{message}</level>",
        "colorize": True,  # 自定义配色
        "serialize": False,  # 以 JSON 数据格式打印
        "backtrace": True,  # 是否显示完整的异常堆栈跟踪
        "diagnose": True,  # 异常跟踪是否显示触发异常的方法或语句所使用的变量，生产环境应设为 False
        "enqueue": True,  # 默认线程安全。若想实现协程安全 或 进程安全，该参数设为 True
        "catch": True,  # 捕获异常
    },
    {
        "sink": LOG_FILE,
        "level": "INFO",
        "format": "[{time:YYYY-MM-DD HH:mm:ss.SSS}][{level}][{file}:{line}]: {message}",
        "serialize": False,
        "backtrace": True,
        "diagnose": True,
        "enqueue": True,
        "catch": True,
    },
]

VERSION = ssrconfig["VERSION"]

if __name__ == "__main__":
    pf = check_platform()
    if pf == "Unknown":
        logger.critical("Your system is not supported. Please contact the developer.")
        sys.exit(1)

    CONFIG_LOAD_MODE = 0  # 0 for import result, 1 for guiconfig, 2 for subscription url
    CONFIG_FILENAME = ""
    CONFIG_URL = ""
    IMPORT_FILENAME = ""
    FILTER_KEYWORD = []
    FILTER_GROUP_KEYWORD = []
    FILTER_REMARK_KEYWORD = []
    EXCLUDE_KEYWORD = []
    EXCLUDE_GROUP_KEYWORD = []
    EXCLUDE_REMARK_KEYWORD = []
    TEST_METHOD = ""
    TEST_MODE = ""
    # PROXY_TYPE = "SSR"
    # SPLIT_CNT = 0
    SORT_METHOD = ""
    SKIP_CONFIRMATION = True
    RESULT_IMAGE_COLOR = "origin"

    args = cli_cfg.init(VERSION)

    if args.paolu:
        shutil.rmtree(ROOT_PATH)
        sys.exit(0)

    # print("********* Important Tip 重要提示 *********")
    # print("ChenBilly yyds!")
    # print("******************************************")
    # input("Press ENTER to continue or Ctrl+C to exit.")

    if args.debug:
        for each in handlers:
            each.update({"level": "DEBUG"})
        logger.debug("Program running in debug mode.")
        logger.configure(handlers=handlers)
    else:
        logger.configure(handlers=handlers)
    logger.enable("__main__")

    logger.info(
        f'SSRSpeed {ssrconfig["VERSION"]}, Web Api Version {ssrconfig["WEB_API_VERSION"]}'
    )

    if not args.skip_requirements_check:
        rc = RequirementsCheck()
        rc.check()
    else:
        logger.warning("Requirements check skipped.")

    """
    if args.proxy_type:
        if args.proxy_type.lower() == "ss":
            PROXY_TYPE = "SS"
        elif args.proxy_type.lower() == "ssr":
            PROXY_TYPE = "SSR"
        elif args.proxy_type.lower() == "ssr-cs":
            PROXY_TYPE = "SSR-C#"
        elif args.proxy_type.lower() == "v2ray":
            PROXY_TYPE = "V2RAY"
        else:
            logger.warning(
                f"Unknown proxy type {args.proxy_type}, using default ssr."
            )
    """

    # print(args.test_method)
    if args.test_method == "speedtestnet":
        TEST_METHOD = "SPEED_TEST_NET"
    elif args.test_method == "fast":
        TEST_METHOD = "FAST"
    elif args.test_method == "stasync":
        TEST_METHOD = "ST_ASYNC"
    elif args.test_method == "socket":
        TEST_METHOD = "SOCKET"
    else:
        TEST_METHOD = "ST_ASYNC"

    if args.test_mode == "default":
        TEST_MODE = "DEFAULT"
    elif args.test_mode == "pingonly":
        TEST_MODE = "TCP_PING"
    elif args.test_mode == "stream":
        TEST_MODE = "STREAM"
    elif args.test_mode == "all":
        TEST_MODE = "ALL"
    elif args.test_mode == "wps":
        TEST_MODE = "WEB_PAGE_SIMULATION"
    else:
        logger.critical(f"Invalid test mode : {args.test_mode}")
        sys.exit(1)

    if args.confirmation:
        SKIP_CONFIRMATION = args.confirmation

    if args.result_color:
        RESULT_IMAGE_COLOR = args.result_color

    if args.import_file:
        CONFIG_LOAD_MODE = 0
    elif args.guiConfig:
        CONFIG_LOAD_MODE = 1
        CONFIG_FILENAME = args.guiConfig
    elif args.url:
        CONFIG_LOAD_MODE = 2
        CONFIG_URL = args.url
    else:
        logger.error("No config input, exiting...")
        sys.exit(1)

    if args.filter:
        FILTER_KEYWORD = args.filter
    if args.group:
        FILTER_GROUP_KEYWORD = args.group
    if args.remarks:
        FILTER_REMARK_KEYWORD = args.remarks

    if args.efliter:
        EXCLUDE_KEYWORD = args.efliter
    # 	print (EXCLUDE_KEYWORD)
    if args.egfilter:
        EXCLUDE_GROUP_KEYWORD = args.egfilter
    if args.erfilter:
        EXCLUDE_REMARK_KEYWORD = args.erfilter

    logger.debug(
        f"\nFilter keyword : {FILTER_KEYWORD}"
        f"\nFilter group : {FILTER_GROUP_KEYWORD}"
        f"\nFilter remark : {FILTER_REMARK_KEYWORD}"
        f"\nExclude keyword : {EXCLUDE_KEYWORD}"
        f"\nExclude group : {EXCLUDE_GROUP_KEYWORD}"
        f"\nExclude remark : {EXCLUDE_REMARK_KEYWORD} "
    )

    """
    if int(args.split_count > 0):
        SPLIT_CNT = int(args.split_count)
    """

    if args.sort_method:
        sm = args.sort_method
        # 	print(sm)
        if sm == "speed":
            SORT_METHOD = "SPEED"
        elif sm == "rspeed":
            SORT_METHOD = "REVERSE_SPEED"
        elif sm == "ping":
            SORT_METHOD = "PING"
        elif sm == "rping":
            SORT_METHOD = "REVERSE_PING"
        else:
            logger.error(f"Sort method {sm} not support.")

    sc = SSRSpeedCore()

    if args.import_file and CONFIG_LOAD_MODE == 0:
        IMPORT_FILENAME = args.import_file
        sc.colors = RESULT_IMAGE_COLOR
        sc.sort_method = SORT_METHOD if SORT_METHOD else ""
        sc.import_and_export(IMPORT_FILENAME)
        sys.exit(0)

    configs: list = []
    if CONFIG_LOAD_MODE == 1:
        sc.console_setup(
            TEST_MODE,
            TEST_METHOD,
            RESULT_IMAGE_COLOR,
            SORT_METHOD,
            cfg_filename=CONFIG_FILENAME,
        )
    # 	sc.console_read_file_configs(CONFIG_FILENAME)
    else:
        sc.console_setup(
            TEST_MODE, TEST_METHOD, RESULT_IMAGE_COLOR, SORT_METHOD, url=CONFIG_URL
        )
    # 	sc.console_read_subscription(CONFIG_URL)

    if args.group_override:
        sc.set_group(args.group_override)

    sc.filter_nodes(
        FILTER_KEYWORD,
        FILTER_GROUP_KEYWORD,
        FILTER_REMARK_KEYWORD,
        EXCLUDE_KEYWORD,
        EXCLUDE_GROUP_KEYWORD,
        EXCLUDE_REMARK_KEYWORD,
    )
    sc.clean_result()

    if not SKIP_CONFIRMATION:
        ans = input("Before the test please confirm the nodes, Ctrl-C to exit. (Y/N)")
        if ans.upper() == "Y":
            pass
        else:
            sys.exit(0)

    sc.start_test(args)
