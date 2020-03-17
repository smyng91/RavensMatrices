
import numpy as np
from PIL import Image, ImageChops, ImageOps, ImageFilter, ImageDraw
from itertools import product
import pprint, logging
import math, operator


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
        for figure in problem.figures:
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

        return problem.answer

######################################################################
class Solver:
######################################################################
    def __init__(self):
        pass

    def solve(self,fig_problem,fig_choices):
        sol = test.EQUAL(self,fig_problem,fig_choices)
        if sol != -1: print(sol); return sol
        sol = test.MIRROR(self,fig_problem,fig_choices)
        if sol != -1: print(sol); return sol
        sol = test.ROTATE(self,fig_problem,fig_choices)
        if sol != -1: print(sol); return sol
        # sol = test.FILL(self,fig_problem,fig_choices)
        # if sol != -1: print(sol); return sol
        print('cannot solve!')
        return -1



        # # Check for addition and subtraction between Fig A and B
        # x = "A"
        # y = "B"
        # z = "C" # C will be tested against choices
        # if Operation.test_add_sub( fig_progression, fig_choice, x, y, z ):
        #     for fig in fig_choice:
        #         fig_sol = Operation.test_add_sub( fig_progression, fig_choice, x, y, z )[1]        
        #         sol = int(fig_sol[-5]) 
        #         solverType = 'Add/Sub; A/B'
        #         return sol                           

        # # Check for addition and subtraction between Fig A and C
        # x = "A"
        # y = "C"
        # z = "B" # C will be tested against choices
        # if Operation.test_add_sub( fig_progression, fig_choice, x, y, z ):
        #     print("true")
        #     for fig in fig_choice:
        #         fig_sol = Operation.test_add_sub( fig_progression, fig_choice, x, y, z )[1]        
        #         sol = int(fig_sol[-5]) 
        #         solverType = 'Add/Sub; A/C'
        #         return sol        



