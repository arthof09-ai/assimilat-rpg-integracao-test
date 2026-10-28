"""Pure offline write-set sketch from a preverified TESTE excerpt. Zero remote mutation.

A real adapter must use native block IDs/versioned tree, images & children before
it can issue edits. This preparation is deliberately non-executable in Notion.
"""
from __future__ import annotations
import copy,re
from adapters_r15_preflight import read_fixture,AdapterBlocker

class NativeHold(AdapterBlocker):pass


def make_readonly_sketch(title:str,markdown:str,*,expected_current=None,new_maxima=None):
    scan=read_fixture(title,markdown)
    if not scan['resource_compatible'] or not scan['attribute_compatible']:
        raise NativeHold('source/save baseline differs')
    if not expected_current or not new_maxima:
        raise NativeHold('explicit expected current and maxima required')
    actions=[]
    for key in ('Vida','Alma'):
        b=scan['active']['resources'][key]
        if expected_current.get(key)!=b['current']:
            raise NativeHold('requested current value differs from readback')
        v=new_maxima.get(key)
        if type(v) is not int or v<b['current']:
            raise NativeHold('invalid new maximum, cannot heal or shrink below current')
        actions.append({'field':key,'expected_before':copy.deepcopy(b),
                        'proposed_after':{'current':b['current'],'maximum':v},
                        'mutation_mode':'NATIVE_BLOCK_ID_REQUIRED_NOT_AVAILABLE'})
    return {'title':title,'layout':scan['layout'],
            'actions':actions,'native_writer':'HOLD','save_integrity':'BLOCK_TREE_PENDING',
            'images':'MEDIA_INDEPENDENCE_PENDING','child_pages':'FULL_CLOSURE_PENDING',
            'time_of_physical_page_proof':'NOT_PROVIDED_BY_STATIC_EXCERPT',
            'real_notion_mutations':0}
