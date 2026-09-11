---
title: Optional CubeDynamics Extension
---

# Want to Go Further with CubeDynamics?

CubeDynamics is an optional extension for teams working with labeled multidimensional arrays. It is not required for a successful Hackathon project, and teams should keep the scientific question ahead of the software.

## Current installation status

As of September 2026, the [official CubeDynamics repository](https://github.com/CU-ESIIL/cubedynamics) describes version `0.1.0rc1` as alpha software preparing its first release candidate. There is **no public PyPI package or GitHub Release installation**. The supported event route is a mentor-maintained, checksum-verified wheel or environment supplied by facilitators.

Do not ask participants to guess an installation command, install an unverified artifact, or spend the short build window debugging a prerelease package. If the verified setup is unavailable, use `xarray`, the OLC notebooks, or another familiar tool and document the analytical logic.

## When it may help

CubeDynamics may be useful when a team wants to make an operation over named dimensions explicit and inspectable—for example, averaging a time dimension in a gridded climate cube. The OLC Technical Extender notebooks remain the event-specific starting point.

Official example shape:

```python
import matplotlib.pyplot as plt
import xarray as xr
from cubedynamics import pipe, verbs as v

with xr.open_dataset(
    "tests/fixtures/real_data/prism_boulder_january_2024.nc",
    engine="scipy",
) as observations:
    cube = observations["tmax"].load()

result = pipe(cube) | v.mean(over="time", keep_dim=False)
result.unwrap().plot()
plt.show()
```

This exact snippet depends on the repository’s example fixture and a verified CubeDynamics environment. It is an orientation example, not a participant installation test.

## Useful entry points

- [CubeDynamics repository and current status](https://github.com/CU-ESIIL/cubedynamics)
- [CubeDynamics documentation](https://cu-esiil.github.io/cubedynamics/)
- [CubeDynamics vignettes](https://cu-esiil.github.io/cubedynamics/vignettes/)
- [OLC 2026 Buildathon materials](https://github.com/olc-techsupport/Education-Climate-Resiliency-Digital-Sovereignty/tree/main/2026%20Buildathon)
- [Prepared OLC public datasets](https://github.com/olc-techsupport/Education-Climate-Resiliency-Digital-Sovereignty/tree/main/2026%20Buildathon/data)

If using CubeDynamics, record the exact artifact or environment supplied by facilitators, its checksum or version, the input data, the operation performed, and an equivalent plain-language description.
