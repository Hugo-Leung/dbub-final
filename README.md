# Final SeaQuest results on the flavor asymmetry of the proton light-quark sea with proton-induced Drell-Yan process

The Fermilab E906/SeaQuest collaboration performed measurements of the Drell-Yan process using 120 GeV proton beams bombarding liquid hydrogen and liquid deuterium targets. A combined analysis of all collected data was performed to obtain the final results for the $\sigma_{pd}/2\sigma_{pp}$ Drell-Yan cross section ratio covering the kinematic region of $0.13 < x < 0.45$. The $x$-dependencies of $\bar{d}\left(x\right) / \bar{u}\left(x\right)$ and $\bar{d}\left(x\right) - \bar{u}\left(x\right)$ are extracted from these cross section ratios. It is found that $\bar{d}\left(x\right)$ is greater than $\bar{u}\left(x\right)$ over the entire measured $x$ range, with improved statistical accuracy compared to previous measurements. The new results on $\bar{d}\left(x\right) / \bar{u}\left(x\right)$ and $\bar{d}\left(x\right) - \bar{u}\left(x\right)$ are compared to various parton distribution functions and theoretical calculations.

---
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