######################################################################
class test(Solver):
######################################################################       
    def __init__(self):
        
        super()

    def EQUAL(self,fig_problem,fig_choices):
        
        global iptype
        global tol
        tol = 0.999
        if iptype == 2 :
            row = [0,2]; row1 = [0,1]; row2 = [2]; row3 = []
            col = [0,1]; col1 = [0,2]; col2 = [1]; col3 = []
            diag = [1]; diag1 = [1,2]; diag2 = []
        elif iptype == 3:
            row = [0,3,6]; row1 = [0,1,2]; row2 = [3,4,5]; row3 = [6,7]
            col = [0,1,2]; col1 = [0,3,6]; col2 = [1,4,7]; col3 = [2,5]
            diag = [0,2]; diag1 = [0,4]; diag2 = [2,4,6]

        ''' EQUAL -> all; row-wise; column-wise; diagonal'''
        # row-wise
        idx = 0
        test_row = []
        for figure in [fig_problem[count] for count in row]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[x] for x in row1 if idx == 1]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_row.append(f[0])
            for figure in [fig_problem[x] for x in row2 if idx == 2]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_row.append(f[0])
            for figure in [fig_problem[x] for x in row3 if idx == 3]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_row.append(f[0])
        # column-wise                    
        idx = 0    
        test_col = []                
        for figure in [fig_problem[count] for count in col]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[x] for x in col1 if idx == 1]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_col.append(f[0])
            for figure in [fig_problem[x] for x in col2 if idx == 2]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_col.append(f[0])
            for figure in [fig_problem[x] for x in col3 if idx == 3]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_col.append(f[0])

        # diagonal-wise                    
        idx = 0    
        test_diag = []                
        for figure in [fig_problem[count] for count in diag]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[x] for x in diag1 if idx == 1]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_diag.append(f[0])
            for figure in [fig_problem[x] for x in diag2 if idx == 2]:
                y = figure.visualFilename
                f = (op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1')))
                test_diag.append(f[0])
        # print(test_col,test_row,test_diag)
        probab = []    
        if all(test_col + test_row + test_diag) is True:     
            # all 
            for figure in fig_choices:
                y = figure.visualFilename
                aux, p = op.equal_AB( self,Image.open(x).convert('1'),Image.open(y).convert('1'))
                probab.append(p)
            idx = probab.index(max(probab))+1
            sol = int(idx)
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
        idx = probab.index(max(probab))+1
        # print(probab)
        if max(probab) <= 0.999: return -1
        sol = int(idx)
        return sol


    def MIRROR(self,fig_problem,fig_choices):

        global iptype
        global tol
        tol = 0.999
        if iptype == 2 :
            row = [0]; row1 = [1]; row2 = []
            col = [0]; col1 = [2]; col2 = []
            diag = [1]; diag1 = [2]; diag2 = []
            ii = 2
        elif iptype == 3:
            row = [0,3]; row1 = [2]; row2 = [5]  
            col = [0,1]; col1 = [6]; col2 = [7] 
            diag = [2]; diag1 = [6];
            ii = 3
        
        ''' MIRROR -> LEFT-RIGHT; TOP-BOTTOM -> column; row; diagonal ''' 
        # row-wise
        idx = 0
        test_row_lr = []
        test_row_tb = []
        for figure in [fig_problem[count] for count in row]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[x] for x in row1 if idx == 1]:
                y = figure.visualFilename
                yy = Image.open(y).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
                f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                test_row_lr.append(f[0])
                y = Image.open(y).convert('1').transpose(Image.FLIP_TOP_BOTTOM)
                f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                test_row_tb.append(f[0])
            for figure in [fig_problem[x] for x in row2 if idx == 2]:
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
            for figure in [fig_problem[x] for x in col1 if idx==1]:
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
            for figure in [fig_problem[x] for x in diag1 if idx == 1]:
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
        idx = probab.index(max(probab))+1
        if max(probab) <= 0.999: return -1
        sol = int(idx)
        return sol


    def ROTATE(self,fig_problem,fig_choices):
        global iptype
        global tol
        tol = 0.999
        if iptype == 2:
            row = [0]; row1 = [1]; row2 = []; row3=[]; row4=[]; row5=[]
            col = [0]; col1 = [2]; col2 = []; col3=[]; col4=[]; col5=[]
            diag = [1]; diag1 = [2]; diag2 = []
            ii = 2
            jj = 0
        # elif iptype == 3:
        #     row = [0,3,6]; row1 = [1,2]; row2 = [4,5]; row3 = [7]
        #     col = [0,1,2]; col1 = [3,6];  col2 = [4,7]; col3 = [5]
        #     diag = [0,2]; diag1 = [4]; diag2 = [4,6]
        #     jj = 4
        
        ''' ROTATE -> -90; +90 -> column; row; diagonal ''' 
        # row-wise
        idx = 0
        test_row_p90 = []
        test_row_m90 = []
        for figure in [fig_problem[count] for count in row]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[x] for x in row1 if idx == 1]:
                    y = figure.visualFilename
                    yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                    test_row_p90.append(f[0])
                    y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                    test_row_m90.append(f[0])
            # for figure in [fig_problem[x] for x in row2 if idx == 2]:
            #         y = figure.visualFilename
            #         yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
            #         test_row_p90.append(f[0])
            #         y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),y))
            #         test_row_m90.append(f[0])
            # for figure in [fig_problem[x] for x in row3 if idx == 3]:
            #         y = figure.visualFilename
            #         yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
            #         test_row_p90.append(f[0])
            #         y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),y))
            #         test_row_m90.append(f[0])
        # column-wise
        idx = 0
        test_col_p90 = []
        test_col_m90 = []
        for figure in [fig_problem[count] for count in col]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[x] for x in col1 if idx == 1]:
                    y = figure.visualFilename
                    yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                    test_col_p90.append(f[0])
                    y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                    test_col_m90.append(f[0])
            # for figure in [fig_problem[x] for x in col2 if idx == 2]:
            #         y = figure.visualFilename
            #         yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
            #         test_col_p90.append(f[0])
            #         y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),y))
            #         test_col_m90.append(f[0])
            # for figure in [fig_problem[x] for x in col3 if idx == 3]:
            #         y = figure.visualFilename
            #         yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
            #         test_col_p90.append(f[0])
            #         y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),y))
            #         test_col_m90.append(f[0])
        # diagonal-wise
        idx = 0
        test_diag_p90 = []
        test_diag_m90 = []
        for figure in [fig_problem[count] for count in diag]:
            x = figure.visualFilename
            idx += 1
            for figure in [fig_problem[x] for x in diag1 if idx == 1]:
                    y = figure.visualFilename
                    yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
                    test_diag_p90.append(f[0])
                    y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
                    f = (op.equal_AB( self,Image.open(x).convert('1'),y))
                    test_diag_m90.append(f[0])
            # for figure in [fig_problem[x] for x in diag2 if idx == 2]:
            #         y = figure.visualFilename
            #         yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
            #         test_diag_p90.append(f[0])
            #         y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
            #         f = (op.equal_AB( self,Image.open(x).convert('1'),y))
            #         test_diag_m90.append(f[0])

        # print(test_col_m90,test_col_p90)
        # print(test_row_m90,test_row_p90)
        # print(test_diag_m90,test_diag_p90)
        probab = []
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
            if max(probab1) > max(probab2):    
                idx1 = probab1.index(max(probab1))+1
                idx = idx1
                probab = probab1
            else:
                idx2 = probab2.index(max(probab2))+1
                idx = idx2
                probab = probab2
            # print(probab)
            if max(probab) <= 0.999: return -1
            sol = int(idx)
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
            if max(probab1) > max(probab2):    
                idx1 = probab1.index(max(probab1))+1
                idx = idx1
                probab = probab1
            else:
                idx2 = probab2.index(max(probab2))+1
                probab = probab2
                idx = idx2
            if max(probab) <= 0.999: return -1
            sol = int(idx)
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
            if max(probab1) > max(probab2):    
                idx1 = probab1.index(max(probab1))+1
                idx = idx1
                probab = probab1
            else:
                idx2 = probab2.index(max(probab2))+1
                probab = probab2
                idx = idx2
            if max(probab) <= 0.999: return -1
            sol = int(idx)
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
        idx = probab.index(max(probab))+1
        if max(probab) <= 0.999: return -1
        sol = int(idx)
        return sol


    def FILL(self,fig_problem,fig_choices):
        global iptype
        global tol
        tol = 0.999
        if iptype == 2:
            row = [0]; row1 = [1]; row2 = []; 
            col = [0]; col1 = [2]; col2 = []; 
            diag = [1]; diag1 = [2]; diag2 = []; 
            ii = 2
            jj = 0
        elif iptype == 3:
            row = [0,3,6]; row1 = [1,2]; row2 = [4,5]; row3 = [7]
            col = [0,1,2]; col1 = [3,6];  col2 = [4,7]; col3 = [5]
            diag = [0,2]; diag1 = [4]; diag2 = [4,6]
            jj = 4       
        
    #     # row-wise
    #     idx = 0
    #     test_row = []
    #     for figure in [fig_problem[count] for count in row]:
    #         x = figure.visualFilename
    #         idx += 1
    #         for figure in [fig_problem[x] for x in row1 if idx == 1]:
    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_row_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_row_m90.append(f[0])
    
    #         for figure in [fig_problem[x] for x in row2 if idx == 2]:
    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_row_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_row_m90.append(f[0])
      
    #         for figure in [fig_problem[x] for x in row3 if idx == 3]:
             
    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_row_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_row_m90.append(f[0])
            
    #     # column-wise
    #     idx = 0
    #     test_col_p90 = []
    #     test_col_m90 = []
    #     for figure in [fig_problem[count] for count in col]:
    #         x = figure.visualFilename
    #         idx += 1
      
    #         for figure in [fig_problem[x] for x in col1 if idx == 1]:
        
    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_col_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_col_m90.append(f[0])

    #         for figure in [fig_problem[x] for x in col2 if idx == 2]:
  
    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_col_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_col_m90.append(f[0])
           
    #         for figure in [fig_problem[x] for x in col3 if idx == 3]:
          
    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_col_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_col_m90.append(f[0])
    
    #     # diagonal-wise
    #     idx = 0
    #     test_diag_p90 = []
    #     test_diag_m90 = []
    #     for figure in [fig_problem[count] for count in diag]:
    #         x = figure.visualFilename
    #         idx += 1
    
    #         for figure in [fig_problem[x] for x in diag1 if idx == 1]:

    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_diag_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_diag_m90.append(f[0])
  
    #         for figure in [fig_problem[x] for x in diag2 if idx == 2]:
    
    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_diag_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_diag_m90.append(f[0])
    
    #         for figure in [fig_problem[x] for x in diag3 if idx == 3]:

    #                 y = figure.visualFilename
    #                 yy = Image.open(y).convert('1').transpose(Image.ROTATE_90)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),yy))
    #                 test_diag_p90.append(f[0])
    #                 y = Image.open(y).convert('1').transpose(Image.ROTATE_270)
    #                 f = (op.equal_AB( self,Image.open(x).convert('1'),y))
    #                 test_diag_m90.append(f[0])
     
    #     # print(test_col_m90,test_col_p90)
    #     # print(test_row_m90,test_row_p90)
    #     # print(test_diag_m90,test_diag_p90)
    #     probab = []
    #     if all(test_col_p90 + test_col_m90) is True:
    #         probab1 = []
    #         probab2 = []
    #         for figure in fig_choices:
    #             x = fig_problem[col[-1]+ii-1].visualFilename
    #             x1 = Image.open(x).convert('1').transpose(Image.ROTATE_90)
    #             x2 = Image.open(x).convert('1').transpose(Image.ROTATE_270)
    #             y = figure.visualFilename
    #             aux, p1 = op.equal_AB( self,x1,Image.open(y).convert('1'))
    #             probab1.append(p1)
    #             aux, p2 = op.equal_AB( self,x2,Image.open(y).convert('1'))
    #             probab2.append(p2)
    #         if max(probab1) > max(probab2):    
    #             idx1 = probab1.index(max(probab1))+1
    #             idx = idx1
    #             probab = probab1
    #         else:
    #             idx2 = probab2.index(max(probab2))+1
    #             idx = idx2
    #             probab = probab2
    #         # print(probab)
    #         if max(probab) <= 0.999: return -1
    #         sol = int(idx)
    #         return sol
    #     elif all(test_row_p90 + test_row_m90) is True:
    #         probab1 = []
    #         probab2 = []
    #         for figure in fig_choices:
    #             x = fig_problem[row[-1]+ii-1].visualFilename
    #             x1 = Image.open(x).convert('1').transpose(Image.ROTATE_90)
    #             x2 = Image.open(x).convert('1').transpose(Image.ROTATE_270)
    #             y = figure.visualFilename
    #             aux, p1 = op.equal_AB( self,x1,Image.open(y).convert('1'))
    #             probab1.append(p1)
    #             aux, p2 = op.equal_AB( self,x2,Image.open(y).convert('1'))
    #             probab2.append(p2)
    #         if max(probab1) > max(probab2):    
    #             idx1 = probab1.index(max(probab1))+1
    #             idx = idx1
    #             probab = probab1
    #         else:
    #             idx2 = probab2.index(max(probab2))+1
    #             probab = probab2
    #             idx = idx2
    #         if max(probab) <= 0.999: return -1
    #         sol = int(idx)
    #         return sol
    #     elif all(test_diag_p90 + test_diag_m90) is True:
    #         probab1 = []
    #         probab2 = []
    #         for figure in fig_choices:
    #             x = fig_problem[diag[-1]+ii-1].visualFilename
    #             x1 = Image.open(x).convert('1').transpose(Image.ROTATE_90)
    #             x2 = Image.open(x).convert('1').transpose(Image.ROTATE_270)
    #             y = figure.visualFilename
    #             aux, p1 = op.equal_AB( self,x1,Image.open(y).convert('1'))
    #             probab1.append(p1)
    #             aux, p2 = op.equal_AB( self,x2,Image.open(y).convert('1'))
    #             probab2.append(p2)
    #         if max(probab1) > max(probab2):    
    #             idx1 = probab1.index(max(probab1))+1
    #             idx = idx1
    #             probab = probab1
    #         else:
    #             idx2 = probab2.index(max(probab2))+1
    #             probab = probab2
    #             idx = idx2
    #         if max(probab) <= 0.999: return -1
    #         sol = int(idx)
    #         return sol
    #     elif all(test_col_p90) is True:
    #         # column-wise
    #         x = fig_problem[col[-1]+ii-1].visualFilename
    #         x = Image.open(x).convert('1').transpose(Image.ROTATE_90)
    #     elif all(test_row_p90) is True:
    #         # row-wise
    #         x = fig_problem[row[-1]+ii].visualFilename
    #         x = Image.open(x).convert('1').transpose(Image.ROTATE_90)
    #     elif all(test_diag_p90) is True:
    #         # diagonal
    #         x = fig_problem[diag[jj]].visualFilename
    #         x = Image.open(x).convert('1').transpose(Image.ROTATE_90)
    #     elif all(test_col_m90) is True:
    #         # column-wise
    #         x = fig_problem[col[-1]+ii-1].visualFilename
    #         x = Image.open(x).convert('1').transpose(Image.ROTATE_270)
    #     elif all(test_row_m90) is True:
    #         # row-wise
    #         x = fig_problem[row[-1]+ii].visualFilename
    #         x = Image.open(x).convert('1').transpose(Image.ROTATE_270)
    #     elif all(test_diag_m90) is True:
    #         # diagonal
    #         x = fig_problem[diag[jj]].visualFilename
    #         x = Image.open(x).convert('1').transpose(Image.ROTATE_270)            
    #     else:
    #         return -1
    #     for figure in fig_choices:
    #         y = figure.visualFilename
    #         aux, p = op.equal_AB( self,x,Image.open(y).convert('1'))
    #         probab.append(p)
    #     idx = probab.index(max(probab))+1
    #     if max(probab) <= 0.999: return -1
    #     sol = int(idx)
    #     return sol


    #     ''' FILL -> column; row; diagonal ''' 
    #     x = fig_problem.visualFilename.convert('RGB')
    #     fig_fill = op.FILL(self,x,)
        
    #     for fig in fig_choice:
    #         figID = fig.visualFilename
    #         figureImage = figID).convert('1')
    #         # figureImage.show()
    #         # diff = ImageChops.dsifference(figureImage,fig_progress)
    #         # diff.show() 
    #         diff = ImageChops.subtract_modulo(fig_progress,figureImage)
    #         # need to compare both edge / fill using subtraction
    #         if( np.amax(diff) < 10 ):
    #             return figID








            
