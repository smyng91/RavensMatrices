
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

        problem.answer = -1  # set the default answer to null

        # categorize problem figures
        ID_progression = ["A.png", "B.png", "C.png", "D.png", "E.png", "F.png", "G.png", "H.png"]
        fig_progression = []
        for figure in problem.figures:
            fig = problem.figures[figure]
            figID = fig.visualFilename  # figure name
            if figID[-5:] in ID_progression:
                fig_progression.append(fig)
        ID_choice = ["1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png"]
        fig_choice = []
        for figure in problem.figures:
            fig = problem.figures[figure]
            figID = fig.visualFilename  # figure name
            if figID[-5:] in ID_choice:
                fig_choice.append(fig)

        # check problem type
        if problem.problemType == "2x2":
            problem.answer = Solver.twoXtwo(problem,fig_progression,fig_choice)
            if problem.answer == 0: problem.answer = -1 
            print(problem.answer)
        elif problem.problemType == "3x3":
            problem.answer = Solver.threeXthree(problem,fig_progression,fig_choice)
            if problem.answer == 0: problem.answer = -1
        else:
            problem.answer = -1
        return problem.answer

######################################################################
class Solver:
######################################################################
    def __init__(self):
        pass

    def twoXtwo(problem,fig_progression,fig_choice):
        global deg
        global solverType
        solverType = []

        


        # Check if A=B=C
        if Operation.test_equal_all( fig_progression ):
            fig_sol = ImgAnalysis.match_figs(fig_progression[0], fig_choice) 
            if fig_sol:
                sol = int(fig_sol[-5])
                solverType = 'A=B=C'
                return sol

        # Check if A = B (hence C = D)
        if Operation.test_equal_AB( fig_progression ):
            x = "C.png" # C will be tested against choices
            for fig in fig_progression:
                if x in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_figs(fig, fig_choice) 
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'A = B; C = D'
                        return sol
       
        # Check if A = C (hence B = D)
        if Operation.test_equal_AC( fig_progression ):
            x = "B.png" # B will be tested against choices
            for fig in fig_progression:
                if x in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_figs(fig, fig_choice) 
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'A = C; B = D'
                        return sol
        
        # Check if B is a mirror image of A
        if Operation.test_mirrir_AB( fig_progression ):
            x = "C.png" # C will be tested against choices
            for fig in fig_progression:
                if x in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_mirror_y(fig, fig_choice) 
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'B mirror of A'
                        return sol

        # Check if C is a mirror image of A
        if Operation.test_mirrir_AC( fig_progression ):
            x = "B.png" # B will be tested against choices
            for fig in fig_progression:
                if x in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_mirror_x(fig, fig_choice) 
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'C mirror of A'
                        return sol

        # Check if B is a rotation of A; include both -90 and + 90                          
        x = "A"
        y = "B"
        if Operation.test_rotate( fig_progression, x, y ):
            z = "C.png" # C will be tested against choices
            for fig in fig_progression:
                if z in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_rotate(fig, fig_choice )  
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'B rotation of A'
                        return sol

        # Check if C is a rotation of A; include both -90 and + 90                    
        x = "A"
        y = "C"
        if Operation.test_rotate( fig_progression, x, y ):
            z = "B.png" # B will be tested against choices
            for fig in fig_progression:
                if z in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_rotate(fig, fig_choice) 
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'C rotationn of A'
                        return sol

        # Check if progression figures are same in shape but different in color    
        #  B == A
        x = "A"
        y = "B"
        if Operation.test_shape( fig_progression, x, y ):
            z = "C.png" # C will be tested against choices
            for fig in fig_progression:
                if z in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_figs_contrast(fig, fig_choice ) 
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'Same Shape / Fill; B == A'
                        return sol
        # C == A
        x = "A"
        y = "C"
        if Operation.test_shape( fig_progression, x, y ):
            z = "B.png" # B will be tested against choices
            for fig in fig_progression:
                if z in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_figs_contrast(fig, fig_choice ) 
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'Same Shape / Fill; C == A'
                        return sol
        # C == B
        x = "B"
        y = "C"
        if Operation.test_shape( fig_progression, x, y ):
            z = "A.png" # A will be tested against choices
            for fig in fig_progression:
                if z in fig.visualFilename:
                    fig_sol = ImgAnalysis.match_figs_contrast(fig, fig_choice )
                    if fig_sol:
                        sol = int(fig_sol[-5]) 
                        solverType = 'Same Shape / Fill; C == B'
                        return sol

        # Check for addition and subtraction between Fig A and B
        x = "A"
        y = "B"
        z = "C" # C will be tested against choices
        if Operation.test_add_sub( fig_progression, fig_choice, x, y, z ):
            for fig in fig_choice:
                fig_sol = Operation.test_add_sub( fig_progression, fig_choice, x, y, z )[1]        
                sol = int(fig_sol[-5]) 
                solverType = 'Add/Sub; A/B'
                return sol                           

        # Check for addition and subtraction between Fig A and C
        x = "A"
        y = "C"
        z = "B" # C will be tested against choices
        if Operation.test_add_sub( fig_progression, fig_choice, x, y, z ):
            print("true")
            for fig in fig_choice:
                fig_sol = Operation.test_add_sub( fig_progression, fig_choice, x, y, z )[1]        
                sol = int(fig_sol[-5]) 
                solverType = 'Add/Sub; A/C'
                return sol        

        return -1

    def threeXthree(problem,fig_progression,fig_choice):

        return -1
       
