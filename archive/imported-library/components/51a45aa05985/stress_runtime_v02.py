"""Deterministic synthetic stress of no-healing & damage-temp-first properties."""
from random import Random
from evolution_runtime import projected_resources, apply_damage_temporary_first

rng=Random(1709)
for i in range(2500):
    cap=rng.randint(0,80000); current=rng.randint(0,cap)
    pcap=rng.randint(0,80000); pcurrent=rng.randint(0,pcap)
    tempcap=rng.randint(0,20000); temp=rng.randint(0,tempcap)
    nxt=cap+rng.randint(0,5000); pnext=pcap+rng.randint(0,5000); tnext=tempcap+rng.randint(0,3000)
    state={'vida_atual':current,'vida_maxima':cap,'pa_atual':pcurrent,'pa_capacidade':pcap,'vida_temp_atual':temp,'vida_temp_maxima':tempcap}
    new=projected_resources(state,before_max_vida=cap,after_max_vida=nxt,before_pa_capacity=pcap,
                            after_pa_capacity=pnext,after_temp_max=tnext)['after']
    assert new['vida_atual']==current and new['pa_atual']==pcurrent and new['vida_temp_atual']==temp
    dmg=rng.randint(0,3000); struck=apply_damage_temporary_first(state,dmg)
    assert struck['vida_temp_atual']==max(0,temp-dmg)
    assert struck['vida_atual']==max(0,current-max(0,dmg-temp))
print('STRESS RUNTIME v0.2: 2500/2500 casos sintéticos aprovados (no autoheal, temp damage first)')
