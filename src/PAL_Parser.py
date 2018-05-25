# ##########################################
#####
#####
############ PAL Parser
#####
#####
###########################################


from src.lexer import tokens
import ply.yacc as yacc
import src.pal as pal
from src import *


def p_init_frame(p):
    'expression : INIT PAREN_L NUMBER COMMA NUMBER PAREN_R'
    if len(pal.framesArray) > 0:
        p[0] = "Initialisation already done."
    else:
        pal.animationWidth = p[3]
        pal.animationHeight = p[5]
        pal.createFrame()
        p[0] = "Frame created with index 0."


def p_create_frame(p):
    'expression : CREATEFRAME'
    pal.createFrame()
    p[0] = "Frame created with index", pal.currentFrame


def p_show(p):
    'expression : SHOW'
    if checkInit(p):
        print("Displaying Frame with index", pal.currentFrame)
        print("Close Preview Window to continue imputing commands.")
        pal.makeCanvas()
        p[0] = "Closed display"


def p_changeFrame(p):
    'expression : CHANGEFRAME PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        if (int(p[3]) < 0) or (len(pal.framesArray) - 1 < int(p[3])):
            p[0] = 'Invalid index'
        else:
            pal.currentFrame = int(p[3])
            p[0] = 'Frame changed to frame in index ', pal.currentFrame


def p_SetBackground(p):
    'expression : SETBACKGROUND PAREN_L IDENTIFIER PERIOD IDENTIFIER PAREN_R'
    if checkInit(p):
        pal.framesArray[pal.currentFrame].setBackground(p[3] + p[4] + p[5])
        p[0] = 'Background created'


def p_MoveBackground(p):
    'expression : MOVEBACKGROUND PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        if pal.framesArray[pal.currentFrame].background is None:
            p[0] = 'background isnt set'
        else:
            pal.framesArray[pal.currentFrame].moveBackground(int(p[3]))
            p[0] = 'Background moved'


# ---------- ASSETS ----------

def p_CreateAsset(p):
    'expression : CREATEASSET PAREN_L IDENTIFIER COMMA IDENTIFIER PERIOD IDENTIFIER PAREN_R'
    if checkInit(p):
        pal.framesArray[pal.currentFrame].addAsset(pal.Asset(p[5] + p[6] + p[7], p[3]))
        p[0] = 'Asset Created with name '


def p_MoveAsset(p):
    'expression : IDENTIFIER MOVEASSET PAREN_L IDENTIFIER COMMA NUMBER COMMA NUMBER PAREN_R'
    if checkInit(p):
        asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
        if asset is None:
            p[0] = 'Asset cant be found'
        else:
            moveMode = p[4]
            if (moveMode != "R") & (moveMode != "A"):
                p[0] = 'Invalid Option, only <R> and <A>'
            elif moveMode == "R":
                asset.move(p[6], p[8])
                p[0] = 'asset moved'
            else:
                asset.moveAbs(p[6], p[8])
                p[0] = 'asset moved'


def p_ResizeAssetAbsolute(p):
    'expression : IDENTIFIER RESIZEASSET ABSOLUTE PAREN_L NUMBER COMMA NUMBER PAREN_R'
    if checkInit(p):
        asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
        if asset is None:
            p[0] = 'Asset cant be found'
        else:
            asset.resizeAsset(int(p[5]), int(p[7]))
            p[0] = 'asset resized'


def p_ResizeAssetMultiplier(p):
    'expression : IDENTIFIER RESIZEASSET MULTIPLIER PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
        if asset is None:
            p[0] = 'Asset cant be found'
        else:
            asset.resizeAssetMultiplier(int(p[5]))
            p[0] = 'asset resized'


def p_RotateAssetRelative(p):
    'expression : IDENTIFIER ROTATEASSET RELATIVE PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
        if asset is None:
            p[0] = 'Asset cant be found'
        else:
            asset.rotate(int(p[5]))
            p[0] = 'asset rotated'


def p_RotateAssetAbsolute(p):
    'expression : IDENTIFIER ROTATEASSET ABSOLUTE PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
        if asset is None:
            p[0] = 'Asset cant be found'
        else:
            asset.rotateAbs(int(p[5]))
            p[0] = 'Sprite rotated'


def p_removeAsset(p):
    'expression : IDENTIFIER REMOVEASSET'
    if checkInit(p):
        asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
        if asset is None:
            p[0] = 'Asset cant be found'
        else:
            pal.framesArray[pal.currentFrame].unloadAsset(asset)
            p[0] = 'asset removed'


# ---------- SPRITES ----------