######################################################################
class Operation:
######################################################################
    def __init__(self):
        pass

    # A = all?
    def test_equal_all(fig_progression):
        cell_images = []
        for fig in fig_progression:
            figID = fig.visualFilename
            figureImage = Image.open(figID)
            cell_images.append(figureImage)
            for i in range(len(cell_images)-1):
                # print(ImgAnalysis.diff_rms(cell_images[i], cell_images[i+1]))
                if not ImgAnalysis.diff_rms(cell_images[i], cell_images[i+1]) >= 900:
                    return True
                else:
                    return False    

    # A = B?
    def test_equal_AB(fig_progression):
        cell_images = {}
        for fig in fig_progression:
            figID = fig.visualFilename
            figureImage = Image.open(figID)
            cell_images[figID[-5]] = figureImage
        if ImgAnalysis.diff_rms(cell_images['A'], cell_images['B']) >= 900:
            return False
        else:
            return True

    # A = C?
    def test_equal_AC(fig_progression):
        cell_images = {}
        for fig in fig_progression:
            fileName = fig.visualFilename
            figureImage = Image.open(fileName)
            cell_images[fileName[-5]] = figureImage
        if ImgAnalysis.diff_rms(cell_images['A'], cell_images['C']) >= 965:
            return False
        else:
            return True

    # B is a mirror of A?
    def test_mirrir_AB(fig_progression):
        cell_images = {}
        for fig in fig_progression:
            figID = fig.visualFilename
            figureImage = Image.open(figID)
            cell_images[figID[-5]] = figureImage
        if ImgAnalysis.diff_rms(cell_images['A'].transpose(Image.FLIP_LEFT_RIGHT), cell_images['B']) >= 965:
            return False
        else:
            return True            

    # C is a mirror of A?
    def test_mirrir_AC(fig_progression):
        cell_images = {}
        for fig in fig_progression:
            figID = fig.visualFilename
            figureImage = Image.open(figID)
            cell_images[figID[-5]] = figureImage
        if ImgAnalysis.diff_rms(cell_images['A'].transpose(Image.FLIP_TOP_BOTTOM), cell_images['C']) >= 965:
            return False
        else:
            return True          

    # X is a rotation of Y?
    def test_rotate(fig_progression, x, y):
        global deg
        cell_images = {}
        for fig in fig_progression:
            figID = fig.visualFilename
            figureImage = Image.open(figID)
            cell_images[figID[-5]] = figureImage
        if (ImgAnalysis.diff_rms(cell_images[x].transpose(Image.ROTATE_90), cell_images[y]) >= 965) or \
                (ImgAnalysis.diff_rms(cell_images[x].transpose(Image.ROTATE_270), cell_images[y]) >= 1000):
            deg = 0
            return False
        elif (ImgAnalysis.diff_rms(cell_images[x].transpose(Image.ROTATE_90), cell_images[y]) < 1000):
            deg = 90
            return True
        elif (ImgAnalysis.diff_rms(cell_images[x].transpose(Image.ROTATE_270), cell_images[y]) < 1000):
            deg = 270
            return True

    # B == A in shape, but filled in color
    # first test whether the shape is correct
    def test_shape(fig_progression, x, y):
        cell_images = {}
        for fig in fig_progression:
            figID = fig.visualFilename
            figureImage = Image.open(figID).convert("L")
            figEdges = figureImage.filter(ImageFilter.FIND_EDGES)
            cell_images[figID[-5]] = figEdges
        if ImgAnalysis.diff_rms(cell_images[x], cell_images[y]) >= 100:
            return False
        else:
            return True      

    # check for addition / subtraction
    def test_add_sub(fig_progression, fig_choice, x, y, z):
        cell_images = {}
        for fig in fig_progression:
            figID = fig.visualFilename
            figureImage = Image.open(figID).convert("1")
            cell_images[figID[-5]] = figureImage

        # x - y
        diff = ImageChops.difference(cell_images[x],cell_images[y])
        diff = ImageOps.invert(diff.convert('RGB'))
        # diff.show()
        # (x-y) + z
        tmp = cell_images[z].convert('RGB')
        # tmp.show()
        new = ImageChops.difference(tmp, diff)
        new = ImageOps.invert(new.convert('RGB'))
        # new.show()

        # test available choices
        for fig in fig_choice:
            state = False
            figID = fig.visualFilename
            figureImage = Image.open(figID).convert('RGB')
            # need to compare both edge / fill using subtraction
            # print(ImgAnalysis.diff_rms(new, figureImage))
            if ImgAnalysis.diff_rms(new, figureImage) < 600:
                state = True
                return state, figID


