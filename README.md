# Genetic Algorithm for 2D Guillotine Cutting Optimization

This program uses a genetic algorithm to find an optimal layout for a set of rectangular items on a 2D sheet. It loads item data from a CSV file, runs a genetic algorithm to find the best layout, and then visualizes the layout using a plot.

## Requirements

- Python 3.x
- Matplotlib

## Installation

To install the required libraries, you can use the following command:

```bash
pip install matplotlib
```

## Usage

To run the program, you will need to provide the path to the CSV file containing the item data. You can do this by running the following command:

```bash
python main.py items.csv
```

This will load the item data from the CSV file, run the genetic algorithm, and then visualize the best layout.

## Example CSV File

```
id,width,height
item1,10,5
item2,12,3
item3,8,7
```

## Output

The program will print the best individual and its fitness (total area needed) to the console. It will also create a plot of the best layout.

## References

- Toshihiko Ono's paper "Optimizing Two-dimensional Guillotine Cut by Genetic Algorithms"
  http://ono-t.d.dooo.jp/GA/GA-papers/TO-110.pdf