def p_CreateSprite(p):
    'expression : CREATESPRITE PAREN_L IDENTIFIER COMMA IDENTIFIER PERIOD IDENTIFIER COMMA NUMBER COMMA NUMBER PAREN_R'
    if checkInit(p):
        pal.framesArray[pal.currentFrame].addSprite(pal.Sprite(p[3], p[5] + p[6] + p[7], p[9], p[11]))
        p[0] = 'Sprite Created with name ', p[3]


def p_ChangeSpriteState(p):
    'expression : IDENTIFIER CHANGESPRITESTATE PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
        if sprite is not None:
            if (int(p[4]) < 0) or (len(sprite.spritesArray) - 1 < int(p[4])):
                p[0] = "Invalid index"
            else:
                sprite.changeSelectedSprite(int(p[4]))
                p[0] = "Sprite state changed"
        else:
            p[0] = "Sprite can't be found"


def p_MoveSprite(p):
    'expression : IDENTIFIER MOVESPRITE PAREN_L IDENTIFIER COMMA NUMBER COMMA NUMBER PAREN_R'
    if checkInit(p):
        sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
        if sprite is None:
            p[0] = 'Sprite cant be found'
        else:
            if (p[4] != "R") & (p[4] != "A"):
                p[0] = 'Invalid Option, only <R> and <A>'
            elif p[4] == "R":
                sprite.move(p[6], p[8])
                p[0] = 'Sprite moved'
            else:
                sprite.moveAbs(p[6], p[8])
                p[0] = 'Sprite moved'


def p_ResizeSpriteAbsolute(p):
    'expression : IDENTIFIER RESIZESPRITE ABSOLUTE PAREN_L NUMBER COMMA NUMBER PAREN_R'
    if checkInit(p):
        sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
        if sprite is None:
            p[0] = 'Sprite cant be found'
        else:
            sprite.resizeAsset(p[5], p[7])
            p[0] = 'Sprite resized'


def p_ResizeSpriteMultiplier(p):
    'expression : IDENTIFIER RESIZESPRITE MULTIPLIER PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
        if sprite is None:
            p[0] = 'Sprite cant be found'
        else:
            sprite.resizeAssetMultiplier(p[5])
            p[0] = 'Sprite resized'


def p_RotateSpriteRelative(p):
    'expression : IDENTIFIER ROTATESPRITE RELATIVE PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
        if sprite is None:
            p[0] = 'Asset cant be found'
        else:
            sprite.rotate(int(p[5]))
            p[0] = 'Sprite rotated'


def p_RotateSpriteAbsolute(p):
    'expression : IDENTIFIER ROTATESPRITE ABSOLUTE PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
        if sprite is None:
            p[0] = 'Asset cant be found'
        else:
            sprite.rotateAbs(int(p[5]))
            p[0] = 'Sprite rotated'


def p_removeSprite(p):
    'expression : IDENTIFIER REMOVESPRITE'
    if checkInit(p):
        sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
        if sprite is None:
            p[0] = 'Asset cant be found'
        else:
            pal.framesArray[pal.currentFrame].unloadSprite(sprite)
            p[0] = 'Sprite removed'


def p_CreateAnimation(p):
    'expression : CREATEANIMATION PAREN_L NUMBER PAREN_R'
    if checkInit(p):
        pal.save(p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input", p)


# test
def p_test(p):
    'expression : TEST '
    parser.parse("init (500,480)")
    parser.parse("setBackground (bg.jpg)")
    parser.parse("createSprite (sprt,sprt.png,360,260)")
    parser.parse("sprt moveSprite (R,-90,230)")
    parser.parse("createAsset (fire,fire.png)")
    parser.parse("fire resizeAsset absolute (125,125)")
    parser.parse("fire moveAsset(A,300,350)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt moveSprite (R,50,0)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt changeSpriteState(1)")
    parser.parse("sprt moveSprite (R,20,-15)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-40,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt changeSpriteState(3)")
    parser.parse("sprt moveSprite (R,30,-15)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt moveSprite (R,35,10)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt changeSpriteState(5)")
    parser.parse("sprt moveSprite (R,20,20)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt changeSpriteState(6)")
    parser.parse("sprt moveSprite (R,20,0)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt changeSpriteState(10)")
    parser.parse("sprt moveSprite (R,20,0)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt changeSpriteState(11)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createFrame")
    parser.parse("sprt changeSpriteState(13)")
    parser.parse("moveBackground (-100)")
    parser.parse("fire moveAsset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createAnimation(0.15)")
    p[0] = "finished loading test"


def checkInit(p):
    if len(pal.framesArray) > 0:
        return True
    else:
        p[0] = "Not initialized yet"
        return False


# Build the parser
parser = yacc.yacc()


while True:
    try:
        s = input('Pal > ')
        s.lower()
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
