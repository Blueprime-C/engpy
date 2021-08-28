from copy import copy
alpha = ['F', 'a', 'b', 'c', 'd',
         'e', 'f', 'g', 'h', 'i',
         'j', 'k', 'l', 'm', 'n',
         'o', 'p', 'q', 'r', 's',
         't', 'u', 'v', 'w', 'x',
         'y', 'z', 'ȩ', 'î', 'ĵ',
         'ǩ']
_alpha = [alphas.upper() for alphas in alpha] + ['ȩ', 'î', 'ĵ', 'ǩ']

for alphas in copy(alpha):
    alpha.append(alphas.upper())
     
chars = alpha + ['*','+','-',' ','.','/','^','(',')','1','2','3','4','5','6','7',
                 '8','9','0','}','{',':','"',"'",',']
greeks = [chr(i) for i in range(913,970)]
greek_eng_Upper = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon',
             'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lamda',
             'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Space',
             'Sigma1', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']
greek_eng_Lower = [case.lower() for case in greek_eng_Upper if case != 'Space']
del greek_eng_Upper[18]
greek_eng_misc = ['CHi', 'CWye', 'CAlpha', 'CEpsilon',
                  'CNu', 'Cohi', 'CUpsilon']
alpha_greek = alpha + greeks

greek_map = dict(zip(greek_eng_Upper + greek_eng_misc + greek_eng_Lower,
                     greeks)
                 )
constants = {chr(960): 3.141592653589793,
             chr(553) : 2.718281828459045}

