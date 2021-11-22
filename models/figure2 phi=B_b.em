s,a1,a2,b1,b2,c1,c2
a,b,c
a:(s<=a1),(a1<=a2),(a2<=a1)
b:(s<=b1),(b1<=b2),(b2<=b1)
c:(s<=c1),(c1<=c2),(c2<=c1)
a1:p
b1:p
c1:p

# Formula: (D_a (B_b p)) /\ (B_a (~(D_b (B_b p)))) /\ (B_a (~(D_c (B_b p)))) /\ (D_b (B_b p)) /\ (B_b (~(D_a (B_b p)))) /\ (B_b (~(D_c (B_b p)))) /\ (D_c (B_b p)) /\ (B_c (~(D_b (B_b p)))) /\ (B_c (~(D_a (B_b p))))