######################################################################
class op(test):
######################################################################
    def __init__(self):
        super()

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
        ImageDraw.floodfill(x,xy=(0,0),value=(255,0,255))
        # Make everything not magenta black
        n  = np.array(x)
        n[(n[:, :, 0:3] != [255,0,255]).any(2)] = [0,0,0]
        # Revert all artifically filled magenta pixels to white
        n[(n[:, :, 0:3] == [255,0,255]).all(2)] = [255,255,255]
        return Image.fromarray(n).convert('1')



    # # B == A in shape, but filled in color
    # # first test whether the shape is correct
    # def test_shape(self,fig_progression, x, y):
    #     cell_images = {}
    #     for fig in fig_progression:
    #         figID = fig.visualFilename
    #         figureImage = figID).convert("L")
    #         figEdges = figureImage.filter(ImageFilter.FIND_EDGES)
    #         cell_images[figID[-5]] = figEdges
    #     if ImgAnalysis.diff_rms(cell_images[x], cell_images[y]) >= 100:
    #         return False
    #     else:
    #         return True      

    # # check for addition / subtraction
    # def test_add_sub(self,fig_progression, fig_choice, x, y, z):
    #     cell_images = {}
    #     for fig in fig_progression:
    #         figID = fig.visualFilename
    #         figureImage = figID).convert("1")
    #         cell_images[figID[-5]] = figureImage

    #     # x - y
    #     diff = ImageChops.difference(cell_images[x],cell_images[y])
    #     diff = ImageOps.invert(diff.convert('RGB'))
    #     # diff.show()
    #     # (x-y) + z
    #     tmp = cell_images[z].convert('RGB')
    #     # tmp.show()
    #     new = ImageChops.difference(tmp, diff)
    #     new = ImageOps.invert(new.convert('RGB'))
    #     # new.show()

    #     # test available choices
    #     for fig in fig_choice:
    #         state = False
    #         figID = fig.visualFilename
    #         figureImage = figID).convert('RGB')
    #         # need to compare both edge / fill using subtraction
    #         # print(ImgAnalysis.diff_rms(new, figureImage))
    #         if ImgAnalysis.diff_rms(new, figureImage) < 600:
    #             state = True
    #             return state, figID


















