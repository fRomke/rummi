# rummi
Counting winning rummikub hands

To run use:
./rummi_generator


Fill out the functions in main() to count the winning hands

Options include:

-print(rummi.callRecCount(t, n_stones, k_colors, m_copies))

Returns the amount of winning hands for size t.


-perfListWinnings(minhand, maxhand, n_stones, k_colors, m_copies)

Generates a list for each hand between minhand and maxhand in parallel using multiple cores.


-listWinnings(minhand, maxhand, n_stones, k_colors, m_copies)

Generates a list for each hand between minhand and maxhand sequentially using a single core.
