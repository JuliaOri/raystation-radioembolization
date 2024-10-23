## Total absorbed dose per voxel in Y-90 radioembolization using PET imaging
The average beta energy of the Yttrium-90 decay is 933.6 keV

$$\overline{E}_{Y-90}= 933.6 \text{keV}\cdot 1.6\cdot 10^{-16}\text{J/keV}$$

Taking $\Delta t$ as the timelapse between the Y-90 administration and image aquisition, the decay factot $F_d$ can be defined as

$$F_d=\frac{A_0}{A_t}=e^{t\cdot \frac{\ln 2}{T_{1/2}}}$$

where $T_{1/2}=64.1 \text{h}$ is the Y-90 half-life, $A_0$ is the administered initial activity and $A_t$ is the measured activity per voxel at the time of the aquisition.

The total absorbed dose per voxel will thus be

$$D=\frac{E_{\text{total, Y-90}}}{\rho}$$

where $\rho = 1.03\text{kg/l}$ is the liver's average density.

The total energy per voxel will be 
```math
E_{\text{total, Y-90}} =\overline{E}_{Y-90} \cdot N_0 = \overline{E}_{Y-90} \cdot A_0\cdot \frac{T_{1/2}}{\ln 2}
```

Finally, given that the total number of administered nuclei per voxel can be calculated as $N_0=A_0\cdot \frac{T_{1/2}}{\ln2}$, the total absorbed dose per voxel will be
```math
D $= \frac{\overbrace{E_{\text{total, Y-90}}}^{\overline{E}_{Y-90} \cdot A_0\cdot \frac{T_{1/2}}{\ln 2}}}{\rho}
$= \overline{E}_{Y-90} \cdot \underbrace{A_0}_{A_t\cdot F_d}\cdot \frac{T_{1/2}}{\ln 2} \cdot \frac{1}{\rho}=\overline{E}_{Y-90} \cdot A_t\cdot F_d\cdot \frac{T_{1/2}}{\ln 2} \cdot \frac{1}{\rho}=A_t\cdot\left[\overline{E}_{Y-90} \cdot  F_d\cdot \frac{T_{1/2}}{\ln 2} \cdot \frac{1}{\rho}\right]=A_t\cdot F_\text{cPET}
```

