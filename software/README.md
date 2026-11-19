# Software

Code that runs under an operating system on the body's embedded computer — the edge AI module, under Linux — as [spec 07.1](../spec/07-firmware-and-software.md#71-the-division) defines software. Which of its tasks are hard, firm or soft real-time is not decided here but in [`../realtime_config/`](../realtime_config/).

| Module | What it is | Status |
|---|---|---|
| Capture drivers | Camera, thermal, LiDAR, microphone and SDR capture, timestamped on the shared time base (plan S-9) | 🔜 *waiting a target* |
| Feature extraction and compression | The ≥2:1 the link requires ([spec 05.4](../spec/05-sensing.md#54-aggregate-rate-against-the-link)) | 🔜 *waiting update* |
| Sensor fusion | Multi-rate, on a shared time base | 🔜 *waiting update* |
| Log assembly and synchronisation | Two tiers, synchronised off-board after an outage | 🔜 — port of [`../reference/audit_log.py`](../reference/audit_log.py) |
| Link management | Graceful degradation before dropped streams | 🔜 *waiting update* |

The binding of RSIL to these modules and to the real-time code, algorithm by algorithm — fieldbus masters, drivers, ROS 2, estimators, controllers, faculties — is [`RSIL-in-GEMs.md`](RSIL-in-GEMs.md).

No source yet. The executable specifications this code will be checked against are in [`../reference/`](../reference/). Planned work, module by module: [`../plan/software.md`](../plan/software.md).
