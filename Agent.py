
import numpy as np
from PIL import Image, ImageChops, ImageOps, ImageFilter, ImageDraw
from itertools import product
import pprint, logging
import math, operator
import sys
from concurrent import futures
from functools import partial
import argparse

######################################################################
class Agent:
######################################################################
    def __init__(self):
        pass

    def Solve(self,problem):
        
        global iptype 
        
        problem.answer = -1  # set the default answer to null
        # categorize problem figures
        given = ["A.png", "B.png", "C.png","D.png", "E.png", "F.png", "G.png", "H.png" ]
        choices = ["1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png"]
        fig_problem = []
        fig_choices = []
        for figure in sorted(problem.figures):
            fig = problem.figures[figure].visualFilename   
            if fig[-5:] in given:
                fig_problem.append(problem.figures[figure])
            elif fig[-5:] in choices:
                fig_choices.append(problem.figures[figure])

        # check problem type & initialize parameters
        if problem.problemType == "2x2":
            iptype = 2
            problem.answer = Solver.solve(self,fig_problem,fig_choices)
        elif problem.problemType == "3x3":
            iptype = 3
            problem.answer = Solver.solve(self,fig_problem,fig_choices)
        print(problem.answer)
        return problem.answer

######################################################################
class Solver:
######################################################################
    def __init__(self):
        pass

    def solve(self,fig_problem,fig_choices):
        sol = test.EQUAL(self,fig_problem,fig_choices)
        if sol != -1:  return sol
        sol = test.MIRROR(self,fig_problem,fig_choices)
        if sol != -1: return sol
        if iptype == 2: 
            sol = test.ROTATE(self,fig_problem,fig_choices)
            if sol != -1:  return sol
            sol = test.FILL(self,fig_problem,fig_choices)
            if sol != -1: return sol
        sol = test.add_sub(self,fig_problem,fig_choices)
        if sol != -1: return sol
        # print('cannot solve!')
        return -1


