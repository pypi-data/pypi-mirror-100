# sambal

sambal provides functions to

- uniformly sample a sphere
- uniformly sample a spherical cap of a sphere

# Usage

## Random vector on sphere

Generate a random vector on a 100-dimensional unit sphere.
```python
import numpy as np
from sambal import random_on_sphere

dim = 100
print(random_on_sphere(dim))
```

The same as above, but with a random number generator seeded to 0.
```python
import numpy as np
from sambal import random_on_sphere

dim = 100
rng = np.random.default_rng(0)
print(random_on_sphere(dim, rng))
```

## Random vector on spherical cap

Generate a 100-dimensional random vector on a spherical cap whose
central axis is `[1, 1, 1, ..., 1] / sqrt(100)` and whose maximum
planar angle is `pi/3`.
```python
import numpy as np
from sambal import random_on_cap

dim = 100
axis = np.ones(dim)
axis = axis / np.linalg.norm(axis)
max_planar_angle = np.pi/3
print(random_on_cap(axis, max_planar_angle))
```

The same as above, but with a random number generator seeded to 0.
```python
import numpy as np
from sambal import random_on_cap

rng = np.random.default_rng(0)
dim = 100
axis = np.ones(dim)
axis = axis / np.linalg.norm(axis)
max_planar_angle = np.pi/3
print(random_on_cap(axis, max_planar_angle, rng))
```

# Citing

If you use this code for your research, please cite the paper [An O(n)
algorithm for generating uniform random vectors in n-dimensional
cones](https://arxiv.org/abs/2101.00936).

# License

sambal is free software released under the terms of the [GNU General
Public License](https://www.gnu.org/licenses/gpl.html), either version
3 of the License, or (at your option) any later version.
