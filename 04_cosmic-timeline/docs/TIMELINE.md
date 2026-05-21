# Timeline Eras (TL Keyframes)

The timeline maps `animT` (0→1) to 13.8 billion years of cosmic history.

## Keyframe Table

| aT    | Age (Gyr)  | Era Name         | Camera R | Background | Fog    |
|-------|------------|------------------|----------|------------|--------|
| 0.000 | 1e-30      | Big Bang         | 180      | 0x180713   | 0.016  |
| 0.050 | 1e-15      | Particle Era     | 165      | 0x0D0305   | 0.013  |
| 0.100 | 1e-11      | Nucleosynthesis  | 150      | 0x0A0305   | 0.010  |
| 0.160 | 0.00038    | CMB Released     | 130      | 0x060309   | 0.008  |
| 0.220 | 0.003      | Dark Ages        | 112      | 0x020308   | 0.006  |
| 0.300 | 0.2        | First Stars      | 85       | 0x010309   | 0.005  |
| 0.400 | 0.4        | First Galaxies   | 272      | 0x010209   | 0.004  |
| 0.430 | 0.7        | Quasar Era       | 144      | 0x010209   | 0.004  |
| 0.500 | 1.5        | Galaxy Web       | 352      | 0x010208   | 0.004  |
| 0.570 | 5.8        | Milky Way        | 288      | 0x010209   | 0.004  |
| 0.640 | 9.2        | Solar System     | 25       | 0x01030A   | 0.005  |
| 0.700 | 10.0       | Early Life       | 10       | 0x010A0C   | 0.007  |
| 0.930 | 13.56      | Recent Stars     | 12       | 0x010408   | 0.006  |
| 0.990 | 13.799     | Now — 1000yr     | 6        | 0x01070C   | 0.009  |
| 1.000 | 13.8       | Present Day      | 6        | 0x01070C   | 0.010  |

## Scene Group Timing

All scenes persist to `aT=1.01` (nothing disappears).

| Scene       | Start | Peak | Fade | End  | Description |
|-------------|-------|------|------|------|-------------|
| bigbang     | 0.00  | 0.02 | 0.20 | 1.01 | Explosion particles |
| particles   | 0.04  | 0.08 | 0.25 | 1.01 | QGP → protons → atoms |
| darkages    | 0.18  | 0.22 | 0.30 | 1.01 | Cold neutral gas + DM halos |
| firststars  | 0.22  | 0.30 | 0.50 | 1.01 | Pop III stars + supernovae |
| starfield   | 0.28  | 0.34 | 0.95 | 1.01 | 15,000 background stars |
| protogal    | 0.36  | 0.42 | 0.60 | 1.01 | 8 proto-galaxy clumps |
| compact     | 0.28  | 0.35 | 0.55 | 1.01 | Pulsar + stellar BH |
| quasar      | 0.35  | 0.41 | 0.48 | 1.01 | BH + accretion disk + jets |
| galaxyweb   | 0.46  | 0.54 | 0.92 | 1.01 | MW + 12 local group galaxies |
| solarsystem | 0.60  | 0.64 | 0.92 | 1.01 | Sun + 8 planets + belts |
| pillars     | 0.88  | 0.92 | 0.97 | 1.01 | Eagle Nebula particle columns |
| now         | 0.95  | 0.97 | 1.00 | 1.01 | Local stars + constellation lines |