######################################################################
class test:
######################################################################       
    def __init__(self):
        
        pass


    def EQUAL(self,fig_problem,fig_choices):
        # print('equal')
        global iptype
        global tol
        tol = 0.999 
        if iptype == 2 :
            row = [0,2]; row1 = [1]; row2 = []; row3 = []
            col = [0,1]; col1 = [2]; col2 = []; col3 = []
            diag = [1]; diag1 = [2]; diag2 = []
        elif iptype == 3:
            row = [0,3,6]; row1 = [1,2]; row2 = [4,5]; row3 = [7]
            col = [0,1,2]; col1 = [3,6]; col2 = [4,7]; col3 = [5]
            diag = [0,2]; diag1 = [4]; diag2 = [4,6]

        ''' EQUAL -> all; row-wise; column-wise; diagonal'''
        # row-wise
        idx = 0
        test_row = []
        for figure in [fig_problem[count] for count in row]:
            x = figure.visualFilename
            idx += 1
            for fig in [fig_problem[ii] for ii in row1 if idx == 1]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_row.append(f[0])
            for fig in [fig_problem[ii] for ii in row2 if idx == 2]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_row.append(f[0])
            for fig in [fig_problem[ii] for ii in row3 if idx == 3]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_row.append(f[0])
        # column-wise                    
        idx = 0    
        test_col = []                
        for fig in [fig_problem[count] for count in col]:
            x = fig.visualFilename
            idx += 1
            for fig in [fig_problem[ii] for ii in col1 if idx == 1]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_col.append(f[0])
            for fig in [fig_problem[ii] for ii in col2 if idx == 2]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_col.append(f[0])
            for fig in [fig_problem[ii] for ii in col3 if idx == 3]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_col.append(f[0])
        # diagonal-wise                    
        idx = 0    
        test_diag = []                
        for figure in [fig_problem[ii] for ii in diag]:
            x = figure.visualFilename
            idx += 1
            for fig in [fig_problem[ii] for ii in diag1 if idx == 1]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_diag.append(f[0])
            for fig in [fig_problem[ii] for ii in diag2 if idx == 2]:
                y = fig.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_diag.append(f[0])
        # print(test_row,test_col,test_diag)
        probab = []    
        figID = []
        if all(test_col + test_row + test_diag) is True:     
            # all 
            x = fig_problem[0].visualFilename
            for figure in fig_choices:
                y = figure.visualFilename
                aux, p = op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1'))
                probab.append(p)
                figID.append(figure.visualFilename[-5:-4])
            imax = probab.index(max(probab))
            # print(probab)
            if max(probab) <= 0.999: return -1
            sol = int(figID[imax])
            return sol
        elif all(test_col) is True:
            # column-wise
            x = fig_problem[col[-1]].visualFilename
        elif all(test_row) is True:
            # row-wise
            x = fig_problem[row[-1]].visualFilename
        elif all(test_diag) is True:
            x = fig_problem[diag[0]].visualFilename
        else:
            return -1
        for figure in fig_choices:
            y = figure.visualFilename
            aux, p = op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1'))
            probab.append(p)
            figID.append(figure.visualFilename[-5:-4])
        imax = probab.index(max(probab))
        # print(probab)
        if max(probab) <= 0.999: return -1
        sol = int(figID[imax])
        return sol


    def MIRROR(self,fig_problem,fig_choices):
        # print('mirror')
        global iptype
        global tol

        tol = 0.9999
        if iptype == 2 :
            row = [0]; row1 = [1]; row2 = []
            col = [0]; col1 = [2]; col2 = []
            diag = [1]; diag1 = [2]; diag2 = []
            ii = 2
        elif iptype == 3:
            row = [0,3]; row1 = [2]; row2 = [5]  
            col = [0,1]; col1 = [6]; col2 = [7] 
            diag = [2]; diag1 = [6]
            ii = 3
        
        ''' MIRROR -> LEFT-RIGHT; TOP-BOTTOM -> column; row; diagonal ''' 
        # row-wise
        idx = 0
        test_row_lr = []
        test_row_tb = []
        for figure in [fig_problem[count] for count in row]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[ii] for ii in row1 if idx == 1]:
                y = figure.visualFilename
                yy = Image.open(y).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
                f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                test_row_lr.append(f[0])
                y = Image.open(y).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
                f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                test_row_tb.append(f[0])
            for figure in [fig_problem[ii] for ii in row2 if idx == 2]:
                y = figure.visualFilename
                yy = Image.open(y).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
                f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                test_row_lr.append(f[0])
                y = Image.open(y).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
                f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                test_row_tb.append(f[0])
        # column-wise
        idx = 0
        test_col_lr = []
        test_col_tb = []
        for figure in [fig_problem[count] for count in col]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[ii] for ii in col1 if idx==1]:
                y = figure.visualFilename
                yy = Image.open(y).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
                f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                test_col_lr.append(f[0])
                y = Image.open(y).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
                f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                test_col_tb.append(f[0])
            for figure in [fig_problem[x] for x in col2 if idx==2]:
                y = figure.visualFilename
                yy = Image.open(y).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
                f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                test_col_lr.append(f[0])
                y = Image.open(y).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
                f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                test_col_tb.append(f[0])
        # diagonal-wise
        idx = 0
        test_diag_lr = []
        test_diag_tb = []
        for figure in [fig_problem[count] for count in diag]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[ii] for ii in diag1 if idx == 1]:
                y = figure.visualFilename
                yy = Image.open(y).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
                f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                test_diag_lr.append(f[0])
                y = Image.open(y).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
                f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                test_diag_tb.append(f[0])
        # print(test_row_lr,test_col_lr,test_diag_lr)
        # print(test_row_tb,test_col_tb,test_diag_tb)
        probab = []
        figID = []
        if all(test_col_lr) is True:
            # column-wise
            x = fig_problem[col[-1]+ii-1].visualFilename
            x = Image.open(x).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
        elif all(test_row_lr) is True:
            # row-wise
            x = fig_problem[row[-1]+ii].visualFilename
            x = Image.open(x).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
        elif all(test_diag_lr) is True:
            x = fig_problem[diag[0]].visualFilename
            x = Image.open(x).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
        elif all(test_col_tb) is True:
            # column-wise
            x = fig_problem[col[-1]+ii-1].visualFilename
            x = Image.open(x).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
        elif all(test_row_tb) is True:
            # row-wise
            x = fig_problem[row[-1]+ii].visualFilename
            x = Image.open(x).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
        elif all(test_diag_tb) is True:
            x = fig_problem[diag[0]].visualFilename
            x = Image.open(x).convert('1').transpose(Image.FLIP_TOP_BOTTOM)            
        else:
            return -1
        for figure in fig_choices:
            y = figure.visualFilename
            aux, p = op.equal_AB( self,x,Image.open(y).convert('1'))
            probab.append(p)
            figID.append(figure.visualFilename[-5:-4])
        imax = probab.index(max(probab))
        if max(probab) <= tol: return -1
        sol = int(figID[imax])
        return sol


    def ROTATE(self,fig_problem,fig_choices):
        # print('rotate')
        global iptype
        global tol
        tol = 0.995
        if iptype == 2:
            row = [0]; row1 = [1]; 
            col = [0]; col1 = [2]; 
            diag = [1]; diag1 = [2]; 
            ii = 2
            jj = 0
        
        ''' ROTATE -> -90; +90 -> column; row; diagonal ''' 
        # row-wise
        idx = 0
        test_row_p90 = []
        test_row_m90 = []
        for figure in [fig_problem[count] for count in row]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[ii] for ii in row1 if idx == 1]:
                    y = figure.visualFilename
                    yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                    test_row_p90.append(f[0])
                    y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                    test_row_m90.append(f[0])
        # column-wise
        idx = 0
        test_col_p90 = []
        test_col_m90 = []
        for figure in [fig_problem[count] for count in col]:
            x = figure.visualFilename
            idx += 1
            for fig in [fig_problem[ii] for ii in col1 if idx == 1]:
                    y = fig.visualFilename
                    yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                    test_col_p90.append(f[0])
                    y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                    test_col_m90.append(f[0])
        # diagonal-wise
        idx = 0
        test_diag_p90 = []
        test_diag_m90 = []
        for figure in [fig_problem[count] for count in diag]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[ii] for ii in diag1 if idx == 1]:
                    y = figure.visualFilename
                    yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                    test_diag_p90.append(f[0])
                    y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                    test_diag_m90.append(f[0])
        # print(test_col_m90,test_col_p90)
        # print(test_row_m90,test_row_p90)
        # print(test_diag_m90,test_diag_p90)
        probab = []
        figID = []
        if all(test_col_p90 + test_col_m90) is True:
            probab1 = []
            probab2 = []
            for figure in fig_choices:
                x = fig_problem[col[-1]+ii-1].visualFilename
                x1 = Image.open(x).convert('1').transpose(Image.ROTATE_90)
                x2 = Image.open(x).convert('1').transpose(Image.ROTATE_270)
                y = figure.visualFilename
                aux, p1 = op.equal_AB( self,x1,Image.open(y).convert('1'))
                probab1.append(p1)
                aux, p2 = op.equal_AB( self,x2,Image.open(y).convert('1'))
                probab2.append(p2)
                figID.append(figure.visualFilename[-5:-4])
            if max(probab1) > max(probab2):    
                idx1 = probab1.index(max(probab1))
                imax = idx1
                probab = probab1
            else:
                idx2 = probab2.index(max(probab2))
                imax = idx2
                probab = probab2
            # print(probab)
            if max(probab) <= tol: return -1
            sol = int(figID[imax])
            return sol
        elif all(test_row_p90 + test_row_m90) is True:
            probab1 = []
            probab2 = []
            for figure in fig_choices:
                x = fig_problem[row[-1]+ii-1].visualFilename
                x1 = Image.open(x).convert('1').transpose(Image.ROTATE_90)
                x2 = Image.open(x).convert('1').transpose(Image.ROTATE_270)
                y = figure.visualFilename
                aux, p1 = op.equal_AB( self,x1,Image.open(y).convert('1'))
                probab1.append(p1)
                aux, p2 = op.equal_AB( self,x2,Image.open(y).convert('1'))
                probab2.append(p2)
                figID.append(figure.visualFilename[-5:-4])
            if max(probab1) > max(probab2):    
                idx1 = probab1.index(max(probab1))
                imax = idx1
                probab = probab1
            else:
                idx2 = probab2.index(max(probab2))
                probab = probab2
                imax = idx2
            if max(probab) <= tol: return -1
            # print(probab)
            sol = int(figID[imax])
            return sol
        elif all(test_diag_p90 + test_diag_m90) is True:
            probab1 = []
            probab2 = []
            for figure in fig_choices:
                x = fig_problem[diag[-1]+ii-1].visualFilename
                x1 = Image.open(x).convert('1').transpose(Image.ROTATE_90)
                x2 = Image.open(x).convert('1').transpose(Image.ROTATE_270)
                y = figure.visualFilename
                aux, p1 = op.equal_AB( self,x1,Image.open(y).convert('1'))
                probab1.append(p1)
                aux, p2 = op.equal_AB( self,x2,Image.open(y).convert('1'))
                probab2.append(p2)
                figID.append(figure.visualFilename[-5:-4])
            if max(probab1) > max(probab2):    
                idx1 = probab1.index(max(probab1))
                imax = idx1
                probab = probab1
            else:
                idx2 = probab2.index(max(probab2))
                probab = probab2
                imax = idx2
            if max(probab) <= tol: return -1
            # print(probab)
            sol = int(figID[imax])
            return sol
        elif all(test_col_p90) is True:
            # column-wise
            x = fig_problem[col[-1]+ii-1].visualFilename
            x = Image.open(x).convert('1').transpose(Image.ROTATE_90)
        elif all(test_row_p90) is True:
            # row-wise
            x = fig_problem[row[-1]+ii].visualFilename
            x = Image.open(x).convert('1').transpose(Image.ROTATE_90)
        elif all(test_diag_p90) is True:
            # diagonal
            x = fig_problem[diag[jj]].visualFilename
            x = Image.open(x).convert('1').transpose(Image.ROTATE_90)
        elif all(test_col_m90) is True:
            # column-wise
            x = fig_problem[col[-1]+ii-1].visualFilename
            x = Image.open(x).convert('1').transpose(Image.ROTATE_270)
        elif all(test_row_m90) is True:
            # row-wise
            x = fig_problem[row[-1]+ii].visualFilename
            x = Image.open(x).convert('1').transpose(Image.ROTATE_270)
        elif all(test_diag_m90) is True:
            # diagonal
            x = fig_problem[diag[jj]].visualFilename
            x = Image.open(x).convert('1').transpose(Image.ROTATE_270)            
        else:
            return -1
        for figure in fig_choices:
            y = figure.visualFilename
            aux, p = op.equal_AB( self,x,Image.open(y).convert('1'))
            probab.append(p)
            figID.append(figure.visualFilename[-5:-4])
        imax = probab.index(max(probab))
        # print(probab)
        if max(probab) <= tol: return -1
        sol = int(figID[imax])
        return sol


    def FILL(self,fig_problem,fig_choices):
        # applicable to 2x2
        global iptype
        global tol
        tol = 0.99
        if iptype == 2 :
            row = [0]; row1 = [1]
            col = [0]; col1 = [2]
            diag = [1]; diag1 = [2]

        ''' FILL '''
        # row-wise
        test_row = []
        for figure in [fig_problem[count] for count in row]:
            x = op.fill(self,figure.visualFilename)
            for figure in [fig_problem[x] for x in row1 ]:
                y = figure.visualFilename
                f = (op.equal_AB( self,x,Image.open(y).convert('1')))
                test_row.append(f[0])
        # column-wise                    
        test_col = []                
        for figure in [fig_problem[count] for count in col]:
            x = op.fill(self,figure.visualFilename)
            for figure in [fig_problem[x] for x in col1 ]:
                y = figure.visualFilename
                f = (op.equal_AB( self,x,Image.open(y).convert('1')))
                test_col.append(f[0])
        # diagonal-wise                    
        test_diag = []                
        for figure in [fig_problem[count] for count in diag]:
            x = op.fill(self,figure.visualFilename)
            for figure in [fig_problem[x] for x in diag1 ]:
                y = figure.visualFilename
                f = (op.equal_AB( self,x,Image.open(y).convert('1')))
                test_diag.append(f[0])
        # print(test_row,test_col,test_diag)
        probab = []    
        figID = []
        if all(test_col + test_row + test_diag) is True:     
            # all 
            for figure in fig_choices:
                y = figure.visualFilename
                aux, p = op.equal_AB( self,x,Image.open(y).convert('1'))
                probab.append(p)
                figID.append(figure.visualFilename[-5:-4])
            imax = probab.index(max(probab))
            sol = int(figID[imax])
            return sol
        elif all(test_col) is True:
            # column-wise
            x = fig_problem[col[-1]+1].visualFilename
        elif all(test_row) is True:
            # row-wise
            x = fig_problem[row[-1]+2].visualFilename
        elif all(test_diag) is True:
            x = fig_problem[diag[0]].visualFilename
        else:
            return -1
        x = op.fill(self,x)
        for figure in fig_choices:
            y = figure.visualFilename
            aux, p = op.equal_AB( self,x,Image.open(y).convert('1'))
            probab.append(p)
            figID.append(figure.visualFilename[-5:-4])
        imax = probab.index(max(probab))
        # print(probab)
        if max(probab) <= tol: return -1
        sol = int(figID[imax])
        return sol
        
    def add_sub(self,fig_problem,fig_choices):
        global iptype
        global tol
        tol = 0.997
        if iptype == 2:
            row = [0]; row1 = [1]; row2 = []; row3 =[]
            col = [0]; col1 = [2]; col2 = []; col3 =[]
            diag = [1]; diag1 = [2]; diag2 = []
            ii = 2
        elif iptype == 3:
            row = [0,3,6]; row1 = [1,2]; row2 = [4,5]; row3 = [7]
            col = [0,1,2]; col1 = [3,6]; col2 = [4,7]; col3 = [5] 
            diag = [0,2]; diag1 = [4]; diag2 =[4,6]
            ii = 3
        
        # row-wise
        idx = 0
        test = []
        dx_row = []
        dcolor_ratio = []
        probab = []
        figID = []
        for figure in [fig_problem[count] for count in row]:
            x = figure.visualFilename
            # check black-to-white pixel ratio;
            # negative difference = addition; positive difference = subtraction
            ratio = op.black_white(self,Image.open(x).convert('1'))
            dcolor_ratio.append(ratio)
            idx += 1
            counter = 0
            for figure in [fig_problem[ii] for ii in row1 if idx == 1]:
                counter += 1
                if counter == 1:
                    if iptype == 2: 
                        y = Image.open(figure.visualFilename).convert('RGB')
                        diff_obj1 = op.diff(self,Image.open(x).convert('RGB'),y)
                        diff = op.diff(self,Image.open(fig_problem[2].visualFilename).convert('RGB'),diff_obj1)
                        for figure in fig_choices:
                            y = figure.visualFilename
                            aux, p = op.equal_AB(self,Image.open(y).convert('1'),diff.convert('1'))
                            probab.append(p)
                            figID.append(figure.visualFilename[-5:-4])
                        # print(probab)
                        # print(figID)
                        imax = probab.index(max(probab))
                        # print(probab)
                        if max(probab) <= 0.997: return -1
                        sol = int(figID[imax])
                        return sol
                    y = Image.open(figure.visualFilename).convert('1')
                    diff = op.equal_AB(self,Image.open(x).convert('1'),y)
                    test.append(diff[1])
                    ratio = op.black_white(self,y)
                    dcolor_ratio.append(ratio)
                elif counter == 2:
                    z = Image.open(figure.visualFilename).convert('1')
                    diff = op.equal_AB(self,y,z)
                    test.append(diff[1])
                    dx_row.append(abs(test[0]-test[1]))
                    ratio = op.black_white(self,z)
                    dcolor_ratio.append(ratio)
            counter = 0
            for figure in [fig_problem[ii] for ii in row2 if idx == 2]:
                counter += 1
                if counter == 1:
                    y = Image.open(figure.visualFilename).convert('1')
                    diff = op.equal_AB(self,Image.open(x).convert('1'),y)
                    test.append(diff[1])
                    ratio = op.black_white(self,y)
                    dcolor_ratio.append(ratio)
                elif counter == 2:
                    z = Image.open(figure.visualFilename).convert('1')
                    diff = op.equal_AB(self,y,z)
                    test.append(diff[1])
                    dx_row.append(abs(test[2]-test[3]))
                    ratio = op.black_white(self,z)
                    dcolor_ratio.append(ratio)
            counter = 0
            for figure in [fig_problem[ii] for ii in row3 if idx == 3]:
                y = Image.open(figure.visualFilename).convert('1')
                diff = op.equal_AB(self,Image.open(x).convert('1'),y)
                test.append(diff[1])
                ratio = op.black_white(self,y)
                dcolor_ratio.append(ratio)
                bwr = []
                bwr.append( dcolor_ratio[0]-dcolor_ratio[1] )
                bwr.append( dcolor_ratio[1]-dcolor_ratio[2] )
                bwr.append( dcolor_ratio[3]-dcolor_ratio[4] )
                bwr.append( dcolor_ratio[4]-dcolor_ratio[5] )
                bwr.append( dcolor_ratio[6]-dcolor_ratio[7] )
                if all(i > 0 for i in bwr) is True:
                    jj = -1 # object subtraction
                elif all(i < 0 for i in bwr) is True:
                    jj = 1 # object addition
                elif any(i == 0 for i in bwr) is True:
                    jj = 0    # add / subt combined
                else:
                    jj = -1
                aux2 = []
                for figure in fig_choices:
                    z = figure.visualFilename
                    aux, p = op.equal_AB(self,Image.open(z).convert('1'),y)
                    probab.append(abs(p-test[4]))
                    figID.append(figure.visualFilename[-5:-4])
                    ratio = op.black_white(self,Image.open(z).convert('1'))
                    aux2.append((dcolor_ratio[7]-ratio))
                dx = abs(probab-sum(dx_row))
                if jj == 1:
                    for iii,val in enumerate(aux2):
                        if aux2[iii] > 0:
                            dx[iii] = 100 
                elif jj == -1:
                    for iii,val in enumerate(aux2):
                        if aux2[iii] < 0:
                            dx[iii] = 100
                imax = np.argmin(dx)
                # print(bwr)
                # print(aux2)
                # print(probab)
                # print(dx)
                    
                if min(dx) >= 1e-1 : return -1
                sol = int(figID[imax])
                return sol


        



