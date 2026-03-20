#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.1.1),
    on 十一月 25, 2025, at 15:10
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2025.1.1'
expName = 'corsi_blocks'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1440, 900]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='D:\\Desktop\\科研\\25秋\\眼动实验\\cognitiveability\\corsi_blocks-master_new\\corsi_blocks_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('exp')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=True,
            monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [-1, -1, -1]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "instructions" ---
    text = visual.TextStim(win=win, name='text',
        text='在这个游戏里，你需要仔细观察并记住屏幕上方块亮起的顺序。\n\n游戏怎么玩？\n一开始会很简单，只有 3个 方块会按顺序亮起。你的任务就是仔细观察，然后按照同样的顺序点击这些方块。\n只要你答对了，下一次挑战的方块数量就会增加一个，难度会慢慢上升。\n\n每个难度下你有 4 次尝试机会。\n\n准备好了吗？请按任意键或点击屏幕任意位置开始。',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "ISI" ---
    blank = visual.TextStim(win=win, name='blank',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    # Run 'Begin Experiment' code from setLocations
    # start with 3 coloured blocks
    nBlocks = 3
    
    # --- Initialize components for Routine "corsi_present" ---
    blk1_3 = visual.Rect(
        win=win, name='blk1_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-1.0, interpolate=True)
    blk2_3 = visual.Rect(
        win=win, name='blk2_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-2.0, interpolate=True)
    blk3_3 = visual.Rect(
        win=win, name='blk3_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-3.0, interpolate=True)
    blk4_3 = visual.Rect(
        win=win, name='blk4_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-4.0, interpolate=True)
    blk5_3 = visual.Rect(
        win=win, name='blk5_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-5.0, interpolate=True)
    blk6_3 = visual.Rect(
        win=win, name='blk6_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-6.0, interpolate=True)
    blk7_3 = visual.Rect(
        win=win, name='blk7_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-7.0, interpolate=True)
    blk8_3 = visual.Rect(
        win=win, name='blk8_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-8.0, interpolate=True)
    blk9_3 = visual.Rect(
        win=win, name='blk9_3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-9.0, interpolate=True)
    
    # --- Initialize components for Routine "corsi_respond" ---
    blk1 = visual.Rect(
        win=win, name='blk1',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=0.0, interpolate=True)
    blk2 = visual.Rect(
        win=win, name='blk2',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-1.0, interpolate=True)
    blk3 = visual.Rect(
        win=win, name='blk3',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-2.0, interpolate=True)
    blk4 = visual.Rect(
        win=win, name='blk4',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-3.0, interpolate=True)
    blk5 = visual.Rect(
        win=win, name='blk5',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-4.0, interpolate=True)
    blk6 = visual.Rect(
        win=win, name='blk6',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-5.0, interpolate=True)
    blk7 = visual.Rect(
        win=win, name='blk7',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-6.0, interpolate=True)
    blk8 = visual.Rect(
        win=win, name='blk8',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-7.0, interpolate=True)
    blk9 = visual.Rect(
        win=win, name='blk9',units='height', 
        width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
        ori=0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1,
        colorSpace='rgb', lineColor=[1,1,1], fillColor=[1,1,1],
        opacity=1, depth=-8.0, interpolate=True)
    corsi_mouse = event.Mouse(win=win)
    x, y = [None, None]
    corsi_mouse.mouseClock = core.Clock()
    submit_button = visual.TextBox2(
         win, text='Submit', placeholder='Type here...', font='Arial',
         ori=0.0, pos=(0.5, -0.4), draggable=False,      letterHeight=0.05,
         size=(0.2, 0.1), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor='darkgrey', borderColor=None,
         flipHoriz=False, flipVert=False, languageStyle='LTR',
         editable=False,
         name='submit_button',
         depth=-11, autoLog=True,
    )
    
    # --- Initialize components for Routine "feedback" ---
    fbtxt = visual.TextStim(win=win, name='fbtxt',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    # Run 'Begin Experiment' code from end_task
    incorrect_count = 0
    
    # --- Initialize components for Routine "end" ---
    text_2 = visual.TextStim(win=win, name='text_2',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "instructions" ---
    # create an object to store info about Routine instructions
    instructions = data.Routine(
        name='instructions',
        components=[text, key_resp, mouse],
    )
    instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # setup some python lists for storing info about the mouse
    mouse.x = []
    mouse.y = []
    mouse.leftButton = []
    mouse.midButton = []
    mouse.rightButton = []
    mouse.time = []
    gotValidClick = False  # until a click is received
    # store start times for instructions
    instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructions.tStart = globalClock.getTime(format='float')
    instructions.status = STARTED
    thisExp.addData('instructions.started', instructions.tStart)
    instructions.maxDuration = None
    # keep track of which components have finished
    instructionsComponents = instructions.components
    for thisComponent in instructions.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instructions" ---
    instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        # *mouse* updates
        
        # if mouse is starting this frame...
        if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse.frameNStart = frameN  # exact frame index
            mouse.tStart = t  # local t and not account for scr refresh
            mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse.started', t)
            # update status
            mouse.status = STARTED
            mouse.mouseClock.reset()
            prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
        if mouse.status == STARTED:  # only update if started and not finished!
            buttons = mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    pass
                    x, y = mouse.getPos()
                    mouse.x.append(x)
                    mouse.y.append(y)
                    buttons = mouse.getPressed()
                    mouse.leftButton.append(buttons[0])
                    mouse.midButton.append(buttons[1])
                    mouse.rightButton.append(buttons[2])
                    mouse.time.append(mouse.mouseClock.getTime())
                    
                    continueRoutine = False  # end routine on response
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=instructions,
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instructions.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructions" ---
    for thisComponent in instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructions
    instructions.tStop = globalClock.getTime(format='float')
    instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructions.stopped', instructions.tStop)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
        thisExp.addData('key_resp.duration', key_resp.duration)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('mouse.x', mouse.x)
    thisExp.addData('mouse.y', mouse.y)
    thisExp.addData('mouse.leftButton', mouse.leftButton)
    thisExp.addData('mouse.midButton', mouse.midButton)
    thisExp.addData('mouse.rightButton', mouse.rightButton)
    thisExp.addData('mouse.time', mouse.time)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    corsi_task = data.TrialHandler2(
        name='corsi_task',
        nReps=1000.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(corsi_task)  # add the loop to the experiment
    thisCorsi_task = corsi_task.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisCorsi_task.rgb)
    if thisCorsi_task != None:
        for paramName in thisCorsi_task:
            globals()[paramName] = thisCorsi_task[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisCorsi_task in corsi_task:
        corsi_task.status = STARTED
        if hasattr(thisCorsi_task, 'status'):
            thisCorsi_task.status = STARTED
        currentLoop = corsi_task
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisCorsi_task.rgb)
        if thisCorsi_task != None:
            for paramName in thisCorsi_task:
                globals()[paramName] = thisCorsi_task[paramName]
        
        # --- Prepare to start Routine "ISI" ---
        # create an object to store info about Routine ISI
        ISI = data.Routine(
            name='ISI',
            components=[blank],
        )
        ISI.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from setLocations
        # create 9 blocks that shows sequence
        blocks = [blk1_3, blk2_3, blk3_3, blk4_3, blk5_3, blk6_3, blk7_3, blk8_3, blk9_3]
        
        # create 9 response blocks
        respond_blocks = [blk1, blk2, blk3, blk4, blk5, blk6, blk7, blk8, blk9]
        
        # set the required number of blocks to visible
        block_order = [] 
        correct_order = [] 
        respond_block_order = []
        for block in range(nBlocks):
            blocks[block].setColor('white')
            respond_blocks[block].setColor('white')
            # responses will be saved as string so we need the correct answer to be in string format
            correct_order.append(respond_blocks[block].name)
            # populate list with coloured block sequence
            block_order.append(blocks[block]) 
            respond_block_order.append(respond_blocks[block])
        # set the position of blocks to be random
        # preset some random locations so that the boxes never overlap
        xys = [[0.25625, 0.0975], [0.0675, 0.07375], [-0.09875, 0.065], [-0.26625, 0.235], [0.22, 0.2425], [0.16625, 0.3825], [-0.18625, 0.41125], [-0.01875, 0.235], [-0.3575, -0.05625], [-0.12125, -0.12625], [0.05875, -0.0575], [0.19375, -0.17125], [0.30125, -0.0175], [0.4125, -0.1325], [0.365, -0.27625], [-0.01125, -0.295], [-0.285, -0.27125], [-0.4075, 0.11875], [-0.485, 0.34625], [0.4625, 0.35875], [0.45375, 0.175], [0.54, 0.03625], [0.62875, -0.1825], [0.57875, -0.31375], [-0.45875, -0.3], [-0.55125, -0.13375], [-0.6025, 0.0725], [-0.675, 0.29875], [-0.68625, -0.225], [0.03125, -0.41], [0.1925, -0.295], [-0.16125, -0.28], [-0.24625, 0.04375], [-0.0225, 0.395], [0.28875, 0.39875], [0.6375, 0.27375], [-0.35125, 0.36625]]
        
        # randomise the coordinates
        shuffle(xys)
        count = 0 # used to iterate through list
        positions = []
        for block in blocks:
            # keep the same block positions
            block.setPos([xys[count][0], xys[count][1]])
            respond_blocks[count].setPos([xys[count][0], xys[count][1]])
            
            positions.append(xys[count])
            
            count += 1
        
        # save positions used to csv output
        thisExp.addData('positions', positions)
        # store start times for ISI
        ISI.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        ISI.tStart = globalClock.getTime(format='float')
        ISI.status = STARTED
        thisExp.addData('ISI.started', ISI.tStart)
        ISI.maxDuration = None
        # keep track of which components have finished
        ISIComponents = ISI.components
        for thisComponent in ISI.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "ISI" ---
        ISI.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # if trial has changed, end Routine now
            if hasattr(thisCorsi_task, 'status') and thisCorsi_task.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blank* updates
            
            # if blank is starting this frame...
            if blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blank.frameNStart = frameN  # exact frame index
                blank.tStart = t  # local t and not account for scr refresh
                blank.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blank, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blank.started')
                # update status
                blank.status = STARTED
                blank.setAutoDraw(True)
            
            # if blank is active this frame...
            if blank.status == STARTED:
                # update params
                pass
            
            # if blank is stopping this frame...
            if blank.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > blank.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    blank.tStop = t  # not accounting for scr refresh
                    blank.tStopRefresh = tThisFlipGlobal  # on global time
                    blank.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blank.stopped')
                    # update status
                    blank.status = FINISHED
                    blank.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=ISI,
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                ISI.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ISI.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ISI" ---
        for thisComponent in ISI.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for ISI
        ISI.tStop = globalClock.getTime(format='float')
        ISI.tStopRefresh = tThisFlipGlobal
        thisExp.addData('ISI.stopped', ISI.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if ISI.maxDurationReached:
            routineTimer.addTime(-ISI.maxDuration)
        elif ISI.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        
        # set up handler to look after randomisation of conditions etc
        block_sequence = data.TrialHandler2(
            name='block_sequence',
            nReps=nBlocks, 
            method='random', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
        )
        thisExp.addLoop(block_sequence)  # add the loop to the experiment
        thisBlock_sequence = block_sequence.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisBlock_sequence.rgb)
        if thisBlock_sequence != None:
            for paramName in thisBlock_sequence:
                globals()[paramName] = thisBlock_sequence[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisBlock_sequence in block_sequence:
            block_sequence.status = STARTED
            if hasattr(thisBlock_sequence, 'status'):
                thisBlock_sequence.status = STARTED
            currentLoop = block_sequence
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisBlock_sequence.rgb)
            if thisBlock_sequence != None:
                for paramName in thisBlock_sequence:
                    globals()[paramName] = thisBlock_sequence[paramName]
            
            # --- Prepare to start Routine "corsi_present" ---
            # create an object to store info about Routine corsi_present
            corsi_present = data.Routine(
                name='corsi_present',
                components=[blk1_3, blk2_3, blk3_3, blk4_3, blk5_3, blk6_3, blk7_3, blk8_3, blk9_3],
            )
            corsi_present.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from setColor
            # set the block to red
            block_order[block_sequence.thisN].fillColor = [1, 0, 0]
            print(block_order[block_sequence.thisN].pos)
            print(block_order[block_sequence.thisN].opacity)
            # store start times for corsi_present
            corsi_present.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            corsi_present.tStart = globalClock.getTime(format='float')
            corsi_present.status = STARTED
            thisExp.addData('corsi_present.started', corsi_present.tStart)
            corsi_present.maxDuration = None
            # keep track of which components have finished
            corsi_presentComponents = corsi_present.components
            for thisComponent in corsi_present.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "corsi_present" ---
            corsi_present.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 0.5:
                # if trial has changed, end Routine now
                if hasattr(thisBlock_sequence, 'status') and thisBlock_sequence.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *blk1_3* updates
                
                # if blk1_3 is starting this frame...
                if blk1_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk1_3.frameNStart = frameN  # exact frame index
                    blk1_3.tStart = t  # local t and not account for scr refresh
                    blk1_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk1_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk1_3.started')
                    # update status
                    blk1_3.status = STARTED
                    blk1_3.setAutoDraw(True)
                
                # if blk1_3 is active this frame...
                if blk1_3.status == STARTED:
                    # update params
                    pass
                
                # if blk1_3 is stopping this frame...
                if blk1_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk1_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk1_3.tStop = t  # not accounting for scr refresh
                        blk1_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk1_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk1_3.stopped')
                        # update status
                        blk1_3.status = FINISHED
                        blk1_3.setAutoDraw(False)
                
                # *blk2_3* updates
                
                # if blk2_3 is starting this frame...
                if blk2_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk2_3.frameNStart = frameN  # exact frame index
                    blk2_3.tStart = t  # local t and not account for scr refresh
                    blk2_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk2_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk2_3.started')
                    # update status
                    blk2_3.status = STARTED
                    blk2_3.setAutoDraw(True)
                
                # if blk2_3 is active this frame...
                if blk2_3.status == STARTED:
                    # update params
                    pass
                
                # if blk2_3 is stopping this frame...
                if blk2_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk2_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk2_3.tStop = t  # not accounting for scr refresh
                        blk2_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk2_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk2_3.stopped')
                        # update status
                        blk2_3.status = FINISHED
                        blk2_3.setAutoDraw(False)
                
                # *blk3_3* updates
                
                # if blk3_3 is starting this frame...
                if blk3_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk3_3.frameNStart = frameN  # exact frame index
                    blk3_3.tStart = t  # local t and not account for scr refresh
                    blk3_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk3_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk3_3.started')
                    # update status
                    blk3_3.status = STARTED
                    blk3_3.setAutoDraw(True)
                
                # if blk3_3 is active this frame...
                if blk3_3.status == STARTED:
                    # update params
                    pass
                
                # if blk3_3 is stopping this frame...
                if blk3_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk3_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk3_3.tStop = t  # not accounting for scr refresh
                        blk3_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk3_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk3_3.stopped')
                        # update status
                        blk3_3.status = FINISHED
                        blk3_3.setAutoDraw(False)
                
                # *blk4_3* updates
                
                # if blk4_3 is starting this frame...
                if blk4_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk4_3.frameNStart = frameN  # exact frame index
                    blk4_3.tStart = t  # local t and not account for scr refresh
                    blk4_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk4_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk4_3.started')
                    # update status
                    blk4_3.status = STARTED
                    blk4_3.setAutoDraw(True)
                
                # if blk4_3 is active this frame...
                if blk4_3.status == STARTED:
                    # update params
                    pass
                
                # if blk4_3 is stopping this frame...
                if blk4_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk4_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk4_3.tStop = t  # not accounting for scr refresh
                        blk4_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk4_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk4_3.stopped')
                        # update status
                        blk4_3.status = FINISHED
                        blk4_3.setAutoDraw(False)
                
                # *blk5_3* updates
                
                # if blk5_3 is starting this frame...
                if blk5_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk5_3.frameNStart = frameN  # exact frame index
                    blk5_3.tStart = t  # local t and not account for scr refresh
                    blk5_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk5_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk5_3.started')
                    # update status
                    blk5_3.status = STARTED
                    blk5_3.setAutoDraw(True)
                
                # if blk5_3 is active this frame...
                if blk5_3.status == STARTED:
                    # update params
                    pass
                
                # if blk5_3 is stopping this frame...
                if blk5_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk5_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk5_3.tStop = t  # not accounting for scr refresh
                        blk5_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk5_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk5_3.stopped')
                        # update status
                        blk5_3.status = FINISHED
                        blk5_3.setAutoDraw(False)
                
                # *blk6_3* updates
                
                # if blk6_3 is starting this frame...
                if blk6_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk6_3.frameNStart = frameN  # exact frame index
                    blk6_3.tStart = t  # local t and not account for scr refresh
                    blk6_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk6_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk6_3.started')
                    # update status
                    blk6_3.status = STARTED
                    blk6_3.setAutoDraw(True)
                
                # if blk6_3 is active this frame...
                if blk6_3.status == STARTED:
                    # update params
                    pass
                
                # if blk6_3 is stopping this frame...
                if blk6_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk6_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk6_3.tStop = t  # not accounting for scr refresh
                        blk6_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk6_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk6_3.stopped')
                        # update status
                        blk6_3.status = FINISHED
                        blk6_3.setAutoDraw(False)
                
                # *blk7_3* updates
                
                # if blk7_3 is starting this frame...
                if blk7_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk7_3.frameNStart = frameN  # exact frame index
                    blk7_3.tStart = t  # local t and not account for scr refresh
                    blk7_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk7_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk7_3.started')
                    # update status
                    blk7_3.status = STARTED
                    blk7_3.setAutoDraw(True)
                
                # if blk7_3 is active this frame...
                if blk7_3.status == STARTED:
                    # update params
                    pass
                
                # if blk7_3 is stopping this frame...
                if blk7_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk7_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk7_3.tStop = t  # not accounting for scr refresh
                        blk7_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk7_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk7_3.stopped')
                        # update status
                        blk7_3.status = FINISHED
                        blk7_3.setAutoDraw(False)
                
                # *blk8_3* updates
                
                # if blk8_3 is starting this frame...
                if blk8_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk8_3.frameNStart = frameN  # exact frame index
                    blk8_3.tStart = t  # local t and not account for scr refresh
                    blk8_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk8_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk8_3.started')
                    # update status
                    blk8_3.status = STARTED
                    blk8_3.setAutoDraw(True)
                
                # if blk8_3 is active this frame...
                if blk8_3.status == STARTED:
                    # update params
                    pass
                
                # if blk8_3 is stopping this frame...
                if blk8_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk8_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk8_3.tStop = t  # not accounting for scr refresh
                        blk8_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk8_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk8_3.stopped')
                        # update status
                        blk8_3.status = FINISHED
                        blk8_3.setAutoDraw(False)
                
                # *blk9_3* updates
                
                # if blk9_3 is starting this frame...
                if blk9_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    blk9_3.frameNStart = frameN  # exact frame index
                    blk9_3.tStart = t  # local t and not account for scr refresh
                    blk9_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(blk9_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blk9_3.started')
                    # update status
                    blk9_3.status = STARTED
                    blk9_3.setAutoDraw(True)
                
                # if blk9_3 is active this frame...
                if blk9_3.status == STARTED:
                    # update params
                    pass
                
                # if blk9_3 is stopping this frame...
                if blk9_3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > blk9_3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        blk9_3.tStop = t  # not accounting for scr refresh
                        blk9_3.tStopRefresh = tThisFlipGlobal  # on global time
                        blk9_3.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'blk9_3.stopped')
                        # update status
                        blk9_3.status = FINISHED
                        blk9_3.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=corsi_present,
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    corsi_present.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in corsi_present.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "corsi_present" ---
            for thisComponent in corsi_present.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for corsi_present
            corsi_present.tStop = globalClock.getTime(format='float')
            corsi_present.tStopRefresh = tThisFlipGlobal
            thisExp.addData('corsi_present.stopped', corsi_present.tStop)
            # Run 'End Routine' code from setColor
            # reset the block colour
            block_order[block_sequence.thisN].fillColor = [1, 1, 1]
            
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if corsi_present.maxDurationReached:
                routineTimer.addTime(-corsi_present.maxDuration)
            elif corsi_present.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-0.500000)
            # mark thisBlock_sequence as finished
            if hasattr(thisBlock_sequence, 'status'):
                thisBlock_sequence.status = FINISHED
            # if awaiting a pause, pause now
            if block_sequence.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                block_sequence.status = STARTED
            thisExp.nextEntry()
            
        # completed nBlocks repeats of 'block_sequence'
        block_sequence.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "corsi_respond" ---
        # create an object to store info about Routine corsi_respond
        corsi_respond = data.Routine(
            name='corsi_respond',
            components=[blk1, blk2, blk3, blk4, blk5, blk6, blk7, blk8, blk9, corsi_mouse, submit_button],
        )
        corsi_respond.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the corsi_mouse
        corsi_mouse.x = []
        corsi_mouse.y = []
        corsi_mouse.leftButton = []
        corsi_mouse.midButton = []
        corsi_mouse.rightButton = []
        corsi_mouse.time = []
        corsi_mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        # Run 'Begin Routine' code from check_correct
        # list to keep track which blocks was clicked
        order_clicked = []
        
        # attribute to show the Submit button
        show = False
        
        submit_button.reset()
        # store start times for corsi_respond
        corsi_respond.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        corsi_respond.tStart = globalClock.getTime(format='float')
        corsi_respond.status = STARTED
        thisExp.addData('corsi_respond.started', corsi_respond.tStart)
        corsi_respond.maxDuration = None
        # keep track of which components have finished
        corsi_respondComponents = corsi_respond.components
        for thisComponent in corsi_respond.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "corsi_respond" ---
        corsi_respond.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisCorsi_task, 'status') and thisCorsi_task.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blk1* updates
            
            # if blk1 is starting this frame...
            if blk1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk1.frameNStart = frameN  # exact frame index
                blk1.tStart = t  # local t and not account for scr refresh
                blk1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk1.started')
                # update status
                blk1.status = STARTED
                blk1.setAutoDraw(True)
            
            # if blk1 is active this frame...
            if blk1.status == STARTED:
                # update params
                pass
            
            # *blk2* updates
            
            # if blk2 is starting this frame...
            if blk2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk2.frameNStart = frameN  # exact frame index
                blk2.tStart = t  # local t and not account for scr refresh
                blk2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk2.started')
                # update status
                blk2.status = STARTED
                blk2.setAutoDraw(True)
            
            # if blk2 is active this frame...
            if blk2.status == STARTED:
                # update params
                pass
            
            # *blk3* updates
            
            # if blk3 is starting this frame...
            if blk3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk3.frameNStart = frameN  # exact frame index
                blk3.tStart = t  # local t and not account for scr refresh
                blk3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk3.started')
                # update status
                blk3.status = STARTED
                blk3.setAutoDraw(True)
            
            # if blk3 is active this frame...
            if blk3.status == STARTED:
                # update params
                pass
            
            # *blk4* updates
            
            # if blk4 is starting this frame...
            if blk4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk4.frameNStart = frameN  # exact frame index
                blk4.tStart = t  # local t and not account for scr refresh
                blk4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk4.started')
                # update status
                blk4.status = STARTED
                blk4.setAutoDraw(True)
            
            # if blk4 is active this frame...
            if blk4.status == STARTED:
                # update params
                pass
            
            # *blk5* updates
            
            # if blk5 is starting this frame...
            if blk5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk5.frameNStart = frameN  # exact frame index
                blk5.tStart = t  # local t and not account for scr refresh
                blk5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk5.started')
                # update status
                blk5.status = STARTED
                blk5.setAutoDraw(True)
            
            # if blk5 is active this frame...
            if blk5.status == STARTED:
                # update params
                pass
            
            # *blk6* updates
            
            # if blk6 is starting this frame...
            if blk6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk6.frameNStart = frameN  # exact frame index
                blk6.tStart = t  # local t and not account for scr refresh
                blk6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk6, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk6.started')
                # update status
                blk6.status = STARTED
                blk6.setAutoDraw(True)
            
            # if blk6 is active this frame...
            if blk6.status == STARTED:
                # update params
                pass
            
            # *blk7* updates
            
            # if blk7 is starting this frame...
            if blk7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk7.frameNStart = frameN  # exact frame index
                blk7.tStart = t  # local t and not account for scr refresh
                blk7.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk7, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk7.started')
                # update status
                blk7.status = STARTED
                blk7.setAutoDraw(True)
            
            # if blk7 is active this frame...
            if blk7.status == STARTED:
                # update params
                pass
            
            # *blk8* updates
            
            # if blk8 is starting this frame...
            if blk8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk8.frameNStart = frameN  # exact frame index
                blk8.tStart = t  # local t and not account for scr refresh
                blk8.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk8, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk8.started')
                # update status
                blk8.status = STARTED
                blk8.setAutoDraw(True)
            
            # if blk8 is active this frame...
            if blk8.status == STARTED:
                # update params
                pass
            
            # *blk9* updates
            
            # if blk9 is starting this frame...
            if blk9.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk9.frameNStart = frameN  # exact frame index
                blk9.tStart = t  # local t and not account for scr refresh
                blk9.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk9, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk9.started')
                # update status
                blk9.status = STARTED
                blk9.setAutoDraw(True)
            
            # if blk9 is active this frame...
            if blk9.status == STARTED:
                # update params
                pass
            # *corsi_mouse* updates
            
            # if corsi_mouse is starting this frame...
            if corsi_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                corsi_mouse.frameNStart = frameN  # exact frame index
                corsi_mouse.tStart = t  # local t and not account for scr refresh
                corsi_mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(corsi_mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('corsi_mouse.started', t)
                # update status
                corsi_mouse.status = STARTED
                corsi_mouse.mouseClock.reset()
                prevButtonState = corsi_mouse.getPressed()  # if button is down already this ISN'T a new click
            if corsi_mouse.status == STARTED:  # only update if started and not finished!
                buttons = corsi_mouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        clickableList = environmenttools.getFromNames([blk1, blk2, blk3, blk4, blk5, blk6, blk7, blk8, blk9], namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(corsi_mouse):
                                gotValidClick = True
                                corsi_mouse.clicked_name.append(obj.name)
                        if not gotValidClick:
                            corsi_mouse.clicked_name.append(None)
                        x, y = corsi_mouse.getPos()
                        corsi_mouse.x.append(x)
                        corsi_mouse.y.append(y)
                        buttons = corsi_mouse.getPressed()
                        corsi_mouse.leftButton.append(buttons[0])
                        corsi_mouse.midButton.append(buttons[1])
                        corsi_mouse.rightButton.append(buttons[2])
                        corsi_mouse.time.append(corsi_mouse.mouseClock.getTime())
            # Run 'Each Frame' code from check_correct
            for block in respond_blocks:
                if corsi_mouse.isPressedIn(block):
                    # change clicked block to red
                    block.fillColor = [1, 0, 0] 
                    # prevent list from being populated repeatedly with same block while mouse is being held
                    if block.name not in order_clicked: 
                        order_clicked.append(block.name)
            
            # show submit button if amount of blocks clicked is the same as sequence number
            if len(corsi_mouse.clicked_name)==nBlocks:
                show = True
            
            if corsi_mouse.isPressedIn(submit_button):
                continueRoutine = False
            
            # *submit_button* updates
            
            # if submit_button is starting this frame...
            if submit_button.status == NOT_STARTED and show:
                # keep track of start time/frame for later
                submit_button.frameNStart = frameN  # exact frame index
                submit_button.tStart = t  # local t and not account for scr refresh
                submit_button.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(submit_button, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'submit_button.started')
                # update status
                submit_button.status = STARTED
                submit_button.setAutoDraw(True)
            
            # if submit_button is active this frame...
            if submit_button.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=corsi_respond,
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                corsi_respond.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in corsi_respond.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "corsi_respond" ---
        for thisComponent in corsi_respond.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for corsi_respond
        corsi_respond.tStop = globalClock.getTime(format='float')
        corsi_respond.tStopRefresh = tThisFlipGlobal
        thisExp.addData('corsi_respond.stopped', corsi_respond.tStop)
        # store data for corsi_task (TrialHandler)
        corsi_task.addData('corsi_mouse.x', corsi_mouse.x)
        corsi_task.addData('corsi_mouse.y', corsi_mouse.y)
        corsi_task.addData('corsi_mouse.leftButton', corsi_mouse.leftButton)
        corsi_task.addData('corsi_mouse.midButton', corsi_mouse.midButton)
        corsi_task.addData('corsi_mouse.rightButton', corsi_mouse.rightButton)
        corsi_task.addData('corsi_mouse.time', corsi_mouse.time)
        corsi_task.addData('corsi_mouse.clicked_name', corsi_mouse.clicked_name)
        # Run 'End Routine' code from check_correct
        # create a variable to store accuracy
        correct = 0
        # create a list to store accuracy
        correct_list = []
        max_length = max(len(order_clicked), len(correct_order))
        for index in range(max_length):
            clicked_name = order_clicked[index] if index < len(order_clicked) else None
            expected_name = correct_order[index] if index < len(correct_order) else None
            if clicked_name is not None and expected_name is not None and clicked_name == expected_name:
                correct_list.append(1) # add value of 1 if block clicked matches the correct order
            else:
                correct_list.append(0) # add 0 if no match or response length differs
        # e.g. list - [1,1,1] for 3 sequences block
        
        # save list to csv output
        thisExp.addData('correct_list', correct_list)
        
        # if the sum of list is equals to number of sequence, the trial is correct
        if len(order_clicked) == len(correct_order) and sum(correct_list) == len(correct_order):
            correct = 1
        
        # save correct variable to csv output
        thisExp.addData('corsi_correct', correct)
        
        # increase number of blocks if they get it correct
        if correct:
            nBlocks += 1
        
        
        # cap the number of blocks at the max number
        if nBlocks > len(blocks):
            nBlocks = len(blocks)
        # the Routine "corsi_respond" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "feedback" ---
        # create an object to store info about Routine feedback
        feedback = data.Routine(
            name='feedback',
            components=[fbtxt],
        )
        feedback.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from fbcode
        # if the sequence clicked was correct
        if correct:
            thisfb = 'Correct!'
            fbcol = 'green'
        else: # if the sequence clicked was wrong
            thisfb = 'Incorrect!'
            fbcol = 'red'
        fbtxt.setColor(fbcol, colorSpace='rgb')
        fbtxt.setText(thisfb)
        # Run 'Begin Routine' code from reset_col_code
        # reset the colour of all blocks in prep for next trial
        for block in respond_blocks:
            block.fillColor = [1 ,1, 1]
        
        for block in blocks:
            block.fillColor = [1 ,1, 1]
        # store start times for feedback
        feedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        feedback.tStart = globalClock.getTime(format='float')
        feedback.status = STARTED
        thisExp.addData('feedback.started', feedback.tStart)
        feedback.maxDuration = None
        # keep track of which components have finished
        feedbackComponents = feedback.components
        for thisComponent in feedback.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "feedback" ---
        feedback.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisCorsi_task, 'status') and thisCorsi_task.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fbtxt* updates
            
            # if fbtxt is starting this frame...
            if fbtxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fbtxt.frameNStart = frameN  # exact frame index
                fbtxt.tStart = t  # local t and not account for scr refresh
                fbtxt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fbtxt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fbtxt.started')
                # update status
                fbtxt.status = STARTED
                fbtxt.setAutoDraw(True)
            
            # if fbtxt is active this frame...
            if fbtxt.status == STARTED:
                # update params
                pass
            
            # if fbtxt is stopping this frame...
            if fbtxt.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fbtxt.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    fbtxt.tStop = t  # not accounting for scr refresh
                    fbtxt.tStopRefresh = tThisFlipGlobal  # on global time
                    fbtxt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fbtxt.stopped')
                    # update status
                    fbtxt.status = FINISHED
                    fbtxt.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=feedback,
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                feedback.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in feedback.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "feedback" ---
        for thisComponent in feedback.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for feedback
        feedback.tStop = globalClock.getTime(format='float')
        feedback.tStopRefresh = tThisFlipGlobal
        thisExp.addData('feedback.stopped', feedback.tStop)
        # Run 'End Routine' code from end_task
        if not correct:
            incorrect_count += 1
        
        if incorrect_count > 3:
            corsi_task.finished = True
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if feedback.maxDurationReached:
            routineTimer.addTime(-feedback.maxDuration)
        elif feedback.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        # mark thisCorsi_task as finished
        if hasattr(thisCorsi_task, 'status'):
            thisCorsi_task.status = FINISHED
        # if awaiting a pause, pause now
        if corsi_task.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            corsi_task.status = STARTED
        thisExp.nextEntry()
        
    # completed 1000.0 repeats of 'corsi_task'
    corsi_task.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "end" ---
    # create an object to store info about Routine end
    end = data.Routine(
        name='end',
        components=[text_2],
    )
    end.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    text_2.setText('你所能记住的最高方块数量为: ' + str(nBlocks-1))
    # store start times for end
    end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    end.tStart = globalClock.getTime(format='float')
    end.status = STARTED
    thisExp.addData('end.started', end.tStart)
    end.maxDuration = None
    # keep track of which components have finished
    endComponents = end.components
    for thisComponent in end.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "end" ---
    end.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 7.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_2* updates
        
        # if text_2 is starting this frame...
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_2.started')
            # update status
            text_2.status = STARTED
            text_2.setAutoDraw(True)
        
        # if text_2 is active this frame...
        if text_2.status == STARTED:
            # update params
            pass
        
        # if text_2 is stopping this frame...
        if text_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_2.tStartRefresh + 7-frameTolerance:
                # keep track of stop time/frame for later
                text_2.tStop = t  # not accounting for scr refresh
                text_2.tStopRefresh = tThisFlipGlobal  # on global time
                text_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_2.stopped')
                # update status
                text_2.status = FINISHED
                text_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=end,
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            end.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in end.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "end" ---
    for thisComponent in end.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for end
    end.tStop = globalClock.getTime(format='float')
    end.tStopRefresh = tThisFlipGlobal
    thisExp.addData('end.stopped', end.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if end.maxDurationReached:
        routineTimer.addTime(-end.maxDuration)
    elif end.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-7.000000)
    thisExp.nextEntry()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
