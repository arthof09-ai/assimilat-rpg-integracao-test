"""Adaptador Windows estritamente local para fcntl.flock do motor POSIX R14/R17.

O motor legado continua byte-identico. No Windows, bloqueia 1 byte de arquivos
'.lock'/'cas.lock' usando msvcrt.locking; nenhum fallback sem exclusividade.
Este compat nao substitui writer, lease, fencing ou ACL do Notion.
"""
from __future__ import annotations
import os
import sys
import types


def install_windows_flock():
    if sys.platform != 'win32':
        return False
    import msvcrt
    if 'fcntl' in sys.modules:
        return True
    module = types.ModuleType('fcntl')
    module.LOCK_EX = 2
    module.LOCK_UN = 8
    module.LOCK_NB = 4

    def flock(fd, operation):
        if operation & module.LOCK_UN:
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            return None
        if not operation & module.LOCK_EX:
            raise OSError('LOCK_EX obrigatório para este fluxo experimental')
        # Todos os arquivos usados por R14/R17 são de bloqueio e ficam abertos
        # em a+b. Um byte sentinela evita bloqueio sobre arquivo de tamanho 0.
        if os.fstat(fd).st_size == 0:
            os.write(fd, b'\x00')
            os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        mode = msvcrt.LK_NBLCK if operation & module.LOCK_NB else msvcrt.LK_LOCK
        # LK_LOCK aguarda finitamente; quando falha, não prossegue sem lock.
        msvcrt.locking(fd, mode, 1)
        return None

    module.flock = flock
    sys.modules['fcntl'] = module
    return True
