# Counting winning rummikub hands
Counts winning rummikub hands using either a top down approach or a bottom up approach using Frank Takes `frank.cc` which determines if a given hand is winning.

## Top down
To run use:
```
./rummi_generator 1 2 3 4 5 6
```

1. The minimal hand to start from
2. The maximal hand to end with
3. Number of stones (n)
4. Number of colors (k)
5. Number of copies (c)
6. Number of cores to be used

You can also run the program without parameters: 
```
./rummi_generator
```
In that case the default parameters will be used; `3-10, 13 stones, 4 colors, 2 copies, 4 cores`.

## Bottom up
To run use:
```
./rummi_reverse 1 2 3 4
```

1. The maximal hand to start from
2. The minimal hand to end with
3. Number of stones (n)
4. Number of cores to be used