
### Research Overview
This repository corresponds to, "Yield Gap Analysis for Rainfed Grain Sorghum in Kansas." This article addressed the research questions: 1) are grain sorghum yields stagnating in the state of Kansas due to a small exploitable yield gap and 2) what are the environmental and management conditions of the sorghum-based crop rotation? 

### Repository Overview
There are four scripts in this repository:

1) "Yc_Ya.ipynb" is a script providing an example of calculating current yield (Yc), maximum attainable yield (Ya), and growing season rainfall (GSR) for the central crop reporting district in Kansas.
2) "Yw.ipynb" is a script calculating the temporal trend of water limited yield potential (Yw), Ya, and Yc for the central crop reporting district in Kansas.
3) "get_GSR_RET.py" is a script to calculate county level growing season rainfall and reference ET for each county in Kansas in the sorghum growing season. 
4) "yg_functions.py" is a script that has functions to determine 1) CB_Percentile_Mode: the cobb-douglas frontier production used to determine Yw and Ya; 2) Yw_Obs: a function to identify the maximum yield observation at each precipitation bin interval; and 3) TE_MWL: the transpiration efficiency of grain yield relative to water input and minimum water losses.  

### Citation
Sexton‐Bowser, S., & Patrignani, A. (2024). Yield gap analysis for rainfed grain sorghum in Kansas. Agronomy Journal. https://doi.org/10.1002/agj2.21684

