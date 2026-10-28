# VLAB CM-000006 — R161–R170, MESTRE-SIDE, read-only recovery

1. Extract `VLAB_R161_R170_RECEIPTS_TEMPORAL_CROC_ED_CORRECTED_MESTRE_ONLY.zip` into a **new empty directory**. SHA-256 of the nested `R160_BASELINE_EXACT.zip` must be `7b208fe553809df6a999a1e4f9a70d7ad116033e929256bc71dbcd61843f3410`.
2. Verify `R170_SHA256_MANIFEST.json`; all listed files have exact SHA-256. `R160_BASELINE_EXACT.zip` contains R160 and all prior preserved nested history (including original R150).
3. Cold validation without any historical combat re-execution: `python r161_r170/R170_COLD_PORTABLE_RECOVERY.py <absolute-R170-zip-path> <new-receipt-json-path>`.
4. R160 original 9 DBs are only **read** by `r161_reconcile_and_export.py`; its output is a *new* 154-row corrected CSV, never a modified ledger.
5. The five new approved DBs (R165 V3 1, R166 V2 2, R168 2) have checkpoint SQLite, genesis JSON, prereg and independent cold audit. **Do not rerun** `r165_flecha_temporal_native.py`, `r166_concurrent_cocoon_critical.py`, `r168_crocodile_ed_native.py` on any existing file. They were executors, not idempotent audit tools.
6. R163, R165 V2, R166 first-try and any other `UNKNOWN_EFFECT` historical pending transactions stay **LOCKED**. No blind replay, `DELETE pending`, retry or event transplant. R169 V1 adversarial WAL diagnostic is non-credit; only V2 with modified physical database passes semantic red-team.
7. All Notion source pages were reopened read-only in the authorized Mestre profile. Source authority and gaps are recorded in `R164_MECHANICAL_SOURCE_AND_RESISTANCE_GATES.json`; no source-freeze terminal, no official rules, Party or character sheet writes. No DMG ACK.
8. Contracts preserve original 17 IDs and verbatim terminal criteria in `R170_17_CONTRACTS_BEFORE_AFTER.json`. Official power benchmark remains **0/1875**. Read `R170_PSV_MESTRE_ONLY.md` for denominator separation and FIRST-PENDING.

**R161/R162 semantics:** `gross_spell_dice_pre_save` may be different from `raw_damage` returned by a spell after successful saving throw. `net_post_RD` is not `hp_effectively_lost` when lethal excess exists. Record and cap actual HP loss on committed state; never invent half-odd rounding or unlisted elemental resistance.
