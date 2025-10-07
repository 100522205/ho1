#
# PARTE 2.1
#
# 
#

/* sets */
set ORIG;
set DEST;

/* parameters */
param DISP      {ORIG};
param DEMANDA   {DEST};
param COST      {DEST};
param Cant      {ORIG, DEST};

/* decision variables */
var x           {ORIG, DEST} >= 0, integer;

/* objective function */
minimize z:
    sum{i in ORIG, j in DEST} x[i, j]*COST[i, j];

/* Constraints */
s.t. Availability{i in ORIG}:
    sum{j in DEST} x[i, j]<=DISP[i];
s.t. Constraint2 : 
    sum{i in VARIANTS} x[i] <= Prod;

end;