######################################################################
class ImgAnalysis:
######################################################################
    def __init__(self):
        pass    

    def equal_images(image1, image2):
        return ImageChops.difference(image1, image2).getbbox() is None

    def diff_rms(image1, image2):
        h = ImageChops.difference(image1, image2).histogram()
        sq = sum(value*(idx**2) for idx, value in enumerate(h))
        diff_rms = math.sqrt(sq/float(image1.size[0] * image2.size[1]))
        return diff_rms     

    def diff_dice(image1, image2):
        a = np.unpackbits(np.asarray(image1))
        b = np.unpackbits(np.asarray(image2))
        both = np.sum(a == b)
        onlyA = np.sum(a!=b)
        onlyB = np.sum(b!=a)
        diff_dice = 2*both/(onlyA+onlyB+2*both)
        return diff_dice       

    def match_figs(fig_progression, fig_choice):
        fig_progress = Image.open(fig_progression.visualFilename)
        # dx = {}
        for ii, fig in enumerate(fig_choice):
            figID = fig.visualFilename
            figureImage = Image.open(figID)
            # dx[ii] = [figID, ImgAnalysis.diff_rms(fig_progress, figureImage)]
            if ImgAnalysis.diff_rms(fig_progress, figureImage) < 965:
                return figID

    def match_mirror_y(fig_progression, fig_choice):
        fig_progress = Image.open(fig_progression.visualFilename).transpose(Image.FLIP_LEFT_RIGHT)
        for fig in fig_choice:
            figID = fig.visualFilename
            figureImage = Image.open(figID)
            if ImgAnalysis.diff_rms(fig_progress, figureImage) < 965:
                return figID

    def match_mirror_x(fig_progression, fig_choice):
        fig_progress = Image.open(fig_progression.visualFilename).transpose(Image.FLIP_TOP_BOTTOM)
        for figure in fig_choice:
            figID = figure.visualFilename
            figureImage = Image.open(figID)
            if ImgAnalysis.diff_rms(fig_progress, figureImage) < 965:
                return figID

    def match_rotate(fig_progression, fig_choice):
        fig_progress_90 = Image.open(fig_progression.visualFilename).transpose(Image.ROTATE_90)
        fig_progress_270 = Image.open(fig_progression.visualFilename).transpose(Image.ROTATE_270)
        for figure in fig_choice:
            figID = figure.visualFilename
            figureImage = Image.open(figID)
            if ( ImgAnalysis.diff_rms(figureImage, fig_progress_90) < 1000 ) or \
                ( ImgAnalysis.diff_rms(figureImage, fig_progress_270) < 1000 ):
                return figID

    def match_figs_contrast(fig_progression, fig_choice):
        fig_progress = Image.open(fig_progression.visualFilename).convert('RGB')
        ImageDraw.floodfill(fig_progress,xy=(0,0),value=(255,0,255))
        # Make everything not magenta black
        n  = np.array(fig_progress)
        n[(n[:, :, 0:3] != [255,0,255]).any(2)] = [0,0,0]
        # Revert all artifically filled magenta pixels to white
        n[(n[:, :, 0:3] == [255,0,255]).all(2)] = [255,255,255]
        fig_progress= Image.fromarray(n).convert('L')
        for fig in fig_choice:
            figID = fig.visualFilename
            figureImage = Image.open(figID).convert('L')
            # figureImage.show()
            # diff = ImageChops.difference(figureImage,fig_progress)
            # diff.show() 
            diff = ImageChops.subtract_modulo(fig_progress,figureImage)
            # need to compare both edge / fill using subtraction
            if( np.amax(diff) < 10 ):
                return figID