######################################################################
class op:
######################################################################
    def __init__(self):
        pass

    # Fig A == Fig B?
    def equal_AB(self,xx,yy):
        global tol
        
        # receive raw image objects 
        sol = SSIM(np.asarray(xx),np.asarray(yy))
        # print(sol)
        if sol > tol:
            return True,sol
        else:
            return False,sol    
    
    # FILL image
    def fill(self,x):
        x = Image.open(x).convert('RGB')
        ImageDraw.floodfill(x,xy=(0,0),value=(255,0,255))
        # Make everything not magenta black
        n  = np.array(x)
        n[(n[:, :, 0:3] != [255,0,255]).any(2)] = [0,0,0]
        # Revert all artifically filled magenta pixels to white
        n[(n[:, :, 0:3] == [255,0,255]).all(2)] = [255,255,255]
        y = Image.fromarray(n).convert('1')
        # y.show()
        return y

    def diff(self,x,y):
        # x = first image (RGB)
        # y = second image (RGB)
        diff = ImageChops.difference(x,y)
        diff = ImageOps.invert(diff.convert('RGB'))
        return diff

    def black_white(self,x):
        # count the number of black and white pixels
        a = np.asarray(x)
        black = np.count_nonzero(a == 0)
        # print(black)
        return black/np.size(a)









