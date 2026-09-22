#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""Tests for the emission log.

Each test names the conformance requirement it exercises, so a failure points
at a clause rather than at a function.

    python -m unittest discover -s software -v
"""

import hashlib
import hmac
import unittest
from dataclasses import replace

from audit_log import (Agency, Batch, EmissionLog, Record, Tier, merkle_root,
                       verify, GENESIS)

KEY = b"test-key-not-a-signature-scheme"


def sign(root: bytes) -> bytes:
    return hmac.new(KEY, root, hashlib.sha256).digest()


def verify_sig(root: bytes, sig: bytes) -> bool:
    return hmac.compare_digest(sign(root), sig)


def telemetry(seq, t=0):
    return Record(seq=seq, t_ns=t, tier=Tier.FULL, kind="joint_sample",
                  agency=Agency.SELF_CAUSED,
                  payload={"joint": 3, "cmd": 0.1, "pos": 0.09,
                           "cur": 1.2, "torque": 4.4})


def emission(seq, t=0, **kw):
    base = dict(seq=seq, t_ns=t, tier=Tier.EMISSION, kind="reflex_withdraw",
                agency=Agency.SELF_CAUSED,
                context={"field": "scar_dominated", "trigger": "thermal",
                         "window_ns": 4_000_000})
    base.update(kw)
    return Record(**base)


class TestWriteRules(unittest.TestCase):
    """The log refuses records the specification forbids."""

    def test_emission_without_context_is_refused(self):
        """C-9 — every emission carries anchored context, reflexes included."""
        log = EmissionLog(sign)
        with self.assertRaises(ValueError) as e:
            log.append(emission(0, context=None))
        self.assertIn("anchored context", str(e.exception))

    def test_unclassified_emission_is_refused(self):
        """C-8 — classification precedes interpretation."""
        log = EmissionLog(sign)
        with self.assertRaises(ValueError) as e:
            log.append(emission(0, agency=Agency.UNCLASSIFIED))
        self.assertIn("before interpretation", str(e.exception))

    def test_contact_without_amplitude_is_refused(self):
        """C-12 — contact events record measured amplitude."""
        log = EmissionLog(sign)
        with self.assertRaises(ValueError) as e:
            log.append(emission(0, kind="contact", contact=True))
        self.assertIn("amplitude", str(e.exception))

    def test_contact_with_amplitude_is_accepted(self):
        log = EmissionLog(sign)
        log.append(emission(0, kind="contact", contact=True,
                            amplitude={"force_N": 2.4, "temp_C": 33.1,
                                       "vib_hz": 1.1, "duration_ms": 900}))
        self.assertEqual(len(log.records), 1)

    def test_out_of_order_seq_is_refused(self):
        """C-3, C-6 — a log that renumbers to hide a gap is worse than one
        that shows it."""
        log = EmissionLog(sign)
        log.append(telemetry(0))
        with self.assertRaises(ValueError):
            log.append(telemetry(5))


class TestChainAndBatch(unittest.TestCase):

    def test_chain_links_every_record(self):
        log = EmissionLog(sign)
        links = [log.append(telemetry(i, t=i * 2_000_000)) for i in range(5)]
        self.assertEqual(len(set(links)), 5)

    def test_batch_root_covers_its_window(self):
        log = EmissionLog(sign)
        for i in range(8):
            log.append(telemetry(i))
        b = log.seal_batch()
        self.assertEqual((b.first_seq, b.last_seq), (0, 7))
        self.assertTrue(verify_sig(b.merkle_root, b.signature))

    def test_sealing_twice_splits_windows(self):
        log = EmissionLog(sign)
        for i in range(3):
            log.append(telemetry(i))
        b1 = log.seal_batch()
        for i in range(3, 7):
            log.append(telemetry(i))
        b2 = log.seal_batch()
        self.assertEqual((b1.first_seq, b1.last_seq), (0, 2))
        self.assertEqual((b2.first_seq, b2.last_seq), (3, 6))

    def test_empty_seal_returns_none(self):
        self.assertIsNone(EmissionLog(sign).seal_batch())

    def test_odd_node_is_promoted_not_duplicated(self):
        """Duplicating the last node would let two distinct batches share one
        root, so a batch could be rewritten under a signature that still
        verifies."""
        a, b, c = (bytes([i]) * 32 for i in (1, 2, 3))
        three = merkle_root([a, b, c])
        four_dup = merkle_root([a, b, c, c])
        self.assertNotEqual(three, four_dup)

    def test_empty_merkle_is_genesis(self):
        self.assertEqual(merkle_root([]), GENESIS)


class TestVerifier(unittest.TestCase):
    """What an assessor runs — protocol §6, evidence class T."""

    def _good_log(self, n=6):
        log = EmissionLog(sign)
        for i in range(n):
            log.append(telemetry(i, t=i * 2_000_000))
        log.seal_batch()
        return log

    def test_clean_log_has_no_findings(self):
        log = self._good_log()
        self.assertEqual(verify(log.records, log.batches, verify_sig), [])

    def test_tampered_payload_breaks_the_root(self):
        log = self._good_log()
        recs = log.records
        recs[2] = replace(recs[2], payload={**recs[2].payload, "torque": 99.9})
        codes = {f.code for f in verify(recs, log.batches, verify_sig)}
        self.assertIn("ROOT_MISMATCH", codes)

    def test_removed_record_is_reported_as_a_gap(self):
        log = self._good_log()
        recs = [r for r in log.records if r.seq != 3]
        codes = {f.code for f in verify(recs, log.batches, verify_sig)}
        self.assertIn("GAP", codes)
        self.assertIn("BATCH_INCOMPLETE", codes)

    def test_forged_signature_is_reported(self):
        log = self._good_log()
        bad = [Batch(b.first_seq, b.last_seq, b.merkle_root, b.chain_head,
                     b"not-a-signature") for b in log.batches]
        codes = {f.code for f in verify(log.records, bad, verify_sig)}
        self.assertIn("BAD_SIGNATURE", codes)

    def test_verifier_reports_context_gaps_it_is_handed(self):
        """A record can reach an assessor without having passed this module's
        write path — a hostile or broken writer. The verifier checks the same
        rules independently."""
        r = Record(seq=0, t_ns=0, tier=Tier.EMISSION, kind="reflex",
                   agency=Agency.SELF_CAUSED, context=None)
        codes = {f.code for f in verify([r], [])}
        self.assertIn("NO_CONTEXT", codes)

    def test_verification_is_not_a_judgement_of_conduct(self):
        """An internally consistent log says nothing about whether the body
        behaved acceptably — protocol §10."""
        log = EmissionLog(sign)
        log.append(emission(0, kind="contact", contact=True,
                            amplitude={"force_N": 400.0, "duration_ms": 30000}))
        log.seal_batch()
        self.assertEqual(verify(log.records, log.batches, verify_sig), [])


if __name__ == "__main__":
    unittest.main()