#============================================================================
# Structural similarity index code adapted from
# https://github.com/w13b3/SSIM-py
# The code depends on numpy and PILLOW;
# Takes PILLOW image as input
#============================================================================

import sys
import logging
import argparse

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

import logging
from concurrent import futures
from functools import partial
import numpy as np


__version__ = '1.0.0'
logging.debug(f'ssim version: {__version__}')
logging.debug(f'numpy version: {np.__version__}')


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
    logging.info(f'gaussian_kernel: sigma_x {sigma_x}, sigma_y {sigma_y}')
    logging.info(f'gaussian_kernel: size_x {size_x}, size_y {size_y}')

    # faster than np.meshgrid
    y = np.arange(0, size_y, dtype=float)
    x = np.arange(0, size_x, dtype=float)[:, np.newaxis]

    x = np.subtract(x, (size_x // 2))
    y = np.subtract(y, (size_y // 2))

    sigma_x_sq = sigma_x ** 2
    sigma_y_sq = sigma_y ** 2

    exp_part = x ** 2 / (2 * sigma_x_sq) + y ** 2 / (2 * sigma_y_sq)
    kernel = 1 / (2 * np.pi * sigma_x * sigma_y) * np.exp(-exp_part)
    logging.debug(f'gaussian_kernel: created kernel shape {kernel.shape}')
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
        logging.info(f'convolve_array: given array has 2 dimensions, shape {arr.shape}')
        return convolve2d(arr, conv_filter)
    logging.info(f'convolve_array: given array has more than 2 dimensions, shape {arr.shape}')

    # function is faster with concurent.futures and functools.partial
    partial_convolve2d = partial(convolve2d, conv_filter=conv_filter)
    with futures.ThreadPoolExecutor() as ex:  # fast
        arr_stack = ex.map(partial_convolve2d, [arr[:, :, dim] for dim in range(arr.ndim)])

    stack = np.stack(list(arr_stack), axis=2)
    logging.debug(f"convolve_array: stack shape {stack.shape}")
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
        logging.error(msg=msg)
        raise ValueError(msg)

    view_shape = tuple(np.subtract(arr.shape, conv_filter.shape) + 1) + conv_filter.shape
    as_strided = np.lib.stride_tricks.as_strided
    sub_matrices = as_strided(arr, shape=view_shape, strides=arr.strides * 2).transpose()
    einsum = np.einsum('ij,ijkl->kl', conv_filter, sub_matrices)

    logging.debug(f"convolve2d: einsum shape {einsum.shape}")
    return einsum  # -> np.ndarray


def structural_similarity(array1: np.ndarray, array2: np.ndarray, filter_size: int = 11, filter_sigma: float = 1.5,
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
        logging.error(msg=msg)
        raise ValueError(msg)

    array1 = array1.astype(np.float64)
    array2 = array2.astype(np.float64)
    height, width = array1.shape[:2]
    logging.info(f'structural_similarity: array height {height}, width {width}')

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
    c1 = (k1 * max_val) ** 2
    c2 = (k2 * max_val) ** 2
    v1 = 2.0 * sigma_12 + c2
    v2 = sigma_11 + sigma_22 + c2

    # Numerator of SSIM
    num_ssim = (2 * mu_12 + c1) * v1   # -> np.ndarray

    # Denominator of SSIM
    den_ssim = (mu_11 + mu_22 + c1) * v2   # -> np.ndarray

    # SSIM (contrast sensitivity)
    ssim = num_ssim / den_ssim  # -> np.ndarray

    # MeanSSIM
    mssim = np.mean(ssim)  # -> np.float64
    logging.debug(f'structural_similarity: returned mean ssim (score) {mssim}')
    return mssim, ssim  # -> (np.float64, np.ndarray)


# if __name__ == '__main__':
#     print('start\n')

#     import logging
#     console = logging.StreamHandler()
#     logging.basicConfig(level=logging.DEBUG, handlers=(console,))
#     logging.getLogger('__main__').setLevel(logging.DEBUG)
#     logging.captureWarnings(True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# processing.py
# https://github.com/w13b3/SSIM-py

import os
import logging
from contextlib import suppress

import numpy as np

cv2 = None  # try to import opencv-python
with suppress(ModuleNotFoundError):
    import cv2
    logging.debug(f'opencv-python version: {cv2.__version__}')

Image = None  # try to import Pillow
with suppress(ModuleNotFoundError):
    from PIL import Image, __version__
    logging.debug(f'Pillow version: {__version__}')

if not any((cv2, Image)):  # if neither opencv-python or Pillow are installed
    msg = 'Expected either cv2 (opencv-python) or PIL (Pillow) to be installed.'
    logging.error(msg=msg)
    raise ModuleNotFoundError(msg)


__version__ = '1.0.0'
logging.debug(f'processing version: {__version__}')
logging.debug(f'PIL.Image: {type(Image)}')  # check if modules are imported
logging.debug(f'cv2: {type(cv2)}')          # if not result: <class 'NoneType'>


# def _cv2_array(image_path: str, output_gray: bool = False) -> (np.array, None):
#     """ turn an image into an array with cv2 """
#     logging.info(f'_cv2_array: Input image_path {image_path}')
#     logging.info(f'_cv2_array: output_gray {output_gray}')
#     array = None
#     with suppress(cv2.error):
#         array = cv2.imread(image_path, int(not bool(output_gray)))
#     logging.debug(f'_cv2_array: output type {type(array)}')
#     return array  # -> (np.array or None)


# def _pil_array(image_path: str, output_gray: bool = False) -> (np.array, None):
#     """ turn an image into an array with PIL.Image """
#     # logging.info(f'_pil_array: Input image_path {image_path}')
#     # logging.info(f'_pil_array: output_gray {output_gray}')
#     array = None
#     with suppress(FileNotFoundError):
#         with open(image_path, 'rb') as readbytes:
#             open_image = Image.open(readbytes)
#             if bool(output_gray):
#                 # open_image.load()
#                 open_image = open_image.convert('1')
#             array = np.asarray(open_image)
#     logging.debug(f'_pil_array: output type {type(array)}')
#     return array  # -> (np.array or None)


# def image_to_array(image_path: str, output_gray: bool = False) -> np.ndarray:
    # """
    # Turns an image into an array with PIL or cv2.
    # cv2 preferred over PIL.

    # Parameters
    # ----------
    # image_path  str  path to the image.
    # output_gray  bool  True returns a grayscale array.

    # Raises
    # ------
    # FileNotFoundError  if the path to the image is not found.
    # ValueError  if the conversion to array failed and None is returned.

    # Returns
    # -------
    # image_array  numpy.ndarray  array with a value representation of the given image.
    # """
    # logging.info(f'image_to_array: Input image_path {image_path}')
    # logging.info(f'image_to_array: output_gray {output_gray}')
    # image = os.path.realpath(image_path)  # get the absolute path
    # if not os.path.exists(image):
        # msg = f'No such file or directory: {image_path}'
        # logging.error(msg=msg)
        # raise FileNotFoundError(msg)

    # # cv2 preferred over PIL
    # array_func = _pil_array
    # image_array = array_func(image, output_gray)
    # if image_array is None:
    #     msg = f'Image could not be converted to array: {image_path}'
    #     logging.error(msg=msg)
    #     ValueError(msg)

    # return image_array  # -> np.ndarray


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
    if array1.ndim < 2 or array2.ndim < 2:
        msg = 'Expected given array\'s to have at least 2 dimensions'
        logging.error(msg=msg)
        raise ValueError(msg)

    size1_y, size1_x = array1.shape[:2]  # get y and x values of both arrays
    size2_y, size2_x = array2.shape[:2]
    logging.info(f'crop_to_smallest: array1 size_y {size1_y}, size_x {size1_x}')
    logging.info(f'crop_to_smallest: array2 size_y {size2_y}, size_x {size2_x}')

    size_y, size_x = min(size1_y, size2_y), min(size1_x, size2_x)  # get minimum x and y value
    array1, array2 = array1[0:size_y, 0:size_x], array2[0:size_y, 0:size_x]  # crop according minimum

    logging.debug(f'crop_to_smallest: cropped arrays to size_y {size_y}, size_x {size_x}')
    return array1, array2  # -> (np.ndarray, np.ndarray)


# if __name__ == '__main__':
#     print('start\n')

#     import logging
#     console = logging.StreamHandler()
#     logging.basicConfig(level=logging.DEBUG, handlers=(console,))
#     logging.getLogger('__main__').setLevel(logging.DEBUG)
#     logging.captureWarnings(True)

def SSIM(img1,img2):

    # get arguments
    parser = argparse.ArgumentParser(usage='use "%(prog)s --help" for more information',
                                description=description,
                                formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('image1', type=str,
    #                     help='path to image one')
    # parser.add_argument('image2', type=str,
    #                     help='path to image two')
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

    if arguments.verbose:  # enable to show logging if -v or --verbose
        sys.stdout.write('Python: %s\n' % sys.version)

        for key, val in vars(arguments).items():
            sys.stdout.write('%s: %s\n' % (key, val))

        # stream to sys.stdout so piping is enabled, example:
        # python SSIM-py.zip --verbose path/to/image1 path/to/image2 > SSIM-py.log
        # stdout = logging.StreamHandler(stream=sys.stdout)
        stdout = logging.StreamHandler()
        logging.basicConfig(level=logging.DEBUG, handlers=(stdout,))
        logging.getLogger("__main__").setLevel(logging.DEBUG)
        logging.captureWarnings(True)

    logging.debug(f'main version: {__version__}')

    # compare images
    img1_arr = arguments.image1
    img2_arr = arguments.image2

    # if both image dimensions compare the images to Black/White.
    # happens when Black/White and RedGreenBlue images are compared.
    # if img1_arr.ndim != img2_arr.ndim:
    #     sys.stdout.write('WARNING: images given have different dimensions\n')
    #     sys.stdout.write('\tConverting given images to Black/White before comparison\n')
    #     img1_arr = image_to_array(arguments.image1, output_gray=True)
    #     img2_arr = image_to_array(arguments.image2, output_gray=True)

    img1_crop, img2_crop = crop_to_smallest(img1_arr, img2_arr)
    ssim_score, ssim_map = structural_similarity(img1_crop, img2_crop)
    return ssim_score

    # # show result if not -q or --quiet
    # if not arguments.quiet:
    #     score = 'Score: ' if arguments.verbose else ''
    #     newline = '\n' if arguments.verbose else ''
    #     sys.stdout.write('%s%s%s' % (score, float(ssim_score), newline))
