#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""Tests for the agency-tagging reference model.

The centrepiece is `TestProtocolProcedure71`, which runs the procedure
protocol/conformance.md §7.1 specifies, including its pipeline-position check.

    python -m unittest discover -s firmware/reference -t firmware/reference -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "software"))

from audit_log import Agency, AuditLog, Record, Tier
from agency import (AgencyGate, Command, ForwardModel, Sample, Tolerance,
                    UnclassifiableSample, summarise)

MS = 1_000_000


class TestClassification(unittest.TestCase):

    def setUp(self):
        self.gate = AgencyGate()

    def test_return_matching_the_command_is_self_caused(self):
        self.gate.issue(Command(t_ns=0, joint=3, position=0.5, velocity=1.0, torque=4.0))
        v = self.gate.classify(Sample(t_ns=1 * MS, joint=3, position=0.501,
                                      velocity=1.01, torque=4.1))
        self.assertIs(v.agency, Agency.SELF_CAUSED)

    def test_unexplained_torque_is_external(self):
        """Something pushed the joint: it is where it was told to be, carrying
        force nothing commanded."""
        self.gate.issue(Command(t_ns=0, joint=3, position=0.5, velocity=0.0, torque=4.0))
        v = self.gate.classify(Sample(t_ns=1 * MS, joint=3, position=0.5,
                                      velocity=0.0, torque=19.0))
        self.assertIs(v.agency, Agency.EXTERNAL)
        self.assertEqual(v.dominant(), "torque")

    def test_unexplained_motion_is_external(self):
        self.gate.issue(Command(t_ns=0, joint=3, position=0.5, velocity=0.0, torque=4.0))
        v = self.gate.classify(Sample(t_ns=1 * MS, joint=3, position=0.62,
                                      velocity=0.0, torque=4.0))
        self.assertIs(v.agency, Agency.EXTERNAL)
        self.assertEqual(v.dominant(), "position")

    def test_no_command_in_flight_is_external(self):
        v = self.gate.classify(Sample(t_ns=5 * MS, joint=7, position=0.2,
                                      velocity=0.0, torque=6.0))
        self.assertIs(v.agency, Agency.EXTERNAL)
        self.assertIn("no command in flight", v.reason)

    def test_stale_command_does_not_explain_a_later_return(self):
        """A command outside the matching window is not an explanation."""
        self.gate.issue(Command(t_ns=0, joint=3, position=0.5, velocity=0.0, torque=4.0))
        v = self.gate.classify(Sample(t_ns=50 * MS, joint=3, position=0.5,
                                      velocity=0.0, torque=4.0))
        self.assertIs(v.agency, Agency.EXTERNAL)

    def test_command_for_another_joint_does_not_explain_this_one(self):
        self.gate.issue(Command(t_ns=0, joint=3, position=0.5, velocity=0.0, torque=4.0))
        v = self.gate.classify(Sample(t_ns=1 * MS, joint=9, position=0.5,
                                      velocity=0.0, torque=4.0))
        self.assertIs(v.agency, Agency.EXTERNAL)

    def test_missing_time_base_raises_rather_than_tagging_unclassified(self):
        """C-15. A pipeline that quietly tags UNCLASSIFIED has defeated INV-6
        while appearing to satisfy it."""
        with self.assertRaises(UnclassifiableSample):
            self.gate.classify(Sample(t_ns=-1, joint=3, position=0.0,
                                      velocity=0.0, torque=0.0))

    def test_tolerance_is_configurable(self):
        tight = AgencyGate(tolerance=Tolerance(position=0.0001, velocity=0.0001,
                                               torque=0.0001))
        tight.issue(Command(t_ns=0, joint=1, position=0.5, velocity=0.0, torque=4.0))
        v = tight.classify(Sample(t_ns=1 * MS, joint=1, position=0.501,
                                  velocity=0.0, torque=4.0))
        self.assertIs(v.agency, Agency.EXTERNAL)


