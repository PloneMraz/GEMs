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


def actuator_peak_kw(body_mass_kg, f_act, kw_per_kg):
    return body_mass_kg * f_act * kw_per_kg


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


def log_bytes_per_s(dof=41, channels=4, bytes_per_sample=4, hz=500):
    return dof * channels * bytes_per_sample * hz


def gbps(bytes_per_s):
    return bytes_per_s * 8 / 1e9


# --------------------------------------------------------------------------
# a full budget at one operating point
# --------------------------------------------------------------------------

def budget(f_str, f_act, p, endurance, e, coverage, areal, m_fixed,
           kw_per_kg=4.0, c_rate=5.0):
    sf = sigma_f(f_str, f_act, p, endurance, e)
    gamma = growth_factor(sf)
    t_max = endurance_ceiling(f_str, f_act, e, p)
    m_arm = armour_mass(coverage, areal)
    m_ext = m_arm + m_fixed

    out = {
        "inputs": {
            "f_str": f_str, "f_act": f_act, "p_W_per_kg": p,
            "endurance_h": endurance, "e_Wh_per_kg": e,
            "armour_coverage": coverage, "armour_areal_kg_per_m2": areal,
            "m_fixed_kg": m_fixed,
        },
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
    pack_kwh = m * battery_fraction(p, endurance, e) * e / 1000.0
    out.update({
        "gamma": round(gamma, 2),
        "body_mass_kg": round(m, 1),
        "structure_kg": round(m * f_str, 1),
        "actuator_kg": round(m * f_act, 1),
        "battery_kg": round(m * battery_fraction(p, endurance, e), 1),
        "pack_kWh": round(pack_kwh, 2),
        "actuator_peak_kW": round(actuator_peak_kw(m, f_act, kw_per_kg), 0),
        "source_peak_kW": round(source_peak_kw(pack_kwh, c_rate), 1),
        "mass_price_per_kg_added": round(gamma, 2),
    })
    out["binding_peak_limit"] = (
        "source" if out["source_peak_kW"] < out["actuator_peak_kW"] else "actuators"
    )
    return out


def print_report(b):
    i = b["inputs"]
    print("GEMs budget — one operating point")
    print("=" * 60)
    print("inputs   f_str %.2f  f_act %.2f  p %g W/kg  t %g h  e %g Wh/kg"
          % (i["f_str"], i["f_act"], i["p_W_per_kg"], i["endurance_h"], i["e_Wh_per_kg"]))
    print("         armour %d%% coverage at %g kg/m2, fixed mass %g kg"
          % (i["armour_coverage"] * 100, i["armour_areal_kg_per_m2"], i["m_fixed_kg"]))
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
    print("         actuators      %6.1f kg" % b["actuator_kg"])
    print("         battery        %6.1f kg   (%.2f kWh)"
          % (b["battery_kg"], b["pack_kWh"]))
    print("         armour         %6.1f kg" % b["armour_kg"])
    print("         fixed          %6.1f kg" % i["m_fixed_kg"])
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

    # 02.3 endurance ceilings, f_str+f_act = 0.60
    for p, exp in ((10, 18.0), (15, 12.0), (20, 9.0), (25, 7.2)):
        c.append(("t_max e450 p%d" % p, "spec/02-structure-and-motion.md",
                  _fmt(endurance_ceiling(0.30, 0.30, 450, p)) + " h",
                  "endurance ceiling at e=450, p=%d" % p))
    for p, exp in ((10, 36.0), (15, 24.0), (20, 18.0), (25, 14.4)):
        c.append(("t_max e900 p%d" % p, "spec/02-structure-and-motion.md",
                  _fmt(endurance_ceiling(0.30, 0.30, 900, p)) + " h",
                  "endurance ceiling at e=900, p=%d" % p))

    # 02.3 growth factors at e=450
    for p, t in ((20, 2), (20, 4), (20, 6), (20, 8), (15, 10)):
        g = growth_factor(sigma_f(0.30, 0.30, p, t, 450))
        c.append(("gamma p%d t%d" % (p, t), "spec/02-structure-and-motion.md",
                  _fmt(g, 1), "growth factor at p=%d, t=%dh" % (p, t)))

    # 02.4 armour mass
    for cov, areal in ((0.50, 6), (0.50, 9), (0.65, 6), (0.65, 9), (0.80, 6), (0.80, 9)):
        c.append(("armour %d%% @%d" % (cov * 100, areal), "spec/02-structure-and-motion.md",
                  _fmt(armour_mass(cov, areal)) + " kg",
                  "armour at %d%% coverage, %d kg/m2" % (cov * 100, areal)))

    # 02.5 Asimov scaling cross-check
    scaled = 35.0 * (1.75 / 1.2) ** 3
    c.append(("asimov scale", "spec/02-structure-and-motion.md",
              "%.2f" % ((1.75 / 1.2) ** 3), "mass scaling ratio (1.75/1.2)^3"))
    c.append(("asimov mass", "spec/02-structure-and-motion.md",
              "~%d kg" % round(scaled), "35 kg body scaled to 1.75 m"))

    # 02.6 shoulder torque, and the actuator mass that follows at 80 Nm/kg
    for load, reach in ((5, 0.40), (15, 0.70), (30, 0.70), (50, 0.70)):
        t = shoulder_torque(load, reach)
        c.append(("torque %dkg %.2fm" % (load, reach), "spec/02-structure-and-motion.md",
                  "%d Nm (%.2f kg)" % (round(t), actuator_mass_for_torque(t, 80.0)),
                  "shoulder torque and actuator mass, %d kg at %.2f m" % (load, reach)))

    # 02.6 the density-to-f_act mapping — the coupling that must not drift
    total_nm = joint_torque_total(130.0)
    c.append(("joint torque total", "spec/02-structure-and-motion.md",
              "**%d Nm**" % round(total_nm),
              "summed joint torque of the declared kinematics at 130 kg"))
    for d in (80, 85, 90):
        m = total_nm / d
        c.append(("f_act @%d" % d, "spec/02-structure-and-motion.md",
                  "%.1f kg | **%.2f**" % (m, m / 130.0) if d != 85
                  else "%.1f kg | %.2f" % (m, m / 130.0),
                  "actuator mass and f_act at %d Nm/kg" % d))
    c.append(("f_act band", "spec/02-structure-and-motion.md",
              "80–90 Nm/kg maps onto `f_act` %.2f–%.2f" % (total_nm / 90 / 130.0, total_nm / 80 / 130.0),
              "the density band and the f_act band, stated as one constraint"))

    # 02.7 both operating points, derived here rather than transcribed
    for t in (2, 4):
        g = growth_factor(sigma_f(0.30, 0.30, 20, t, 450))
        m = g * 28.8                       # mid of the m_ext range of 02.5
        kwh = m * battery_fraction(20, t, 450) * 450 / 1000.0
        c.append(("body t%dh" % t, "spec/02-structure-and-motion.md",
                  "~%d kg" % round(m), "body mass at the %d h point" % t))
        c.append(("pack t%dh" % t, "spec/02-structure-and-motion.md",
                  "%.1f kWh" % kwh, "pack size at the %d h point" % t))
        c.append(("actuators t%dh" % t, "spec/02-structure-and-motion.md",
                  "%d–%d kW" % (round(m * 0.30 * 3), round(m * 0.30 * 5)),
                  "actuator power band at the %d h point" % t))
        for cr in (3, 5, 10):
            c.append(("source t%dh %dC" % (t, cr), "spec/02-structure-and-motion.md",
                      "%d kW" % round(source_peak_kw(kwh, cr)),
                      "source peak at the %d h point, %dC" % (t, cr)))

    # 03.6 self-discharge and sleep, on the pack figure 02.7 quotes
    PACK = 10.4
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
    ap.add_argument("--f-act", type=float, default=0.30, help="actuator mass fraction")
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

    b = budget(a.f_str, a.f_act, a.p, a.endurance, a.e,
               a.coverage, a.areal, a.m_fixed, a.kw_per_kg, a.c_rate)
    if a.json:
        print(json.dumps(b, indent=2))
    else:
        print_report(b)
    return 0 if b["converges"] else 2


if __name__ == "__main__":
    sys.exit(main())
