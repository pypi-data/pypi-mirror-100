## Project Description

Decision support systems are used in industry, to assist users in making decisions.
Many methods are used in decision making, one of which is the Analytical Hierarchy Process (AHP). In this method, several layers can be used in decision making. This package has been designed to solve the AHP method with several layers.

### Depedencies
* Python >= 3
* numpy

### How to use
* run(layers)

### Parameters
**layers** : iterable, array, np.array

> The structure of your AHP model (single layer or multi layer).

### Example structure
* Goal
* Layer 1
  * Node 1
  * Node 2
  * Node 3
 * Layer 2
   * Node 1
   * Node 2
 * Alternatives Layer
	 * Alternative 1
	 * Alternative 2
	 * Alternative 3
	 * Alternative 4
### Example of code
```
from stahp import stahp

print(stahp.run(
[
    [
        [1, .3, 5],
        [3, 1, 5],
        [.2, .2, 1]
    ],
    [
        [
            [1, .2],
            [5, 1]
        ],
        [
            [1, 3],
            [.3, 1]
        ],
        [
            [1, 4],
            [.25, 1]
        ]
    ],
    [
        [
            [1, 3, .25, 7],
            [.3, 1, .25, 7],
            [4, 4, 1, 9],
            [.14, .14, .11, 1]
        ],


        [
            [1, 3, .25, 7],
            [.3, 1, .25, 7],
            [4, 4, 1, 9],
            [.14, .14, .11, 1]
        ]
    ]
]
))
```

## Example of output
```
[0.2502 0.1562 0.5556 0.038 ] #alternative 3 is the best choice
```