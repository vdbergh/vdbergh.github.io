from __future__ import division

import math,argparse

"""
This program computes passing probabilities and expected running times for SPRT tests.
See http://hardy.uhasselt.be/Fishtest/sprta.pdf for more information.
"""

nelo_divided_by_nt=800/math.log(10)

def L(x):
    return 1/(1+10**(-x/400))

def PT(LA,LB,h):
    """ Universal functions """
    if abs(h*(LA-LB))<1e-6:
        # avoid division by zero
        P=-LA/(LB-LA)
        T=-LA*LB
    else:
        exp_a=math.exp(-h*LA)
        exp_b=math.exp(-h*LB)
        P=(1-exp_a)/(exp_b-exp_a)
    T=(2/h)*(LB*P+LA*(1-P))
    return P,T

class SPRT:

    def __init__(self,alpha=0.05,beta=0.05,elo0=0,elo1=5,draw_ratio=0.6,RMSbias=0.0,elo_model='logistic'):
        assert elo_model in ('logistic','normalized')
        self.LA=math.log(beta/(1-alpha))
        self.LB=math.log((1-beta)/alpha)
        RMSbias_score=L(RMSbias)-0.5
        variance3=(1-draw_ratio)/4.0
        variance=variance3-RMSbias_score**2
        sigma=math.sqrt(variance)
        if elo_model=='logistic':
            self.score0,self.score1=[L(elo) for elo in (elo0,elo1)]
        else:   # assume normalized
            self.score0,self.score1=[(elo/nelo_divided_by_nt)*sigma+0.5 for elo in (elo0,elo1)]
 
        self.w2=(self.score1-self.score0)**2/variance

    def characteristics(self,elo): # currently elo is always logistic
        score=L(elo)
        h=(2*score-(self.score0+self.score1))/(self.score1-self.score0)
        P,T=PT(self.LA,self.LB,h)
        return P,T/self.w2
        
if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha",help="probability of a false positve",type=float,default=0.05)
    parser.add_argument("--beta" ,help="probability of a false negative",type=float,default=0.05) 
    parser.add_argument("--elo0", help="H0 expressed in Elo",type=float,default=0.0)
    parser.add_argument("--elo1", help="H1 expressed in Elo",type=float,default=5.0)
    parser.add_argument("--elo", help="True Elo value (logistic)",type=float,default=5.0)
    parser.add_argument("--draw_ratio", help="draw ratio",type=float,default=0.7)
    parser.add_argument("--bias", help="Root Mean Square bias",type=float,default=0.0)
    parser.add_argument(
        "--elo-model",
        help="logistic or normalized",
        choices=['logistic', 'normalized'],
        default='logistic',
    )
    
    args=parser.parse_args()

    elo0=args.elo0
    elo1=args.elo1
    elo=args.elo
    draw_ratio=args.draw_ratio
    RMSbias=args.bias
    alpha=args.alpha
    beta=args.beta
    elo_model=args.elo_model

    print("elo0           = %.2f" % elo0)
    print("elo1           = %.2f" % elo1)
    print("elo (logistic) = %.2f" % elo)
    print("draw_ratio     = %.2f" % draw_ratio)
    print("RMSbias        = %.2f" % RMSbias)
    print("alpha          = %.2f" % alpha)
    print("beta           = %.2f" % beta)
    print("elo_model      = %s"   % elo_model)

    s=SPRT(alpha,beta,elo0,elo1,draw_ratio,RMSbias,elo_model)
    (power,expected)=s.characteristics(elo)

    print("pass probability:      %4.2f%%" % (100*power))
    print("avg running time: %10.0f" % expected)

    
