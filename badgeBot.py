
"""
########
BadgeBot
########
by David Jonathan Ross
based on a design by Nick Sherman
Coded using Drawbot <http://drawbot.readthedocs.org> and, of course, Input <http://input.fontbureau.com>

It makes badges for awesome conferences, like @TypographicsNYC!
Learn more: <http://djr.com/misc/typographicsbadge>

This was designed to be used with Stilla SH <https://www.myfonts.com/fonts/efscangraphic/stilla-sh/>
Few typefaces will match its funkiness. If you use a different typeface, it just won't be the same, 
and you may have to tweak things to get it looking right.

I'll be the first to admit that this is quick and dirty, and stuff like how to pass variables
has not been totally thought through. But I hope you find it useful and/or interesting!
"""

import string
import random
import csv
import os

## VARIABLES
pt = 72
w = 4 * pt
h = 3 * pt

# RGB colors for screen viewing, otherwise, use CMYK
d = 255
textColor = 252/d, 15/d, 60/d, 1
backgroundColor = 27/d, 161/d, 236/d, 1
frameColor = 254/d, 223/d, 53/d, 1

# define fonts. 
nameFont = 'StillaSHOP-Regular'
companyFont = 'StorkText-Regular'

# since you probably don't have Stilla or my unpublished font, use Georgia as a fallback
if nameFont not in installedFonts():
    nameFont = 'Georgia-BoldItalic'
if companyFont not in installedFonts():
    companyFont = 'Georgia'

# We use this to add space between the lines. This list is made for Stilla.
# It may be different for other fonts!
descenders = ['Q', 'J', 'f', 'g', 'j', 'p', 'q', 'y', 'z']

# Set default space we will add between lines. 
# We are doing some funky stuff so we won't use the normal lineHeight function
lineSpace = 9
  
## HELPERS

def fillColor(c):
    """
    a helper function that processes rgba or cymka tuples. 
    I use this because I hate having to switch back and forth between
    color spaces, and splitting up colors from tuples each time.
    """
    if len(c) == 5:
        cmykFill(c[0], c[1], c[2], c[3], c[4])
    elif len(c) == 4:
        fill(c[0], c[1], c[2], c[3])
    else:
        fill(c[0], c[1], c[2])


## BADGE FUNCTIONS

def drawBackground(w, h):
    """
    draw a rectangle that is a background
    """
    fillColor(backgroundColor)
    rect(0, 0, w, h)

def drawFrame(frameWidth, frameHeight, numberOfPointsMin=4, numberofPointsMax=6, perpindicularRandomness=2, parallelRandomness=10):
    """
    make a box with random jagginess
    """
    # for goodness sake make these variables shorter
    pdr = perpindicularRandomness
    plr = parallelRandomness
    # get the number of segments to use
    segments = random.randrange(numberOfPointsMin, numberofPointsMax)
    # draw the path, one direction at a time. Loop through the segment, and.
    # we have to subtract from segments so we don't hit the shared corners twice.
    fillColor(frameColor)
    newPath()
    moveTo((0, 0))
    for i in range(segments-1):
        lineTo( ( 0+random.randrange(-pdr, pdr) , (i+1)*frameHeight/segments + random.randrange(-plr, plr) ) )    
    lineTo((0, frameHeight))
    for i in range(segments-1):
        lineTo( ( (i+1)*frameWidth/segments + random.randrange(-plr, plr) , frameHeight+random.randrange(-pdr, pdr) ) )
    lineTo((frameWidth, frameHeight))
    for i in range(segments-2, 0, -1):
        lineTo( ( frameWidth+random.randrange(-pdr, pdr) , (i+1)*frameHeight/segments + random.randrange(-plr, plr) ) )
    lineTo((frameWidth, 0))
    for i in range(segments-2, 0, -1):
        lineTo( ( (i+1)*frameWidth/segments + random.randrange(-plr, plr) , 0+random.randrange(-pdr, pdr) ) )
    closePath()
    drawPath()

def drawCompany(company, companySize, companyWidth, companyHeight):
    """
    draw the company name, easy peasy.
    """
    font(companyFont, companySize)
    fillColor(backgroundColor)
    textBox(company, (0, 0, companyWidth, companyHeight), align='center')

def getLinesFromName(name):
    """
    Split a name string into a list of lines
    """
    lines = name.split(' ')
    # Process hyphens without removing them. There has to be an easier way to do this, no?
    newLines = []
    for line in lines:
        if '-' in line:
            lineElements = line.split('-')
            for i, lineElement in enumerate(lineElements): 
                if i != len(lineElements)-1:
                    newLines.append(lineElement+'-')
                else:
                    newLines.append(lineElement)
        else:
            newLines.append(line)
    lines = newLines
    return lines

