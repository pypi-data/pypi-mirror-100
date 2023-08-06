* EQUIVALENT CIRCUIT FOR VECTOR FITTED S-MATRIX
* Created using scikit-rf vectorFitting.py
*
.SUBCKT s_equivalent p1 p2 
*
* port 1
R1 a1 0 (50+0j)
V1 p1 a1 0
H1 nt1 nts1 V1 (50+0j)
E1 nts1 0 p1 0 1
* transfer network for s11
F11 0 a1 V11 (0.02+0j)
F11_inv a1 0 V11_inv (0.02+0j)
V11 nt1 nt11 0
V11_inv nt1 nt11_inv 0
* transfer admittances for S11
R11 nt11_inv 0 1.013
C11 nt11_inv 0 2.065f
X1 nt11 0 rcl_vccs_admittance res=1.112 cap=484.353f ind=7.124p gm=4.367m mult=-1
* transfer network for s12
F12 0 a1 V12 (0.02+0j)
F12_inv a1 0 V12_inv (0.02+0j)
V12 nt2 nt12 0
V12_inv nt2 nt12_inv 0
* transfer admittances for S12
R12 nt12_inv 0 16.546
C12 nt12_inv 0 24.502f
X2 nt12 0 rcl_vccs_admittance res=983.786m cap=547.591f ind=6.301p gm=59.451m mult=1
*
* port 2
R2 a2 0 (50+0j)
V2 p2 a2 0
H2 nt2 nts2 V2 (50+0j)
E2 nts2 0 p2 0 1
* transfer network for s21
F21 0 a2 V21 (0.02+0j)
F21_inv a2 0 V21_inv (0.02+0j)
V21 nt1 nt21 0
V21_inv nt1 nt21_inv 0
* transfer admittances for S21
R21 nt21_inv 0 16.546
C21 nt21_inv 0 24.502f
X3 nt21 0 rcl_vccs_admittance res=983.786m cap=547.591f ind=6.301p gm=59.451m mult=1
* transfer network for s22
F22 0 a2 V22 (0.02+0j)
F22_inv a2 0 V22_inv (0.02+0j)
V22 nt2 nt22 0
V22_inv nt2 nt22_inv 0
* transfer admittances for S22
R22 nt22_inv 0 1.006
C22 nt22 0 779.745f
X4 nt22 0 rcl_vccs_admittance res=952.277m cap=565.709f ind=6.100p gm=122.043m mult=1
.ENDS s_equivalent
*
.SUBCKT rcl_vccs_admittance n_pos n_neg res=1k cap=1n ind=100p gm=1m mult=1
L1 n_pos 1 {ind}
C1 1 2 {cap}
R1 2 n_neg {res}
G1 n_pos n_neg 1 2 {gm} m={mult}
.ENDS rcl_admittance
*
.SUBCKT rl_admittance n_pos n_neg res=1k ind=100p
L1 n_pos 1 {ind}
R1 1 n_neg {res}
.ENDS rl_admittance
