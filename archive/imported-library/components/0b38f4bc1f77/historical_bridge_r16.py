"""R16 admission gate for historical ZIP packages and future native adapters.

No archeological file is synthesized, and no supplied ZIP becomes 'historical'
merely because of its filename. R06 canonical checksum is taken from IBX-17;
R07-R09 checksums must be recovered independently before admission.
"""
from __future__ import annotations
import hashlib,zipfile
from dataclasses import dataclass,asdict
from pathlib import Path

R06_EXPECTED='514edc0fa5337cd65e5ac432b030492077853eef88275de2ecc4f8ed57131021'
R10_EXPECTED='de3e4b0a76f6d0fd4e377709e5b7610755206a17e133db216545b58112d2a123'
R15_EXPECTED='d362839f3c200e83eec4fa377c87be4384d47a8fae6c74b00fade92cf7d1be38'

class IntegrationHOLD(ValueError):pass


def sha(path):
    with open(path,'rb') as f:
        h=hashlib.sha256()
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()


def inspect_archive(stage:str,path:str|Path|None,expected_hash:str|None):
    if not path or not Path(path).is_file():
        return {'stage':stage,'state':'NOT_RECOVERED_IN_SCOPED_SEARCH',
                'hash':None,'accepted_as_historical':False,
                'note':'No artifact bytes available; documentary references do not suffice.'}
    if not expected_hash:
        return {'stage':stage,'state':'PROVENANCE_HASH_PENDING',
                'hash':sha(path),'accepted_as_historical':False,
                'note':'Unverified claimant, never import merely by filename.'}
    actual=sha(path)
    if actual!=expected_hash:
        return {'stage':stage,'state':'HASH_MISMATCH',
                'hash':actual,'accepted_as_historical':False,'expected_hash':expected_hash}
    try:
        with zipfile.ZipFile(path,'r') as z:
            bad=z.testzip()
            if bad is not None:
                return {'stage':stage,'state':'CRC_FAIL','bad_entry':bad,
                        'hash':actual,'accepted_as_historical':False}
            members=z.namelist()
    except zipfile.BadZipFile:
        return {'stage':stage,'state':'ZIP_INVALID','hash':actual,
                'accepted_as_historical':False}
    return {'stage':stage,'state':'BYTE_HASH_AND_CRC_VERIFIED',
            'hash':actual,'member_count':len(members),
            'members':members,'accepted_as_historical':True,
            'note':'Not proof of runtime integration or writer access.'}


def interface_contract():
    return {'required':{
        'discover':'authoritative layout + block-tree fingerprint; read-only',
        'read_snapshot':'full normal+form+history+child pages, id+version, read-only',
        'save_preimage':'same-page terminal toggle for real authorized sheet; native readback',
        'stage_plan':'validate decisions and preview, no mutation',
        'commit_blocks':'must prove legitimate Notion writer, fencing and readback',
        'recover':'journal + before/after/UNKNOWN_EFFECT + version-aware compensation',
        'verify_media':'binary independent backing/hash proof or remain PENDING',
        'verify_tables':'semantic full rows/cells/order/column and approved serialization only',
        'verify_children':'complete closure, no orphan relations or image links'},
        'ownership':'CM-000005/IBX-17; coordinator support READ_ONLY',
        'native_writer':'DISABLED',
        'notion_atomicity':'NOT_DEMONSTRATED'}


def refuse_native_write(preflight:dict):
    mandatory=('authorized_instance','writer_exclusive','lease','epoch','fencing','save_full_readback',
               'child_pages_closed','media_backup_independent','before_fingerprint')
    missing=[k for k in mandatory if preflight.get(k) is not True]
    if missing:
        raise IntegrationHOLD('NATIVE_DENY: missing '+','.join(missing))
    # R16 package intentionally has NO native Notion write implementation.
    raise IntegrationHOLD('NATIVE_DENY: no Notion writer implementation; 0/2 remains')
