# Database Systems - Assignment 2

## Part 1 - B+ Tree

Basic Implementation of B+ Tree of general order in `python3`, which can be run using the following command:

```console
python3 part1.py <filepath>
```

Each line of file should contain a query. The following types of queries are supported:

1. INSERT x - Inserts x into the B+ tree
2. FIND x - Prints YES if x is already inserted, else NO
3. COUNT x - Prints number of occurrences of x in B+ tree
4. RANGE x y - Prints number of elements in range x to y (both x and y included)

Here, -10<sup>9</sup> <= x, y <= 10<sup>9</sup>.

## Part 2 - Linear Hashing

Implementation of linear hashing algorithm described [here](https://hackthology.com/pdfs/Litwin-1980-Linear_Hashing.pdf) in `python3`, explained in class, to handle duplicate elimination.

```console
python3 part2.py <filepath>
```

Each line of input file should contain an integer x, x is printed if it was not inserted before in the hashtable. Here, -10<sup>9</sup> <= x <= 10<sup>9</sup>.