def drawName(name, boxWidth, boxHeight):
    """
    This function draws the name to fill a box. It could probably be simplified a whole lot.
    It may take some futzing, especially with vertical space, to make this look halfway decent.
    """
    save()
    
    # turn the name string into a list of lines
    lines = getLinesFromName(name)

    #################
    # DRESS REHEARSAL
    #################

    # remember stuff about each line, and also the total text box 
    lineData = []
    totalTextHeight = 0
    
    for i, line in enumerate(lines):
        # this is a little hack we did to words that end in 'f', because of the huge overhang in Stilla
        if line and line[-1] == 'f':
            line += '  '
        # get the font size at 10 point, and then do the math to figure out the multiplier
        font(nameFont)
        fontSize(10)
        lineHeight(6.5)
        textWidth, textHeight = textSize(line)
        m = boxWidth / textWidth
        # set a ceiling for the multiplier
        maximumMultiplier = 10
        if m > maximumMultiplier:
            m = maximumMultiplier            
        # resize the text box based on the multiplier to get the point size
        textWidth, textHeight = textWidth*m, textHeight*m
        pointSize = 10*m
        
        # look for descenders in a line
        hasDescender = False
        extraSpace = 0
        for letter in line:
            if letter in descenders:
                hasDescender = True
                break
        # if there is a descender, add a little extra space
        if hasDescender:
            extraSpace = pointSize * .175
            
        # remember our line data
        lineData.append((line, textWidth, textHeight, pointSize, extraSpace))
        
        # augment the total text count
        totalTextHeight += textHeight
        totalTextHeight += extraSpace
        # if we aren't on the last line, include the line space
        if i != len(lines)-1:
            totalTextHeight += lineSpace
            
    # go to top left
    translate(0, boxHeight)
    
    #################
    # SET VERTICAL ALIGNMENT
    #################
    
    # set vertical height    
    scaleValue = 1
    if boxHeight > totalTextHeight:
        # ideally, center the text box in the space
        verticalOffset = (boxHeight - totalTextHeight)/2
        translate(0, -verticalOffset)
    else:
        # otherwise, scale the whole damn thing down so it fits in the space
        scaleValue = boxHeight / totalTextHeight
        diff = boxWidth - (scaleValue * boxWidth)
        translate(diff/2, 0)
        scale(scaleValue)
        
    #################
    # DRAW THE WORDS!
    #################
    
    # run through our line data
    for i, (lineText, textWidth, textHeight, pointSize, extraSpace) in enumerate(lineData):
        fillColor(textColor)
        fontSize(pointSize)        
        translate(0, -textHeight)
        save()
        translate((boxWidth-textWidth)/2, 0)
        text(lineText, (0, 0))
        restore()
        translate(0, -lineSpace-extraSpace)
    restore()



def drawBadge(name, company=None, w=w, h=h, setSize=True, DEBUG=False):
    """
    Draw one badge. This handles the positioning, and lets other functions do the drawing.
    """
    
    save()
    
    if setSize:
        newPage(w, h)
    
    # set the outside margin to 1/18 of the width, which will surround the frame
    outsideMargin = w/18
    frameWidth = w-outsideMargin*2
    frameHeight = h-outsideMargin*2

    # set the box margins to 1/24 of the width, which will surround the box of text
    topMargin = bottomMargin = leftMargin = rightMargin = w/24
    boxWidth = frameWidth - leftMargin - rightMargin
    boxHeight = frameHeight - topMargin - bottomMargin

    # draw the background
    if backgroundColor:
        drawBackground(w, h)
    
    # move ourselves to the frame margin, and draw the frame
    translate(outsideMargin, outsideMargin)
    drawFrame(frameWidth, frameHeight)

    # print the company name
    companyHeight = h / 7.5
    companySize = h / 18
    # if the company does exist, print that sucker, and then remove some available space
    # if the company doesn't exist, shift up our box a smidge anyway so it's a bit above center
    if company:
        drawCompany(company, companySize, frameWidth, companyHeight)
        boxHeight -= companyHeight
        bottomMargin += companyHeight
    else:
        boxHeight -= companyHeight / 3
        bottomMargin += companyHeight / 3
        
    # move ourselves to the bottom left of the remaining available space
    translate(leftMargin, bottomMargin)
    # draw the available space, in case we want to see it
    if DEBUG:
        fill(.8)
        rect(0, 0, boxWidth, boxHeight)
    
    # draw the name
    drawName(name, boxWidth, boxHeight)
        
    restore()


