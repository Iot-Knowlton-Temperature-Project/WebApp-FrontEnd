# Data Analysis (datadump.txt)

Generated from `datadump.txt` on 2026-03-04 using `analyze_datadump.py`.

## Dataset overview

- Rows parsed: **37,560**
- Sensors: **1–5** (roughly **7.5k** rows per sensor)
- Time range: **2026-03-03 11:10:49 → 2026-03-04 09:43:16** (**22:32:27**)
- Sampling: **~11s median** per sensor, **no gaps > 60s** (max gap seen: **45s** on sensor 3)
- Humidity validity: **0 rows outside [0, 100]**

## Overall stats

- Temperature: mean **71.10**, sd **1.88**, min **65.68**, median **71.20**, max **74.54**
- Humidity: mean **31.31**, sd **2.17**, min **23.97**, median **31.24**, max **37.25**

## Per-sensor baseline (mean)

- Sensor 4: **warmest** (temp mean **73.40**), humidity mean **29.55**
- Sensor 5: **coolest** (temp mean **68.11**), humidity mean **31.91**
- Sensor 2: **most humid on average** (humidity mean **33.20**)

## Relationships (temp vs humidity)

Pearson correlation by sensor:

- Sensor 2: **-0.504** (temp up ↔ humidity down)
- Sensor 1: **+0.386**
- Sensor 3: **+0.345**
- Sensor 4: **+0.347**
- Sensor 5: **+0.103** (weak relationship)

Interpretation: sensors 1/3/4 show moderate positive coupling (could indicate shared environmental shifts); sensor 2 behaves more like the typical inverse temp/humidity relationship.

## Notable anomalies / outliers

3σ outlier counts (rough, distribution-dependent):

- Sensor 5 humidity: **224** outliers
- Sensor 3 temperature: **6** outliers
- Sensor 4 humidity: **5** outliers
- Sensor 1 humidity: **10** outliers

### Outlier “events” (contiguous segments)

Computed by grouping consecutive 3σ outliers (same direction: high vs low) if separated by ≤30 seconds.

- Sensor 5 humidity (low): **2026-03-03 11:12:01 → 2026-03-03 11:51:33**
  - Duration: **~39m 32s**, points: **224**, range: **23.97–25.75%**
  - Interpretation: strong **startup/stabilization** behavior (very unlikely to be random noise).
- Sensor 4 humidity (high): **2026-03-04 00:32:12 → 2026-03-04 00:32:56**
  - Duration: **~44s**, points: **5**, range: **35.53–37.25%**
  - Interpretation: short, discrete humidity spike/event.
- Sensor 3 temperature (high): **2026-03-03 11:13:03 → 2026-03-03 11:13:56**
  - Duration: **~53s**, points: **6**, range: **71.87–72.44°F**
  - Interpretation: startup transient.
- Sensor 1 humidity (low): **2026-03-03 11:11:52 → 2026-03-03 11:13:27**
  - Duration: **~95s**, points: **10**, range: **25.09–25.26%**
  - Interpretation: brief early transient.

## Suggested next steps (if this feeds a dashboard/model)

- Consider **dropping the first few minutes** of data for sensors 3 and 5 (startup stabilization).
- If comparing sensors, consider **baseline normalization** (sensor 4 is consistently warmer; sensor 5 is consistently cooler).
- If alerting on humidity, treat **sensor 5 low-humidity burst** and **sensor 4 midnight spike** as distinct events to validate.

## Reproduce

Run:

```bash
C:/Users/brick/AppData/Local/Programs/Python/Python313/python.exe analyze_datadump.py
```
