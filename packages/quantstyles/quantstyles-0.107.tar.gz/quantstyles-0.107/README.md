# Quantstyles

A set of slightly customized colormaps and styles, developed for internal use by Quantum Technology research group in the University of Rostock.

<img src="https://raw.githubusercontent.com/Trel725/quantstyles/master/quantstyles/quant_cmaps.png" width="60%" style="@media (max-width: 1080px) {width=100%}">

It includes the set of colormaps + custom matplotlib style.

<img src="https://raw.githubusercontent.com/Trel725/quantstyles/master/img/demo.png" width="90%" style="@media (max-width: 1080px) {width=100%}">

## Usage

Import the package in your script  
`import quantstyles`  
Package automatically exports all the colormaps, i.e. they could be normally used by their names, e.g.   
`plt.show(data, cmap="quantjet")`  
Custom matplotlib style will be registered during first import of the package. It can be then activated as   
`plt.style.use("quant")`

## Installation
The package is published on pypi, so it is enough to run:
```
pip install quantstyles
```

## Manual installation
``` bash
# clone the repo
git clone https://github.com/Trel725/quantstyles.git --recursive

# build the wheel
make

# manually install the built package
pip install dist/quantstyles-*-py3-none-any.whl

```

## Acknoledgements
This project depends on
- [Beautiful package for generating perceptually uniform colormaps](https://github.com/peterkovesi/PerceptualColourMaps.jl) by Peter Kovesi. The heart of this small project is just a small modification of original Julia code.  
- get-cpt script that allows efficient export of generated colormaps to Python.  

## Development
If you'd like to manually go through all the steps:  
1. Clone the repo by `git clone https://github.com/Trel725/quantstyles.git --recursive` Recursive is needed to sync get-cpt repo.
2. Generate colormaps by executing Julia code in colormaps folder  
```
cd colormaps
julia colormaps.jl
```
PerceptualColourMaps.jl and PyPlot.jl need to be installed. See that code for more details, or just use pre-generated colormaps in the colormaps directory.  
3. Generate Python representation of the colormaps by running `python generate_quantcmaps.py`. This will produce actual file containing colormaps, quantcmaps.py  The command requires numpy, os, glob and (probably) urllib (from get-cpt).
4. Import quantcmaps in your script. All the listed colormaps will be available as usual, e.g. `plt.imshow(data, cmap="quantjet")`  
5. Custom style need to be copied to the matplotlib config dir. See [official manuals](https://matplotlib.org/stable/tutorials/introductory/customizing.html) for details.  
6. Additionally you can try to build pip wheel by executing `make` in the project top directory.
