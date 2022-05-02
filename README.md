# EngPy

EngPy, Python for Engineers; Python for Engineering, a free and open-source Python library for Engineering computations.

EngPy is targeted at handling most engineering problems like calculus, transforms, graphs, complex algebraic expressions, Matrices manipulation, vector analysis, analyzing signals.

The library consists of three major datatypes:

## 1. Expr
This is the core datatype of EngPy. Most other parts of the library are based on this class.
It is responsible for any algebraic manipulations.

1.  Simple Algebra: Addition, Subtraction, Multiplication, Division Substitution of Expressions; change of subject of formula, clear brackets, and fractions.
2.  Calculus: linear and partial differentiation, integration, gradient
3.  Trigonometry
4.  logarithmic Expressions
5.  Transforms: Laplace, Z-Transforms
6.  Visualization: Graphs
7.  Table of Values
8.  Complex Number Manipulation
9.  Solving Expressions
10. Support the engpy AI Implementation for manipulating expressions

`Expr` can be imported from `engpy`:

```python
>>> from engpy import Expr
```

See the doc file or `Expr`'s documentation.

To interact with `Expr` instances as discrete objects, use the `engpy.interface` module.
The `interface` module bridges between the `Expr` class and `Expr` datatypes.

For example, the expression `2xcos3(2θ) - 7y^2sin(2ω) - ln(sqrt(z +3)); s = y - cos(5z)` can be passed directly as a string into the `Expr` constructor:
```python
>>> from engpy import Expr
>>> w = Expr('2xcos3(2theta) - 7y^2sin(2omega) - ln(sqrt(z +3)); s = y - cos(5z)')
>>> s = w - 'cos(5z)'
>>> w
2xcos3(2θ) - 7y^2sin(2ω) - ln(sqrt(z + 3))
>>> s
2xcos3(2θ) - 7y^2sin(2ω) - ln(sqrt(z + 3)) - cos(5z)
```

OR, in discrete form
```python
>>> from interface import *
>>> o,x,t,y,z = Var('omega', 'x', 'theta','y','z')
>>> w = 2*x*cos(2*t)**3 - 7*y**2*sin(2*o) - ln(sqrt(z + 3))
>>> w
2xcos3(2θ) - 7y^2sin(2ω) - ln(sqrt(z + 3))
>>> s = w - cos(5*z)
>>> s
2xcos3(2θ) - 7y^2sin(2ω) - ln(sqrt(z + 3)) - cos(5z)
```

Note that to cast an `Expr` object to it's string representation, you can use:
- `str(expr)`: will return the expression in its simplest lowest form.
- `format(expr)`: will return the expression in its normal form.
- `repr(expr)`: will return the expression in the most readable form.

It's recommended to use `format()` or `repr()` as they faster than `str()`. Only use `str()` when necessary.

## 2. Matrix
This class handles all matrix operations and manipulations. It rests on the `Expr` Class.
Supported operations are:
1. Simple Matrix Algebra: Addition, Subtraction, Multiplication, Division
						  Substitution of Matrices
2. Determinant, Minors, Cofactors, Adjoin, transpose, rank
3. Reduction: echelon, canonical, triangular decomposition
4. Row and column Transformation operations
5. Decomposition: Triangular, Symmetric, hermitian decomposition
6. Matrix Geometry: eigenvalues, modal, spectral, nullspace
				   algebraic multiplicity, geometric multiplicity
				   of a Matrix
7. Differentiation
8. Solving and comparing Matrices

The matrix datatype comes in two implementations; classes `Matrix` and `Matrix_`.
Both can be imported from `engpy`:
```python
>>> from engpy import Matrix
# OR
>>> from engpy import Matrix_
```

See the Matrix\_doc file or EngPy Arrays documentation to learn its usage.

## 3. Vector
This datatype handles vector analysis and operations:
1. Simple Vector Algebra: Addition, Subtraction, Substitution, Modulus
						  of Vectors
2. Angles between Vectors
3. Multiplication of Vector: Dot, and scalar product
4. Vector Calculus: Differentiation and Integration
5. Vector Operations: Tangents, normals, grad, directional derivatives,
					  div, curl
6. Validating properties: solenoidal, irrotational, coplanar, orthogonality
7. Scalar, Vector Triple product

Vector Class can also be imported from `engpy`:
```python
>>> from engpy import Vector
```

**Note:** All these three datatypes work with python operators: `+`, `-`, `/`, `*`, `~` e.g `MatObj1 + MatObj2`.

