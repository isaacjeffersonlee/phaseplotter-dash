# Phase Plotter Dash Web App

### Author: Isaac Lee

## The App
https://phase.herokuapp.com/

## Summary
A little Dash web app to plot the phase portrait of a 2D system.

## Input
Input the *expanded* system, using a semi-colon
to denote the divide between rows. I.e if we have:    

\[x', y'\]^T = A\[x, y\]^T + \[g1(x,y), g2(x,y)\]^T 
     
Then our input would be:
a11\*x + a12\*y + g1(x,y); a21\*x + a22\*y + g2(x,y)  

Where g1(x,y) and g2(x,y) are expressions that can be 
interpreted by python, e.g (1/5) \* x\*\*2 or cos(x) e.t.c
