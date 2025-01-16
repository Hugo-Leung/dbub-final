# Improved measurement of flavor asymmetry of the light-quark sea in the proton with Drell-Yan production in p+p and p+d collisions at 120 GeV
To compile, simply use 

```
latexmk 
```

the output files would be written to the `build` directory


## file structure
Figures should be placed under `figures` directory

## comments
Comments in the tex files are handled by [todonotes](https://tug.ctan.org/macros/latex/contrib/todonotes/todonotes.pdf). To add a comment, please use

```
\todo[author={name}]{comment}
```

The background color can also specified by using the `color=` option.

To denote a missing figure, one can use the following 

```
\missingfigure{description of the figure}
```

All the comments would be hidden if the option `final` is enabled in the document class