#============================================================================
# Structural similarity index code adapted from
# https://github.com/w13b3/SSIM-py
# The code depends on numpy and PILLOW;
# Takes PILLOW image as input
#============================================================================


def gaussian_kernel(shape: tuple = (5,), sigma: tuple = (1.5,)) -> np.ndarray:
    """
    Create a 2d array representing a gaussian kernel.
    shape and sigma tuples with different values can create an asymmetric gauss array.

    References
    ----------
    https://github.com/nichannah/gaussian-filter/blob/master/gaussian_filter.py

    Parameters
    ----------
    shape  tuple  (height, width) of the kernel.
    sigma  tuple  sigma of the kernel.

    Returns
    -------
    numpy.ndarray  an array representing a gaussian kernel.
    """
    size_x, size_y = (shape[0], shape[0]) if len(shape) == 1 else shape[:2]
    sigma_x, sigma_y = (sigma[0], sigma[0]) if len(sigma) == 1 else sigma[:2]

    # faster than np.meshgrid
    y = np.arange(0, size_y, dtype=float)
    x = np.arange(0, size_x, dtype=float)[:, np.newaxis]

    x = np.subtract(x, (size_x // 2))
    y = np.subtract(y, (size_y // 2))

    sigma_x_sq = sigma_x ** 2
    sigma_y_sq = sigma_y ** 2

    exp_part = x ** 2 / (2 * sigma_x_sq) + y ** 2 / (2 * sigma_y_sq)
    kernel = 1 / (2 * np.pi * sigma_x * sigma_y) * np.exp(-exp_part)
    return kernel  # -> np.ndarray


def convolve_array(arr: np.ndarray, conv_filter: np.ndarray) -> np.ndarray:
    """
    Convolves over all the channels of the given array.

    References
    ----------
    https://songhuiming.github.io/pages/2017/04/16/convolve-correlate-and-image-process-in-numpy/


    Parameters
    ----------
    arr  numpy.ndarray  array to convolve over, can be array's with more than 2 dimensions.
    conv_filter  numpy.ndarray  usually a gaussian kernel.

    Returns
    -------
    numpy.ndarray  convolved array with the same dimensions as given.
    """
    if len(arr.shape) <= 2:  # no `depth` and probably 2d array
        return convolve2d(arr, conv_filter)

    # function is faster with concurent.futures and functools.partial
    partial_convolve2d = partial(convolve2d, conv_filter=conv_filter)
    with futures.ThreadPoolExecutor() as ex:  # fast
        arr_stack = ex.map(partial_convolve2d, [arr[:, :, dim] for dim in range(arr.ndim)])

    stack = np.stack(list(arr_stack), axis=2)
    return stack  # -> np.ndarray


def convolve2d(arr: np.ndarray, conv_filter: np.ndarray) -> np.ndarray:
    """
    Convolves over the given array.
    Only accepts array's with two dimensions.

    References
    ----------
    https://en.wikipedia.org/wiki/Convolution#Definition
    https://stackoverflow.com/users/7567938/allosteric

    Parameters
    ----------
    arr  numpy.ndarray  array with 2 dimensions to convolve.
    conv_filter  numpy.ndarray  kernel to calculate the convolution with.

    Raises
    ------
    ValueError  if arr doesn't have 2 dimensions.

    Returns
    -------
    numpy.ndarray  convolved array.
    """
    if len(arr.shape) > 2:
        msg = 'Please input the arr with 2 dimensions'
        raise ValueError(msg)

    view_shape = tuple(np.subtract(arr.shape, conv_filter.shape) + 1) + conv_filter.shape
    as_strided = np.lib.stride_tricks.as_strided
    sub_matrices = as_strided(arr, shape=view_shape, strides=arr.strides * 2).transpose()
    einsum = np.einsum('ij,ijkl->kl', conv_filter, sub_matrices)

    return einsum  # -> np.ndarray


def structural_similarity(array1: np.ndarray, array2: np.ndarray, filter_size: int = 40, filter_sigma: float = 1., \
                        k1: float = 0.01, k2: float = 0.03, max_val: int = 255) -> (np.float64, np.ndarray):
    """
    Compares two given array's with the Structural Similarity (SSIM) index method.

    References
    ----------
    Zhou Wang et al: https://github.com/obartra/ssim/blob/master/assets/ssim.pdf
    https://en.wikipedia.org/wiki/Structural_similarity
    https://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
    https://blog.csdn.net/weixin_42096901/article/details/90172534
    https://github.com/tensorflow/models/blob/master/research/compression/image_encoder/msssim.py

    Parameters
    ----------
    array1  numpy.ndarray  array to compare against the other given array
    array2  numpy.ndarray  array to compare against the other given array
    filter_size  int  gaussian kernel size
    filter_sigma  float  gaussian kernel intensity
    k1  float  default value
    k2  float  default value
    max_val  int  dynamic range of the image  255 for 8-bit  65535 for 16-bit

    Raises
    ------
    ValueError  if given array's doesn't match each others shape (height, width, channels)

    Returns
    -------
    mssim  numpy.ndarray  array (map) of the contrast sensitivity
    ssim  numpy.float64  mean of the contrast sensitivity  number between -1 and 1
    """
    if array1.shape != array2.shape:
        msg = 'Input arrays must have the same shape'
        raise ValueError(msg)

    array1 = array1.astype(np.float64)
    array2 = array2.astype(np.float64)
    height, width = array1.shape[:2]

    if filter_size:  # is 1 or more
        # filter size can't be larger than height or width of arrays.
        size = min(filter_size, height, width)

        # scale down sigma if a smaller filter size is used.
        sigma = size * filter_sigma / filter_size if filter_size else 0
        window = gaussian_kernel(shape=(size,), sigma=(sigma,))
        # convolve = convolve_array
        # compute weighted means
        mu1 = convolve_array(array1, window)
        mu2 = convolve_array(array2, window)

        # compute weighted covariances
        sigma_11 = convolve_array(np.multiply(array1, array1), window)
        sigma_22 = convolve_array(np.multiply(array2, array2), window)
        sigma_12 = convolve_array(np.multiply(array1, array2), window)
    else:  # Empty blur kernel so no need to convolve.
        mu1, mu2 = array1, array2
        sigma_11 = np.multiply(array1, array1)
        sigma_22 = np.multiply(array2, array2)
        sigma_12 = np.multiply(array1, array2)

    # compute weighted variances
    mu_11 = np.multiply(mu1, mu1)
    mu_22 = np.multiply(mu2, mu2)
    mu_12 = np.multiply(mu1, mu2)
    sigma_11 = np.subtract(sigma_11, mu_11)
    sigma_22 = np.subtract(sigma_22, mu_22)
    sigma_12 = np.subtract(sigma_12, mu_12)

    # constants to avoid numerical instabilities close to zero
    c1 = (k1 * max_val) ** 2.
    c2 = (k2 * max_val) ** 2.
    v1 = 2.0 * sigma_12 + c2
    v2 = sigma_11 + sigma_22 + c2

    # Numerator of SSIM
    num_ssim = (2. * mu_12 + c1) * v1   # -> np.ndarray

    # Denominator of SSIM
    den_ssim = (mu_11 + mu_22 + c1) * v2   # -> np.ndarray

    # SSIM (contrast sensitivity)
    ssim = num_ssim / den_ssim  # -> np.ndarray

    # MeanSSIM
    mssim = np.mean(ssim)  # -> np.float64
    return mssim, ssim  # -> (np.float64, np.ndarray)


def crop_to_smallest(array1: np.ndarray, array2: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Crops the given array's to the smallest height and width of both array's.
    if both images already have the same height and width, nothing will be cropped.

    Parameters
    ----------
    array1  numpy.ndarray  input array to crop
    array2  numpy.ndarray  input array to crop

    Raises
    ------
    ValueError  if given arrays doesn't have 2 or more dimensions

    Returns
    -------
    array1  numpy.ndarray  cropped to the smallest height and width
    array2  numpy.ndarray  cropped to the smallest height and width
    """

    size1_y, size1_x = array1.shape[:2]  # get y and x values of both arrays
    size2_y, size2_x = array2.shape[:2]

    size_y, size_x = min(size1_y, size2_y), min(size1_x, size2_x)  # get minimum x and y value
    array1, array2 = array1[0:size_y, 0:size_x], array2[0:size_y, 0:size_x]  # crop according minimum

    return array1, array2  # -> (np.ndarray, np.ndarray)


def SSIM(img1,img2):

    __version__ = '1.0.0'

    description = """
    This is the --help information
    ------------------------------
    Compares two given images and returns a score between 0 and 1.
    The score is calculated with Structural Similarity (SSIM) index method.

    Best result is given if both images are the same height and width.
    Converts the images to B/W if given images doesn't have the same channels.
    """
    # https://github.com/w13b3/SSIM-py

    # get arguments
    parser = argparse.ArgumentParser(usage='use "%(prog)s --help" for more information',
                                description=description,
                                formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-g', '--gray', action='store_true',
                        help='convert images to gray before comparison')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true',
                    help='show initial arguments and logging')
    group.add_argument('-q', '--quiet', action='store_true',
                    help='show nothing, not even the score of the comparison')
    arguments = parser.parse_args()

    arguments.image1 = img1
    arguments.image2 = img2


    # compare images
    img1_arr = arguments.image1
    img2_arr = arguments.image2

    img1_crop, img2_crop = crop_to_smallest(img1_arr, img2_arr)
    ssim_score, ssim_map = structural_similarity(img1_crop, img2_crop)
    return ssim_score