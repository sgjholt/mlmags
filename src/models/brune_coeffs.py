"""Brune model coefficients for P or S waves.
"""

BRUNE_COEFFS = {
                'P':{
                        'vel': 6000,
                        'rad_coef': 0.52, 
                        'FS': 2., 
                        'eta': 1, 
                        'rho': 2800, 
                        'ro': 1000,
                },
    
                'S':{
                        'vel': 3500, 
                        'rad_coef': 0.63, 
                        'FS': 2., 
                        'eta': 1., 
                        'rho': 2700., 
                        'ro': 1000.
                }
                }