class TestProtocolProcedure71(unittest.TestCase):
    """protocol/conformance.md §7.1 — C-8, agency classification.

    Procedure: command a known motion; during that motion apply an external
    force at a surface the body is not moving with; inspect the log.

    Pass: the log distinguishes the commanded motion from the applied force,
    and the distinction is present in records written *before* any fusion or
    compression stage.
    """

    MOVING_JOINT = 3        # commanded through a known arc
    STRUCK_JOINT = 11       # a surface the body is not moving with

    def _run_procedure(self):
        gate = AgencyGate()
        log = AuditLog()
        seq = 0

        for step in range(6):
            t = step * MS
            # the commanded motion
            cmd = Command(t_ns=t, joint=self.MOVING_JOINT,
                          position=0.1 * step, velocity=1.0, torque=5.0)
            gate.issue(cmd)
            moving = Sample(t_ns=t + 200_000, joint=self.MOVING_JOINT,
                            position=0.1 * step + 0.002, velocity=1.01, torque=5.05)

            # the external force, on a joint carrying no command
            struck = Sample(t_ns=t + 200_000, joint=self.STRUCK_JOINT,
                            position=0.0, velocity=0.0,
                            torque=24.0 if step == 3 else 0.0)

            for s in (moving, struck):
                v = gate.classify(s)
                log.append(Record(
                    seq=seq, t_ns=s.t_ns, tier=Tier.FULL, kind="joint_sample",
                    agency=v.agency,
                    payload={"joint": s.joint, "pos": s.position,
                             "torque": s.torque, "residual": v.residual,
                             "stage": "pre_fusion"}))
                seq += 1
        return log

    def test_the_log_distinguishes_the_two(self):
        log = self._run_procedure()
        moving = [r for r in log.records if r.payload["joint"] == self.MOVING_JOINT]
        struck = [r for r in log.records if r.payload["joint"] == self.STRUCK_JOINT]

        self.assertTrue(all(r.agency is Agency.SELF_CAUSED for r in moving),
                        "commanded motion was not recognised as self-caused")
        self.assertTrue(all(r.agency is Agency.EXTERNAL for r in struck),
                        "the struck joint was not recognised as external")

    def test_the_distinction_is_written_before_fusion(self):
        """The half of §7.1 that a conclusion-only check would miss."""
        log = self._run_procedure()
        self.assertTrue(all(r.payload["stage"] == "pre_fusion" for r in log.records))
        self.assertTrue(all("residual" in r.payload for r in log.records),
                        "the residual the classification rests on was not kept, "
                        "so an assessor cannot re-derive the tag")

    def test_no_record_leaves_the_gate_unclassified(self):
        log = self._run_procedure()
        self.assertEqual(
            [r.seq for r in log.records if r.agency is Agency.UNCLASSIFIED], [])

    def test_summary_counts(self):
        log = self._run_procedure()
        self.assertEqual(len(log.records), 12)
        ext = [r for r in log.records if r.agency is Agency.EXTERNAL]
        self.assertEqual(len(ext), 6, "every sample on the struck joint is external")


class TestForwardModelIsReplaceable(unittest.TestCase):

    def test_a_better_model_changes_the_verdict(self):
        """The gate does not care how the prediction is made. A model that
        accounts for gravity sag explains a return the trivial one calls
        external."""

        class SaggingModel(ForwardModel):
            def predict(self, cmd, at_t_ns):
                s = super().predict(cmd, at_t_ns)
                return Sample(s.t_ns, s.joint, s.position - 0.05, s.velocity, s.torque)

        cmd = Command(t_ns=0, joint=2, position=0.5, velocity=0.0, torque=3.0)
        sample = Sample(t_ns=MS, joint=2, position=0.45, velocity=0.0, torque=3.0)

        naive = AgencyGate()
        naive.issue(cmd)
        self.assertIs(naive.classify(sample).agency, Agency.EXTERNAL)

        better = AgencyGate(model=SaggingModel())
        better.issue(cmd)
        self.assertIs(better.classify(sample).agency, Agency.SELF_CAUSED)


if __name__ == "__main__":
    unittest.main()
