This code is written 2014/2/10 for the PGM Assignment #1 (Bayesian Network).

The program is structured with three main classes:
    
CPT: It takes the observed data, and its "printCPT" method generates the conditional probability table for the parameter.The input to the method is pretty straightforward. 
    
                 CPTOBject.printCPT(A, [B,C]) // P(A|B, C)
    
The output is a hashmap that stores the table with (key: CPTInstance, value: Probability)
    
CPTInstance: This object is a key to the hashmap that CPT returned.
                 For all variables in the given CPT, specific values are given.
                 CPTInstance takes the variable Node objects with its value set.
                 Node objects are "copied" with its value from the generic given Node variables.

                 a_bc_map = CPTObject.printCPT(A, [B, C]) // P(A| B, C)

                 // P(A='1'|B='Low', C='High')
                 A_ = A.copy('1')
                 B_ = B.copy('Low')
                 C_ = C.copy('High')
                 a_bc_map[CPTInstance(A_, [B_, C_])
                 
   
 Node: It represents a random variable. It contains its possible values.
 This can be further implemented to consider the network structure by having "children" and "parents", though it wasn't necessary for the scope of this assignment.
