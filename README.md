# Final SeaQuest results on the flavor asymmetry of the proton light-quark sea with proton-induced Drell-Yan process
To compile, simply use 

```
latexmk 
```

the output files would be written to the `build` directory


## file structure
Figures should be placed under `figures` directory. The tex files under `tables` are generate by root scripts and can be hard to read.

## comments
Comments to the paper are handled by [todonotes](https://tug.ctan.org/macros/latex/contrib/todonotes/todonotes.pdf). To add a comment, please use

```
\todo[author={name}]{comment}
```

The background color can also specified by using the `color=` option.

To denote a missing figure, one can use the following 

```
\missingfigure{description of the figure}
```

All the comments will be hidden if the option `final` is specified in the document class
