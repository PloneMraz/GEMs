#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""
GEMs budget model — mass, energy, power and data rate.

The platform specification declares envelopes rather than a configuration,
because structure, actuation and energy sit on one coupled loop. This script is
that loop, executable: give it a point and it tells you what the body weighs,
whether the design converges at all, and what the numbers cost elsewhere.

    python scripts/gems_budget.py                  # budget at the default point
    python scripts/gems_budget.py --endurance 6    # a different point
    python scripts/gems_budget.py --json           # machine-readable
    python scripts/gems_budget.py --check          # verify the figures in spec/

Nothing here is a design recommendation. Every operating point is the
controller's to choose; this only prices the choice.
"""

import argparse
import json
import sys
from pathlib import Path

BODY_SKIN_AREA_M2 = 1.8   # skin area of a ~1.75 m body, spec 02.4
G = 9.81


# --------------------------------------------------------------------------
# the coupled loop  (spec 02.1)
# --------------------------------------------------------------------------

def battery_fraction(p_w_per_kg, endurance_h, e_wh_per_kg):
    """f_bat = p*t/e — the share of body mass that is battery."""
    return p_w_per_kg * endurance_h / e_wh_per_kg


def sigma_f(f_str, f_act, p_w_per_kg, endurance_h, e_wh_per_kg):
    return f_str + f_act + battery_fraction(p_w_per_kg, endurance_h, e_wh_per_kg)


def growth_factor(sf):
    """gamma = 1/(1-Sf). None when the design does not converge."""
    return None if sf >= 1.0 else 1.0 / (1.0 - sf)


def endurance_ceiling(f_str, f_act, e_wh_per_kg, p_w_per_kg):
    """t_max = (1 - f_str - f_act) * e / p — beyond this no design exists."""
    return (1.0 - f_str - f_act) * e_wh_per_kg / p_w_per_kg


def armour_mass(coverage, areal_kg_per_m2, area_m2=BODY_SKIN_AREA_M2):
    return area_m2 * coverage * areal_kg_per_m2


# --------------------------------------------------------------------------
# what the loop prices  (spec 02.6, 02.7, 03, 06.4)
# --------------------------------------------------------------------------

def shoulder_torque(load_kg, reach_m):
    """tau = M*g*L, spec 02.6."""
    return load_kg * G * reach_m


def actuator_mass_for_torque(torque_nm, nm_per_kg=33.0):
    return torque_nm / nm_per_kg


def source_peak_kw(pack_kwh, c_rate):
    return pack_kwh * c_rate


def self_discharge_w(pack_kwh, percent_per_month):
    return pack_kwh * 1000.0 * (percent_per_month / 100.0) / (30 * 24)


def sleep_hours(pack_kwh, floor_w):
    return pack_kwh * 1000.0 / floor_w


def joint_torque_total(body_mass_kg):
    """Summed peak joint torque of the declared kinematics.

    Delegates to the sizing model in hardware/electrical so that the torque
    table has one home. Duplicating it here is how the two would drift.
    """
    import sys
    from pathlib import Path
    d = str(Path(__file__).resolve().parent.parent / "hardware" / "electrical")
    if d not in sys.path:
        sys.path.insert(0, d)
    from actuator_sizing import torque_table
    return sum(r[3] for r in torque_table(body_mass_kg))


def carry_capacity(body_mass_kg):
    """(kg at the module's peak, kg at its rated torque, limiting joints) —
    hardware/electrical/actuator_sizing.py, against the AKH70-48."""
    import sys
    from pathlib import Path
    d = str(Path(__file__).resolve().parent.parent / "hardware" / "electrical")
    if d not in sys.path:
        sys.path.insert(0, d)
    from actuator_sizing import carry_capacity as cc
    return cc(body_mass_kg)


def torque_split():
    """(Nm per kg of body for legs and trunk, fixed Nm for arms, wrists, neck)."""
    import sys
    from pathlib import Path
    d = str(Path(__file__).resolve().parent.parent / "hardware" / "electrical")
    if d not in sys.path:
        sys.path.insert(0, d)
    from actuator_sizing import split
    return split()


def actuator_split(density):
    """f_act_s: the actuator fraction that scales with body mass (legs, trunk);
    m_act_fixed: the actuator mass that does not (arms, wrists, neck), which
    the loop carries in m_ext."""
    per_kg, fixed = torque_split()
    return per_kg / density, fixed / density


def log_bytes_per_s(dof=41, channels=4, bytes_per_sample=4, hz=500):
    return dof * channels * bytes_per_sample * hz


def gbps(bytes_per_s):
    return bytes_per_s * 8 / 1e9


# --------------------------------------------------------------------------
# a full budget at one operating point
# --------------------------------------------------------------------------

def budget(f_str, density, p, endurance, e, coverage, areal, m_fixed,
           kw_per_kg=4.0, c_rate=5.0):
    f_act_s, m_act_fixed = actuator_split(density)
    sf = sigma_f(f_str, f_act_s, p, endurance, e)
    gamma = growth_factor(sf)
    t_max = endurance_ceiling(f_str, f_act_s, e, p)
    m_arm = armour_mass(coverage, areal)
    m_ext = m_arm + m_fixed + m_act_fixed

    out = {
        "inputs": {
            "f_str": f_str, "density_Nm_per_kg": density, "p_W_per_kg": p,
            "endurance_h": endurance, "e_Wh_per_kg": e,
            "armour_coverage": coverage, "armour_areal_kg_per_m2": areal,
            "m_fixed_kg": m_fixed,
        },
        "f_act_scaling": round(f_act_s, 4),
        "actuator_fixed_kg": round(m_act_fixed, 2),
        "sigma_f": round(sf, 4),
        "converges": gamma is not None,
        "endurance_ceiling_h": round(t_max, 2),
        "armour_kg": round(m_arm, 2),
        "non_scaling_kg": round(m_ext, 2),
    }
    if gamma is None:
        out["verdict"] = (
            "DOES NOT CONVERGE. The scaling terms consume the whole body; "
            "nothing is left for armour, sensors or hands. This is not an "
            "expensive design, it is not a design."
        )
        return out

    m = gamma * m_ext
    m_act = m * f_act_s + m_act_fixed
    pack_kwh = m * battery_fraction(p, endurance, e) * e / 1000.0
    carry_peak, carry_rated, carry_joint = carry_capacity(m)
    out.update({
        "gamma": round(gamma, 2),
        "body_mass_kg": round(m, 1),
        "structure_kg": round(m * f_str, 1),
        "actuator_kg": round(m_act, 1),
        "f_act": round(m_act / m, 3),
        "battery_kg": round(m * battery_fraction(p, endurance, e), 1),
        "pack_kWh": round(pack_kwh, 2),
        "actuator_peak_kW": round(m_act * kw_per_kg, 0),
        "source_peak_kW": round(source_peak_kw(pack_kwh, c_rate), 1),
        "mass_price_per_kg_added": round(gamma, 2),
        "carry_kg_at_peak": round(carry_peak, 1),
        "carry_kg_at_rated": round(carry_rated, 1),
        "carry_limited_by": carry_joint,
    })
    out["binding_peak_limit"] = (
        "source" if out["source_peak_kW"] < out["actuator_peak_kW"] else "actuators"
    )
    return out


def print_report(b):
    i = b["inputs"]
    print("GEMs budget — one operating point")
    print("=" * 60)
    print("inputs   f_str %.2f  actuators %g Nm/kg  p %g W/kg  t %g h  e %g Wh/kg"
          % (i["f_str"], i["density_Nm_per_kg"], i["p_W_per_kg"], i["endurance_h"], i["e_Wh_per_kg"]))
    print("         armour %d%% coverage at %g kg/m2, fixed mass %g kg"
          % (i["armour_coverage"] * 100, i["armour_areal_kg_per_m2"], i["m_fixed_kg"]))
    print()
    print("actuators  scaling part f_act_s = %.3f of body (legs, trunk)" % b["f_act_scaling"])
    print("           fixed part   %.1f kg (arms, wrists, neck) -> in m_ext" % b["actuator_fixed_kg"])
    print()
    print("loop     Sf = %.3f   (converges when Sf < 1)" % b["sigma_f"])
    print("         endurance ceiling t_max = %.1f h" % b["endurance_ceiling_h"])
    if not b["converges"]:
        print()
        print("VERDICT  " + b["verdict"])
        return
    print("         gamma = %.2f  -> every 1 kg of function costs %.2f kg of body"
          % (b["gamma"], b["gamma"]))
    print()
    print("mass     body           %6.1f kg" % b["body_mass_kg"])
    print("         structure      %6.1f kg" % b["structure_kg"])
    print("         actuators      %6.1f kg   (f_act %.2f)" % (b["actuator_kg"], b["f_act"]))
    print("         battery        %6.1f kg   (%.2f kWh)"
          % (b["battery_kg"], b["pack_kWh"]))
    print("         armour         %6.1f kg" % b["armour_kg"])
    print("         fixed          %6.1f kg   (compute, sensors, hands, skin, harness)" % i["m_fixed_kg"])
    print()
    print("carry    legs, %s, against the AKH70-48 (222 Nm peak, 74 Nm rated):" % b["carry_limited_by"])
    for k, label in (("carry_kg_at_peak", "one stand-up or step"), ("carry_kg_at_rated", "a sustained climb")):
        v = b[k]
        print("         %-22s %s" % (label, "%.0f kg" % v if v >= 0 else "none, body over by %.0f kg" % -v))
    print()
    print("power    actuators accept %5.0f kW" % b["actuator_peak_kW"])
    print("         source delivers  %5.1f kW" % b["source_peak_kW"])
    print("         peak is limited by: %s" % b["binding_peak_limit"].upper())


# --------------------------------------------------------------------------
# --check : recompute what the specification states
# --------------------------------------------------------------------------

def _fmt(v, nd=1):
    return ("%." + str(nd) + "f") % v


def collect_claims():
    """(id, spec file, computed string, description)"""
    c = []

    F_STR = 0.30
    DENSITY = 80.0
    f_act_s, m_act_fixed = actuator_split(DENSITY)
    M_EXT_MID = 28.8                   # mid of the m_ext range of 02.5, before actuators

    # 02.2 the split
    c.append(("f_act_s", "spec/02-structure-and-motion.md",
              "**%.3f**" % f_act_s, "scaling actuator fraction, legs and trunk at 80 Nm/kg"))
    c.append(("m_act_fixed", "spec/02-structure-and-motion.md",
              "**%.1f kg**" % m_act_fixed, "fixed actuator mass, arms, wrists and neck at 80 Nm/kg"))

    # 02.3 endurance ceilings, f_str + f_act_s
    for p in (10, 15, 20, 25):
        c.append(("t_max e450 p%d" % p, "spec/02-structure-and-motion.md",
                  _fmt(endurance_ceiling(F_STR, f_act_s, 450, p)) + " h",
                  "endurance ceiling at e=450, p=%d" % p))
    for p in (10, 15, 20, 25):
        c.append(("t_max e900 p%d" % p, "spec/02-structure-and-motion.md",
                  _fmt(endurance_ceiling(F_STR, f_act_s, 900, p)) + " h",
                  "endurance ceiling at e=900, p=%d" % p))

    # 02.3 growth factors at e=450
    for p, t in ((10, 2), (10, 10), (15, 4), (15, 10), (20, 2), (20, 4), (20, 6), (20, 8), (20, 10), (25, 8)):
        g = growth_factor(sigma_f(F_STR, f_act_s, p, t, 450))
        c.append(("gamma p%d t%d" % (p, t), "spec/02-structure-and-motion.md",
                  _fmt(g, 1) if g else "*diverges*", "growth factor at p=%d, t=%dh" % (p, t)))

    # 02.4 armour mass, and its price at the 4 h point
    for cov, areal in ((0.50, 6), (0.50, 9), (0.65, 6), (0.65, 9), (0.80, 6), (0.80, 9)):
        c.append(("armour %d%% @%d" % (cov * 100, areal), "spec/02-structure-and-motion.md",
                  _fmt(armour_mass(cov, areal)) + " kg",
                  "armour at %d%% coverage, %d kg/m2" % (cov * 100, areal)))
    g4 = growth_factor(sigma_f(F_STR, f_act_s, 20, 4, 450))
    d_arm = armour_mass(0.80, 6) - armour_mass(0.50, 6)
    c.append(("gamma 4h", "spec/02-structure-and-motion.md", "γ=%.1f" % g4,
              "growth factor at the 4 h point"))
    c.append(("armour price", "spec/02-structure-and-motion.md",
              "~%d kg of armour — and **~%d kg of\n> body**" % (round(d_arm), round(d_arm * g4)),
              "body cost of 80% over 50% coverage at 6 kg/m2, times γ"))

    # 02.5 Asimov scaling cross-check
    scaled = 35.0 * (1.75 / 1.2) ** 3
    c.append(("asimov scale", "spec/02-structure-and-motion.md",
              "%.2f" % ((1.75 / 1.2) ** 3), "mass scaling ratio (1.75/1.2)^3"))
    c.append(("asimov mass", "spec/02-structure-and-motion.md",
              "~%d kg" % round(scaled), "35 kg body scaled to 1.75 m"))

    # 02.5 mass envelope: gamma and body range per operating point
    for label, t, e in (("2h durable", 2, 450), ("4h durable", 4, 450),
                        ("8h ceiling", 8, 900), ("6h durable", 6, 450)):
        g = growth_factor(sigma_f(F_STR, f_act_s, 20, t, e))
        lo, hi = (20 + m_act_fixed) * g, (38 + m_act_fixed) * g
        c.append(("envelope %s" % label, "spec/02-structure-and-motion.md",
                  "| %.1f | **%d–%d kg** |" % (g, round(lo), round(hi)) if t != 6
                  else "| %.1f | %d–%d kg" % (g, round(lo), round(hi)),
                  "growth factor and body range, %s" % label))

    # 02.6 shoulder torque as a lever, M*g*L, and the sized arm joints
    for load, reach in ((5, 0.40), (15, 0.64), (30, 0.64), (50, 0.64)):
        t = shoulder_torque(load, reach)
        c.append(("torque %dkg %.2fm" % (load, reach), "spec/02-structure-and-motion.md",
                  "%d Nm (%.2f kg)" % (round(t), actuator_mass_for_torque(t, DENSITY)),
                  "shoulder torque and actuator mass, %d kg at %.2f m" % (load, reach)))
    from actuator_sizing import arm_torques, SHOULDER_TO_GRIP, ELBOW_TO_GRIP  # noqa: E402
    arms = arm_torques(DENSITY)
    for key, label in (("shoulder", "shoulder pitch"), ("shoulder_roll", "shoulder roll"), ("elbow", "elbow")):
        pay, own = arms[key]
        c.append(("sized %s" % key, "spec/02-structure-and-motion.md",
                  "| %d | %d | **%d Nm** |" % (round(pay), round(own), round(pay + own)),
                  "%s: payload, self-weight, total" % label))
    c.append(("grip levers", "spec/02-structure-and-motion.md",
              "%.2f m from the shoulder and %.2f m from the elbow" % (SHOULDER_TO_GRIP, ELBOW_TO_GRIP),
              "grip-centre levers"))

    # 02.6 the density-to-f_act mapping — the coupling that must not drift
    total_nm = joint_torque_total(130.0)
    per_kg, fixed_nm = torque_split()
    c.append(("joint torque total", "spec/02-structure-and-motion.md",
              "**%d Nm**" % round(total_nm),
              "summed joint torque of the declared kinematics at 130 kg"))
    c.append(("torque split", "spec/02-structure-and-motion.md",
              "%d Nm of it scales with body mass and %d Nm does not" % (round(per_kg * 130), round(fixed_nm)),
              "the two parts of the summed torque"))
    for d in (80, 85, 90):
        m = total_nm / d
        c.append(("f_act @%d" % d, "spec/02-structure-and-motion.md",
                  "%.1f kg | **%.2f**" % (m, m / 130.0) if d != 85
                  else "%.1f kg | %.2f" % (m, m / 130.0),
                  "actuator mass and f_act at %d Nm/kg" % d))
    c.append(("f_act band", "spec/02-structure-and-motion.md",
              "80–90 Nm/kg maps onto `f_act` %.2f–%.2f" % (total_nm / 90 / 130.0, total_nm / 80 / 130.0),
              "the density band and the f_act band, stated as one constraint"))
    c.append(("f_act floor", "spec/02-structure-and-motion.md",
              "allow a floor near %d Nm/kg" % round(total_nm / 0.35 / 130.0),
              "the density at which f_act touches 0.35"))

    # 02.6 carry capacity at both operating points
    for t in (2, 4):
        b = budget(F_STR, DENSITY, 20, t, 450, 0.65, 7.5, 20.0)
        v = b["carry_kg_at_peak"]
        c.append(("carry t%dh" % t, "spec/02-structure-and-motion.md",
                  ("**%d kg**" % round(v)) if v >= 0 else ("exceeds it by %d kg" % round(-v)),
                  "carry capacity at peak, %d h point" % t))

    # 02.7 both operating points, derived here rather than transcribed
    for t in (2, 4):
        b = budget(F_STR, DENSITY, 20, t, 450, 0.65, 7.5, 20.0)
        m, kwh, m_act = b["body_mass_kg"], b["pack_kWh"], b["actuator_kg"]
        c.append(("body t%dh" % t, "spec/02-structure-and-motion.md",
                  "~%d kg" % round(m), "body mass at the %d h point" % t))
        c.append(("pack t%dh" % t, "spec/02-structure-and-motion.md",
                  "%.1f kWh" % kwh, "pack size at the %d h point" % t))
        c.append(("actuators t%dh" % t, "spec/02-structure-and-motion.md",
                  "%d–%d kW" % (round(m_act * 3), round(m_act * 5)),
                  "actuator power band at the %d h point" % t))
        for cr in (3, 5, 10):
            c.append(("source t%dh %dC" % (t, cr), "spec/02-structure-and-motion.md",
                      "%d kW" % round(source_peak_kw(kwh, cr)),
                      "source peak at the %d h point, %dC" % (t, cr)))

    # 03.6 self-discharge and sleep, on the pack figure 02.7 quotes
    PACK = round(budget(F_STR, DENSITY, 20, 4, 450, 0.65, 7.5, 20.0)["pack_kWh"], 1)
    for pct in (1, 2, 3):
        c.append(("selfdisch %d%%" % pct, "spec/03-energy.md",
                  "%d mW" % round(self_discharge_w(PACK, pct) * 1000),
                  "self-discharge on the %.1f kWh pack at %d%%/month" % (PACK, pct)))
    base = self_discharge_w(PACK, 2)
    for extra, label in ((0.0008, "deep"), (0.0188, "passive sensing"),
                         (0.2008, "full-CSI sensing")):
        yrs = sleep_hours(PACK, base + extra) / 8760.0
        c.append(("sleep %s" % label, "spec/03-energy.md", "~%.1f years" % yrs,
                  "sleep duration, %s" % label))

    # 06.4 log rate at the declared joint count
    bps = log_bytes_per_s()
    c.append(("log kB/s", "spec/06-audit-surface.md", "%d kB/s" % round(bps / 1000),
              "full-tier log rate"))
    c.append(("log Mbps", "spec/06-audit-surface.md", "%.1f Mbps" % (gbps(bps) * 1000),
              "full-tier log rate in Mbps"))
    c.append(("log GB/h", "spec/06-audit-surface.md", "%.2f GB/hour" % (bps * 3600 / 1e9),
              "full-tier log volume per hour"))

    # hardware/kinematics.md — the three joint-count configurations
    for dof, label in ((31, "core only"), (41, "core + minimum hands"),
                       (73, "core + anthropomorphic hands")):
        b = log_bytes_per_s(dof=dof)
        c.append(("log %d DOF" % dof, "hardware/kinematics.md",
                  "%d kB/s · %.1f Mbps · %.2f GB/h"
                  % (round(b / 1000), gbps(b) * 1000, b * 3600 / 1e9),
                  "log rate at %s (%d joints)" % (label, dof)))
    return c


def run_check(root):
    claims = collect_claims()
    missing = []
    for cid, path, text, desc in claims:
        f = root / path
        if not f.exists():
            missing.append((cid, path, text, desc, "spec file not found"))
            continue
        if text not in f.read_text(encoding="utf-8"):
            missing.append((cid, path, text, desc, "not found in text"))

    print("GEMs budget check — %d computed figures against spec/" % len(claims))
    print("=" * 60)
    if not missing:
        print("OK  every figure recomputed here appears in the specification.")
        return 0
    for cid, path, text, desc, why in missing:
        print("MISMATCH  %-22s %s" % (cid, desc))
        print("          computed %r, %s in %s" % (text, why, path))
    print()
    print("%d of %d figures did not match." % (len(missing), len(claims)))
    print("A mismatch means the specification and this model disagree, or the")
    print("specification's wording changed. Look at both; do not assume either.")
    return 1


# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="GEMs mass, energy and power budget.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Defaults sit at the 4-hour durable-pack point of spec 02.5.")
    ap.add_argument("--f-str", type=float, default=0.30, help="structure mass fraction")
    ap.add_argument("--density", type=float, default=80.0,
                    help="actuator torque density, Nm/kg peak over module mass")
    ap.add_argument("--p", type=float, default=20.0, help="specific power, W/kg")
    ap.add_argument("--endurance", type=float, default=4.0, help="free-running hours")
    ap.add_argument("--e", type=float, default=450.0, help="battery density, Wh/kg")
    ap.add_argument("--coverage", type=float, default=0.65, help="armour coverage, 0-1")
    ap.add_argument("--areal", type=float, default=7.5, help="armour areal density, kg/m2")
    ap.add_argument("--m-fixed", type=float, default=20.0, help="fixed non-scaling mass, kg")
    ap.add_argument("--kw-per-kg", type=float, default=4.0, help="actuator specific power")
    ap.add_argument("--c-rate", type=float, default=5.0, help="pack discharge C-rate")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--check", action="store_true",
                    help="recompute the figures quoted in spec/ and compare")
    a = ap.parse_args(argv)

    root = Path(__file__).resolve().parent.parent
    if a.check:
        return run_check(root)

    b = budget(a.f_str, a.density, a.p, a.endurance, a.e,
               a.coverage, a.areal, a.m_fixed, a.kw_per_kg, a.c_rate)
    if a.json:
        print(json.dumps(b, indent=2))
    else:
        print_report(b)
    return 0 if b["converges"] else 2


if __name__ == "__main__":
    sys.exit(main())
