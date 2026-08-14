"""全局崩溃日志。

为什么需要它：
- 主线程未捕获异常默认只进 stderr，双击启动（Windows/macOS 打包）时 stderr 被丢弃，用户看不到任何信息。
- Qt 事件循环里抛出的异常（例如点在槽函数里触发的“添加物品/添加帕鲁”崩溃）默认被 Qt 吞掉，
  既不进 sys.excepthook 也不进 stderr 可见文件，导致“崩溃了但毫无痕迹”。
- 本模块提供统一落盘：把完整 traceback（或 Qt 报错）写入 <data>/Logs/Crash/crash_<时间戳>.log，
  同时打印到 stderr，便于事后定位。
"""
import os
import sys
import traceback
import datetime

_LOG_DIR = None


def get_crash_dir():
    """返回崩溃日志目录（不存在则创建）。失败时回退到用户家目录。"""
    global _LOG_DIR
    if _LOG_DIR is not None:
        return _LOG_DIR
    try:
        from resource_resolver import get_data_base
        base = get_data_base()
    except Exception:
        base = os.path.expanduser('~')
    d = os.path.join(base, 'Logs', 'Crash')
    try:
        os.makedirs(d, exist_ok=True)
    except Exception:
        d = None
    _LOG_DIR = d
    return d


def write_crash_report(title, detail, context=''):
    """写一份崩溃报告到文件，并返回文件路径（失败返回 None）。同时打印到 stderr。"""
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    lines = [
        'PalworldSaveTools Crash Report',
        f'Time: {datetime.datetime.now().isoformat(timespec="seconds")}',
        f'Platform: {sys.platform}  Frozen: {getattr(sys, "frozen", False)}  Python: {sys.version.split()[0]}',
    ]
    if context:
        lines.append(f'Context: {context}')
    lines.append('=' * 60)
    lines.append(title)
    lines.append('-' * 60)
    lines.append(detail)
    text = '\n'.join(lines)

    try:
        sys.stderr.write(text + '\n')
    except Exception:
        pass

    d = get_crash_dir()
    if not d:
        return None
    path = os.path.join(d, f'crash_{ts}.log')
    n = 0
    while os.path.exists(path):
        n += 1
        path = os.path.join(d, f'crash_{ts}_{n}.log')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text + '\n')
        return path
    except Exception:
        return None


def report_exception(exc_type, exc_value, exc_tb, context=''):
    """由 sys.excepthook / notify 调用：把一个异常写成崩溃报告。"""
    if exc_tb:
        detail = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    else:
        detail = f'{exc_type}: {exc_value}'
    title = f'Uncaught exception: {getattr(exc_type, "__name__", exc_type)}: {exc_value}'
    return write_crash_report(title, detail, context=context)


class _QtMessage(Exception):
    pass


def _qt_message_handler(mode, context, message):
    """接管 Qt 消息处理器：过滤已知无害噪音，其余（警告/严重/致命）落盘。"""
    s = str(message)
    # 已知无害噪音：线程存储销毁、macOS IME 端口
    if 'QThreadStorage' in s and 'destroyed before end of thread' in s:
        return
    if 'TSMSendMessageToUIServer' in s or 'CFMessagePortSendRequest' in s:
        return
    try:
        from PySide6.QtCore import QtMsgType
    except Exception:
        QtMsgType = None
    severity = 'INFO'
    if QtMsgType is not None:
        mapping = {
            QtMsgType.QtDebugMsg: 'DEBUG',
            QtMsgType.QtInfoMsg: 'INFO',
            QtMsgType.QtWarningMsg: 'WARN',
            QtMsgType.QtCriticalMsg: 'CRIT',
            QtMsgType.QtFatalMsg: 'FATAL',
            QtMsgType.QtSystemMsg: 'SYS',
        }
        try:
            severity = mapping.get(mode, 'INFO')
        except Exception:
            severity = 'INFO'
    if severity in ('WARN', 'CRIT', 'FATAL', 'SYS'):
        ctx = ''
        try:
            ctx = f'{context.file}:{context.line}'
        except Exception:
            pass
        report_exception(_QtMessage, _QtMessage(f'[{severity}] {message}'), None,
                         context=f'Qt:{severity}:{ctx}')


def install_crash_reporting():
    """安装全局崩溃捕获：sys.excepthook + Qt 消息处理器。在创建 QApplication 前调用。"""
    sys.excepthook = lambda et, ev, tb: report_exception(et, ev, tb, context='sys.excepthook')
    try:
        from PySide6.QtCore import qInstallMessageHandler
        qInstallMessageHandler(_qt_message_handler)
    except Exception:
        pass

