"""Mestre R200 prospective spell geometry: exact rational distance + test-only cone aperture.
Never infers cone width, spell cost, LoS, immunity, saving throw or rank.
Validation happens before any native R18 intent is submitted.
"""
from __future__ import annotations
from fractions import Fraction as F
from dataclasses import dataclass
MASTER='https://app.notion.com/p/3ffc2b324ede81c5a5c3d56cc6a29f84'
class SpatialBlocked(ValueError):pass
class SourceGap(ValueError):pass

def point(x):
    if not isinstance(x,(tuple,list)) or len(x)!=2:raise SpatialBlocked('INVALID_POINT')
    return tuple(F(v) for v in x)
def dist2(a,b):
    a=point(a);b=point(b);return sum((v-w)**2 for v,w in zip(a,b))
def center_range(caster,center,limit):return dist2(caster,center)<=F(limit)**2

def freeze_parameters(kind,specific=None):
    s=dict(specific or {})
    if kind=='single':
        if 'range_m' not in s:s['range_m']=F(9);s['range_origin']=MASTER
    elif kind=='circular':
        if 'radius_m' not in s:s['radius_m']=F(6);s['radius_origin']=MASTER
        if 'center_range_m' not in s:s['center_range_m']=F(9);s['center_range_origin']=MASTER
    elif kind=='cone':
        if 'extension_m' not in s:s['extension_m']=F(9,2);s['extension_origin']=MASTER
        # CANON DOES NOT SAY ANGLE: preserve omission and refuse official target-hit claim.
    else:raise SourceGap('MULTITARGET_SHAPE_UNKNOWN_OR_INCOMPATIBLE')
    return s

def affected(kind,caster,positions,*,specific=None,target=None,center=None,direction=None):
    spec=freeze_parameters(kind,specific)
    caster=point(caster)
    if kind=='single':
        if target is None or target not in positions:raise SpatialBlocked('UNKNOWN_SINGLE_TARGET')
        yes=center_range(caster,positions[target],spec['range_m'])
        return {'hits':[target] if yes else [],'excluded':[] if yes else [target], 'valid':yes,'source':spec,'caster_in_area':False}
    if kind=='circular':
        if center is None:raise SpatialBlocked('CENTER_REQUIRED')
        center=point(center)
        if not center_range(caster,center,spec['center_range_m']):raise SpatialBlocked('INVALID_CENTER_OUTSIDE_CAST_RANGE')
        ids=[i for i,p in positions.items() if dist2(p,center)<=F(spec['radius_m'])**2]
        return {'hits':ids,'excluded':[i for i in positions if i not in ids], 'valid':True,'source':spec,
                'caster_in_area':center_range(caster,center,spec['radius_m'])}
    if kind=='cone':
        if direction is None:raise SpatialBlocked('DIRECTION_REQUIRED')
        if 'half_angle_geometry' not in spec:raise SourceGap('CANONICAL_CONE_APERTURE_UNDOCUMENTED_NO_CANONICAL_HIT_RESOLUTION')
        # For explicit isolated LAB model ONLY, use rational-sided wedge: |cross|<=wedge_ratio*forward.
        # Never advertise as canonical angular aperture. Source must explicitly tag TEST.
        if spec['half_angle_geometry']!='TEST_WEDGE_SLOPE_1_TO_1':raise SourceGap('UNSUPPORTED_CONE_WIDTH')
        if spec.get('aperture_origin')!='LAB_TEST_ONLY':raise SourceGap('APERTURE_SOURCE_MISSING')
        d=point(direction)
        norm2=sum(t*t for t in d)
        if norm2==0:raise SpatialBlocked('ZERO_DIRECTION')
        good=[]
        for i,p in positions.items():
            dx,dy=tuple(v-w for v,w in zip(point(p),caster))
            forward=dx*d[0]+dy*d[1]; cross=dx*d[1]-dy*d[0]
            inside=(forward>=0 and dist2(p,caster)<=F(spec['extension_m'])**2 and abs(cross)<=forward)
            if inside:good.append(i)
        return {'hits':good,'excluded':[i for i in positions if i not in good], 'valid':True,'source':spec,
                'caster_in_area':True, 'mode':'LAB_CONE_WEDGE_NOT_CANONICAL'}
    raise SourceGap('SHAPE_NOT_SUPPORTED')

def preflight_cast(actor,positions,*,spell,pa_free,already_spent_pa,action_available=True,target=None,center=None,direction=None):
    # Only legal preflight, never spends PA or moves actor. The actual state writer makes the atomic debit.
    if spell.get('source') is None:raise SourceGap('SPELL_SOURCE_UNKNOWN')
    if spell.get('known_by')!=actor:raise SpatialBlocked('SPELL_NOT_KNOWN_BY_ACTOR')
    if not action_available:raise SpatialBlocked('ACTION_NOT_AVAILABLE')
    cost=spell.get('cost_pa')
    if cost is None:raise SourceGap('SPELL_COST_UNDOCUMENTED')
    if pa_free-already_spent_pa<cost:raise SpatialBlocked('PA_INSUFFICIENT_PREVENT_INTENT')
    if spell.get('kind') not in ('single','circular','cone'):raise SourceGap('SHAPE_UNCLASSIFIED')
    state=affected(spell['kind'],positions[actor],positions, specific=spell.get('specific'),target=target,center=center,direction=direction)
    if not state['valid']:raise SpatialBlocked('TARGET_OUTSIDE_RANGE_NO_COMMIT')
    # Self-effect cannot be dismissed from area without the source saying so.
    return {**state,'spell':spell['name'],'cost_pa':cost,'action':'STANDARD_UNLESS_SOURCE_SPECIFIC',
            'preflight_no_debit':True,'master_source':MASTER}