## SHEET FUNCTIONS

def drawCropMarks(rows, cols, boxWidth, boxHeight, badgeWidth, badgeHeight, margin):
    # assuming we are in the top right, draw crop marks
    save()
    stroke(1)
    for row in range(rows+1):
        line((-margin, -row*badgeHeight), (-margin/2, -row*badgeHeight))
        line((boxWidth+margin, -row*badgeHeight), (boxWidth+margin/2, -row*badgeHeight))
    for col in range(cols+1):
        line((col*badgeWidth, margin), (col*badgeWidth, margin/2))
        line((col*badgeWidth, -boxHeight-margin/2), (col*badgeWidth, -boxHeight-margin))
    restore()

def drawSheets(data, sheetWidth=8.5*pt, sheetHeight=11*pt, badgeWidth=w, badgeHeight=h, margin=.25*pt, multiple=2):
    """
    Make a sheet of badges for printing purposes.
    """
    
    # determine available space
    boxWidth = sheetWidth - margin * 2
    boxHeight = sheetHeight - margin * 2
    # determine number of columns and rows
    cols = int ( boxWidth / badgeWidth )
    rows = int ( boxHeight / badgeHeight )
    
    # reset the box space based on the badge size, rather than the page size
    boxWidth = cols * badgeWidth
    boxHeight = rows * badgeHeight
    
    #setup first page
    newPage(sheetWidth, sheetHeight)
    # fill the sheet with the background color, as a rudimentary bleed
    fillColor(backgroundColor)
    rect(0, 0, sheetWidth, sheetHeight)
    # move to the top left corner, which is where we will start
    translate(margin, sheetHeight-margin)
    # draw crop marks
    drawCropMarks(rows, cols, boxWidth, boxHeight, badgeWidth, badgeHeight, margin)
    # drop down to the bottom left corner to draw the badges
    translate(0, -badgeHeight)
        
    # loop through data
    rowTick = 0
    colTick = 0
    for i, (name, company) in enumerate(data):
        for m in range(multiple):
            # draw the badge without setting the page size
            drawBadge(name, company, setSize=False)
            translate(badgeWidth, 0)
    
            # if we have made it to the last column, translate back and start the next one
            if colTick == cols - 1:
                translate(-badgeWidth*cols, 0)
                translate(0, -badgeHeight)
                colTick = 0
                
                # if we have made it to the last row (and there is still more data), start a new page
                if rowTick == rows - 1 and i != len(data) - 1:
                    # setup a new page
                    newPage(sheetWidth, sheetHeight)
                    # fill the sheet with the background color, as a rudimentary bleed
                    fillColor(backgroundColor)
                    rect(0, 0, sheetWidth, sheetHeight)
                    # move to the top left corner, which is where we will start
                    translate(margin, sheetHeight-margin)
                    # draw crop marks
                    drawCropMarks(rows, cols, boxWidth, boxHeight, badgeWidth, badgeHeight, margin)
                    # drop down to the bottom left corner to draw the badges
                    translate(0, -badgeHeight)
                    rowTick = 0
                else:
                    rowTick += 1
            else:
                colTick += 1

## READING DATA

def readDataFromCSV(csvPath):
    """
    populate a list with rows from a csv file
    """
    data = []
    with open(csvPath, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i, row in enumerate(csvreader):
            data.append(row)
    return data


if __name__ == "__main__":

    # Draw a sample sheet
    size(w, h)
    drawBadge(
        'First Name Last Name', 
        'Company', 
        w=w, 
        h=h,
        setSize=False
        )

    # load data from a csv
    basePath = os.path.split(__file__)[0]
    csvPath = os.path.join(basePath, 'data.csv')
    data = readDataFromCSV(csvPath)

    # if you don't feel like loading data from a file, 
    # you can just make a list of tuples like this one:
    #data = [('David Jonathan Ross', 'The Font Bureau, Inc.')]

    # let's draw some sheets.
    # Since we are not double-sided printing, we will print each twice, side-by-side,
    # and fold along the middle.
    drawSheets(data, 
        sheetWidth = 8.5*pt,
        sheetHeight = 11*pt,
        badgeWidth = w,
        badgeHeight = h,
        margin = .25*pt,
        multiple=2
        )
