/********************* 
 * Corsi_Blocks *
 *********************/


// store info about the experiment session:
let expName = 'corsi_blocks';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'session': '001',
};
let PILOTING = util.getUrlParameters().has('__pilotToken');

// Start code blocks for 'Before Experiment'
// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([-1, -1, -1]),
  units: 'height',
  waitBlanking: true,
  backgroundImage: '',
  backgroundFit: 'none',
});
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); },flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(instructionsRoutineBegin());
flowScheduler.add(instructionsRoutineEachFrame());
flowScheduler.add(instructionsRoutineEnd());
const corsi_taskLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(corsi_taskLoopBegin(corsi_taskLoopScheduler));
flowScheduler.add(corsi_taskLoopScheduler);
flowScheduler.add(corsi_taskLoopEnd);







flowScheduler.add(endRoutineBegin());
flowScheduler.add(endRoutineEachFrame());
flowScheduler.add(endRoutineEnd());
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.EXP);


var currentLoop;
var frameDur;
async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2025.1.1';
  expInfo['OS'] = window.navigator.platform;


  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0 / Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0 / 60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  

  
  psychoJS.experiment.dataFileName = (("." + "/") + `data/${expInfo["participant"]}_${expName}_${expInfo["date"]}`);
  psychoJS.experiment.field_separator = '\t';


  return Scheduler.Event.NEXT;
}


var instructionsClock;
var text;
var key_resp;
var mouse;
var ISIClock;
var blank;
var nBlocks;
var corsi_presentClock;
var blk1_3;
var blk2_3;
var blk3_3;
var blk4_3;
var blk5_3;
var blk6_3;
var blk7_3;
var blk8_3;
var blk9_3;
var corsi_respondClock;
var blk1;
var blk2;
var blk3;
var blk4;
var blk5;
var blk6;
var blk7;
var blk8;
var blk9;
var corsi_mouse;
var submit_button;
var feedbackClock;
var fbtxt;
var incorrect_count;
var endClock;
var text_2;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  text = new visual.TextStim({
    win: psychoJS.window,
    name: 'text',
    text: '在这个游戏里，你需要仔细观察并记住屏幕上方块亮起的顺序。\n\n游戏怎么玩？一开始会很简单，只有3个方块会按顺序亮起。\n你的任务就是仔细观察，然后按照同样的顺序点击这些方块。\n只要你答对了，下一次挑战的方块数量就会增加一个，难度会慢慢上升。\n\n每个难度下你有 4 次尝试机会。\n\n准备好了吗？请按任意键或点击屏幕任意位置开始。',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Initialize components for Routine "ISI"
  ISIClock = new util.Clock();
  blank = new visual.TextStim({
    win: psychoJS.window,
    name: 'blank',
    text: '+',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.2,  wrapWidth: undefined, ori: 0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  // Run 'Begin Experiment' code from setLocations
  nBlocks = 3;
  
  // Initialize components for Routine "corsi_present"
  corsi_presentClock = new util.Clock();
  blk1_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk1_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -1, 
    interpolate: true, 
  });
  
  blk2_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk2_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -2, 
    interpolate: true, 
  });
  
  blk3_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk3_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -3, 
    interpolate: true, 
  });
  
  blk4_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk4_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -4, 
    interpolate: true, 
  });
  
  blk5_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk5_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -5, 
    interpolate: true, 
  });
  
  blk6_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk6_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -6, 
    interpolate: true, 
  });
  
  blk7_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk7_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -7, 
    interpolate: true, 
  });
  
  blk8_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk8_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -8, 
    interpolate: true, 
  });
  
  blk9_3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk9_3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -9, 
    interpolate: true, 
  });
  
  // Initialize components for Routine "corsi_respond"
  corsi_respondClock = new util.Clock();
  blk1 = new visual.Rect ({
    win: psychoJS.window, name: 'blk1', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: 0, 
    interpolate: true, 
  });
  
  blk2 = new visual.Rect ({
    win: psychoJS.window, name: 'blk2', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -1, 
    interpolate: true, 
  });
  
  blk3 = new visual.Rect ({
    win: psychoJS.window, name: 'blk3', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -2, 
    interpolate: true, 
  });
  
  blk4 = new visual.Rect ({
    win: psychoJS.window, name: 'blk4', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -3, 
    interpolate: true, 
  });
  
  blk5 = new visual.Rect ({
    win: psychoJS.window, name: 'blk5', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -4, 
    interpolate: true, 
  });
  
  blk6 = new visual.Rect ({
    win: psychoJS.window, name: 'blk6', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -5, 
    interpolate: true, 
  });
  
  blk7 = new visual.Rect ({
    win: psychoJS.window, name: 'blk7', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -6, 
    interpolate: true, 
  });
  
  blk8 = new visual.Rect ({
    win: psychoJS.window, name: 'blk8', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -7, 
    interpolate: true, 
  });
  
  blk9 = new visual.Rect ({
    win: psychoJS.window, name: 'blk9', units : 'height', 
    width: [0.1, 0.1][0], height: [0.1, 0.1][1],
    ori: 0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1, 
    lineColor: new util.Color([1, 1, 1]), 
    fillColor: new util.Color([1, 1, 1]), 
    colorSpace: 'rgb', 
    opacity: 1, 
    depth: -8, 
    interpolate: true, 
  });
  
  corsi_mouse = new core.Mouse({
    win: psychoJS.window,
  });
  corsi_mouse.mouseClock = new util.Clock();
  submit_button = new visual.TextBox({
    win: psychoJS.window,
    name: 'submit_button',
    text: 'Submit',
    placeholder: 'Type here...',
    font: 'Arial',
    pos: [0.5, (- 0.4)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.2, 0.1],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: 'darkgrey', borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: false,
    multiline: true,
    anchor: 'center',
    depth: -11.0 
  });
  
  // Initialize components for Routine "feedback"
  feedbackClock = new util.Clock();
  fbtxt = new visual.TextStim({
    win: psychoJS.window,
    name: 'fbtxt',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: -1.0 
  });
  
  // Run 'Begin Experiment' code from end_task
  incorrect_count = 0;
  
  // Initialize components for Routine "end"
  endClock = new util.Clock();
  text_2 = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_2',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var routineForceEnded;
var instructionsMaxDurationReached;
var _key_resp_allKeys;
var gotValidClick;
var instructionsMaxDuration;
var instructionsComponents;
function instructionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'instructions' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    instructionsClock.reset();
    routineTimer.reset();
    instructionsMaxDurationReached = false;
    // update component parameters for each repeat
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    // setup some python lists for storing info about the mouse
    // current position of the mouse:
    mouse.x = [];
    mouse.y = [];
    mouse.leftButton = [];
    mouse.midButton = [];
    mouse.rightButton = [];
    mouse.time = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('instructions.started', globalClock.getTime());
    instructionsMaxDuration = null
    // keep track of which components have finished
    instructionsComponents = [];
    instructionsComponents.push(text);
    instructionsComponents.push(key_resp);
    instructionsComponents.push(mouse);
    
    instructionsComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
       });
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
var _mouseXYs;
function instructionsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'instructions' ---
    // get current time
    t = instructionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *text* updates
    if (t >= 0.0 && text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      text.tStart = t;  // (not accounting for frame time here)
      text.frameNStart = frameN;  // exact frame index
      
      text.setAutoDraw(true);
    }
    
    
    // if text is active this frame...
    if (text.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *key_resp* updates
    if (t >= 0.0 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp.tStart = t;  // (not accounting for frame time here)
      key_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp.clearEvents(); });
    }
    
    // if key_resp is active this frame...
    if (key_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp.getKeys({keyList: [], waitRelease: false});
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
        key_resp.duration = _key_resp_allKeys[_key_resp_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    // *mouse* updates
    if (t >= 0.0 && mouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse.tStart = t;  // (not accounting for frame time here)
      mouse.frameNStart = frameN;  // exact frame index
      
      mouse.status = PsychoJS.Status.STARTED;
      mouse.mouseClock.reset();
      prevButtonState = mouse.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse is active this frame...
    if (mouse.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          _mouseXYs = mouse.getPos();
          mouse.x.push(_mouseXYs[0]);
          mouse.y.push(_mouseXYs[1]);
          mouse.leftButton.push(_mouseButtons[0]);
          mouse.midButton.push(_mouseButtons[1]);
          mouse.rightButton.push(_mouseButtons[2]);
          mouse.time.push(mouse.mouseClock.getTime());
          // end routine on response
          continueRoutine = false;
        }
      }
    }
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    instructionsComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
      }
    });
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function instructionsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'instructions' ---
    instructionsComponents.forEach( function(thisComponent) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    });
    psychoJS.experiment.addData('instructions.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp.corr, level);
    }
    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    if (typeof key_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
        psychoJS.experiment.addData('key_resp.duration', key_resp.duration);
        routineTimer.reset();
        }
    
    key_resp.stop();
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse.x', mouse.x);
    psychoJS.experiment.addData('mouse.y', mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', mouse.time);
    
    // the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var corsi_task;
function corsi_taskLoopBegin(corsi_taskLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    corsi_task = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1000, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'corsi_task'
    });
    psychoJS.experiment.addLoop(corsi_task); // add the loop to the experiment
    currentLoop = corsi_task;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    corsi_task.forEach(function() {
      snapshot = corsi_task.getSnapshot();
    
      corsi_taskLoopScheduler.add(importConditions(snapshot));
      corsi_taskLoopScheduler.add(ISIRoutineBegin(snapshot));
      corsi_taskLoopScheduler.add(ISIRoutineEachFrame());
      corsi_taskLoopScheduler.add(ISIRoutineEnd(snapshot));
      const block_sequenceLoopScheduler = new Scheduler(psychoJS);
      corsi_taskLoopScheduler.add(block_sequenceLoopBegin(block_sequenceLoopScheduler, snapshot));
      corsi_taskLoopScheduler.add(block_sequenceLoopScheduler);
      corsi_taskLoopScheduler.add(block_sequenceLoopEnd);
      corsi_taskLoopScheduler.add(corsi_respondRoutineBegin(snapshot));
      corsi_taskLoopScheduler.add(corsi_respondRoutineEachFrame());
      corsi_taskLoopScheduler.add(corsi_respondRoutineEnd(snapshot));
      corsi_taskLoopScheduler.add(feedbackRoutineBegin(snapshot));
      corsi_taskLoopScheduler.add(feedbackRoutineEachFrame());
      corsi_taskLoopScheduler.add(feedbackRoutineEnd(snapshot));
      corsi_taskLoopScheduler.add(corsi_taskLoopEndIteration(corsi_taskLoopScheduler, snapshot));
    });
    
    return Scheduler.Event.NEXT;
  }
}


var block_sequence;
function block_sequenceLoopBegin(block_sequenceLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    block_sequence = new TrialHandler({
      psychoJS: psychoJS,
      nReps: nBlocks, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'block_sequence'
    });
    psychoJS.experiment.addLoop(block_sequence); // add the loop to the experiment
    currentLoop = block_sequence;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    block_sequence.forEach(function() {
      snapshot = block_sequence.getSnapshot();
    
      block_sequenceLoopScheduler.add(importConditions(snapshot));
      block_sequenceLoopScheduler.add(corsi_presentRoutineBegin(snapshot));
      block_sequenceLoopScheduler.add(corsi_presentRoutineEachFrame());
      block_sequenceLoopScheduler.add(corsi_presentRoutineEnd(snapshot));
      block_sequenceLoopScheduler.add(block_sequenceLoopEndIteration(block_sequenceLoopScheduler, snapshot));
    });
    
    return Scheduler.Event.NEXT;
  }
}


async function block_sequenceLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(block_sequence);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function block_sequenceLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}


async function corsi_taskLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(corsi_task);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function corsi_taskLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}


var ISIMaxDurationReached;
var blocks;
var respond_blocks;
var block_order;
var correct_order;
var respond_block_order;
var xys;
var count;
var positions;
var ISIMaxDuration;
var ISIComponents;
function ISIRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'ISI' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    ISIClock.reset(routineTimer.getTime());
    routineTimer.add(0.500000);
    ISIMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from setLocations
    blocks = [blk1_3, blk2_3, blk3_3, blk4_3, blk5_3, blk6_3, blk7_3, blk8_3, blk9_3];
    respond_blocks = [blk1, blk2, blk3, blk4, blk5, blk6, blk7, blk8, blk9];
    block_order = [];
    correct_order = [];
    respond_block_order = [];
    for (var block, _pj_c = 0, _pj_a = util.range(nBlocks), _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
        block = _pj_a[_pj_c];
        blocks[block].setColor("white");
        respond_blocks[block].setColor("white");
        correct_order.push(respond_blocks[block].name);
        block_order.push(blocks[block]);
        respond_block_order.push(respond_blocks[block]);
    }
    console.log("block_order", block_order);
    console.log("correct_order", correct_order);
    console.log("respond_block_order", respond_block_order);
    xys = [[0.25625, 0.0975], [0.0675, 0.07375], [(- 0.09875), 0.065], [(- 0.26625), 0.235], [0.22, 0.2425], [0.16625, 0.3825], [(- 0.18625), 0.41125], [(- 0.01875), 0.235], [(- 0.3575), (- 0.05625)], [(- 0.12125), (- 0.12625)], [0.05875, (- 0.0575)], [0.19375, (- 0.17125)], [0.30125, (- 0.0175)], [0.4125, (- 0.1325)], [0.365, (- 0.27625)], [(- 0.01125), (- 0.295)], [(- 0.285), (- 0.27125)], [(- 0.4075), 0.11875], [(- 0.485), 0.34625], [0.4625, 0.35875], [0.45375, 0.175], [0.54, 0.03625], [0.62875, (- 0.1825)], [0.57875, (- 0.31375)], [(- 0.45875), (- 0.3)], [(- 0.55125), (- 0.13375)], [(- 0.6025), 0.0725], [(- 0.675), 0.29875], [(- 0.68625), (- 0.225)], [0.03125, (- 0.41)], [0.1925, (- 0.295)], [(- 0.16125), (- 0.28)], [(- 0.24625), 0.04375], [(- 0.0225), 0.395], [0.28875, 0.39875], [0.6375, 0.27375], [(- 0.35125), 0.36625]];
    util.shuffle(xys);
    count = 0;
    positions = [];
    for (var block, _pj_c = 0, _pj_a = blocks, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
        block = _pj_a[_pj_c];
        block.setPos([xys[count][0], xys[count][1]]);
        respond_blocks[count].setPos([xys[count][0], xys[count][1]]);
        positions.push(xys[count]);
        count += 1;
    }
    psychoJS.experiment.addData("positions", positions);
    
    psychoJS.experiment.addData('ISI.started', globalClock.getTime());
    ISIMaxDuration = null
    // keep track of which components have finished
    ISIComponents = [];
    ISIComponents.push(blank);
    
    ISIComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
       });
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function ISIRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'ISI' ---
    // get current time
    t = ISIClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *blank* updates
    if (t >= 0.0 && blank.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blank.tStart = t;  // (not accounting for frame time here)
      blank.frameNStart = frameN;  // exact frame index
      
      blank.setAutoDraw(true);
    }
    
    
    // if blank is active this frame...
    if (blank.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blank.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blank.tStop = t;  // not accounting for scr refresh
      blank.frameNStop = frameN;  // exact frame index
      // update status
      blank.status = PsychoJS.Status.FINISHED;
      blank.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    ISIComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
      }
    });
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function ISIRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'ISI' ---
    ISIComponents.forEach( function(thisComponent) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    });
    psychoJS.experiment.addData('ISI.stopped', globalClock.getTime());
    if (routineForceEnded) {
        routineTimer.reset();} else if (ISIMaxDurationReached) {
        ISIClock.add(ISIMaxDuration);
    } else {
        ISIClock.add(0.500000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var corsi_presentMaxDurationReached;
var corsi_presentMaxDuration;
var corsi_presentComponents;
function corsi_presentRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'corsi_present' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    corsi_presentClock.reset(routineTimer.getTime());
    routineTimer.add(0.500000);
    corsi_presentMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from setColor
    block_order[block_sequence.thisN].fillColor = new util.Color([1, 0, 0])
    console.log(block_order[block_sequence.thisN].pos);
    console.log(block_order[block_sequence.thisN].opacity);
    
    psychoJS.experiment.addData('corsi_present.started', globalClock.getTime());
    corsi_presentMaxDuration = null
    // keep track of which components have finished
    corsi_presentComponents = [];
    corsi_presentComponents.push(blk1_3);
    corsi_presentComponents.push(blk2_3);
    corsi_presentComponents.push(blk3_3);
    corsi_presentComponents.push(blk4_3);
    corsi_presentComponents.push(blk5_3);
    corsi_presentComponents.push(blk6_3);
    corsi_presentComponents.push(blk7_3);
    corsi_presentComponents.push(blk8_3);
    corsi_presentComponents.push(blk9_3);
    
    corsi_presentComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
       });
    return Scheduler.Event.NEXT;
  }
}


function corsi_presentRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'corsi_present' ---
    // get current time
    t = corsi_presentClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *blk1_3* updates
    if (t >= 0.0 && blk1_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk1_3.tStart = t;  // (not accounting for frame time here)
      blk1_3.frameNStart = frameN;  // exact frame index
      
      blk1_3.setAutoDraw(true);
    }
    
    
    // if blk1_3 is active this frame...
    if (blk1_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk1_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk1_3.tStop = t;  // not accounting for scr refresh
      blk1_3.frameNStop = frameN;  // exact frame index
      // update status
      blk1_3.status = PsychoJS.Status.FINISHED;
      blk1_3.setAutoDraw(false);
    }
    
    
    // *blk2_3* updates
    if (t >= 0.0 && blk2_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk2_3.tStart = t;  // (not accounting for frame time here)
      blk2_3.frameNStart = frameN;  // exact frame index
      
      blk2_3.setAutoDraw(true);
    }
    
    
    // if blk2_3 is active this frame...
    if (blk2_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk2_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk2_3.tStop = t;  // not accounting for scr refresh
      blk2_3.frameNStop = frameN;  // exact frame index
      // update status
      blk2_3.status = PsychoJS.Status.FINISHED;
      blk2_3.setAutoDraw(false);
    }
    
    
    // *blk3_3* updates
    if (t >= 0.0 && blk3_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk3_3.tStart = t;  // (not accounting for frame time here)
      blk3_3.frameNStart = frameN;  // exact frame index
      
      blk3_3.setAutoDraw(true);
    }
    
    
    // if blk3_3 is active this frame...
    if (blk3_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk3_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk3_3.tStop = t;  // not accounting for scr refresh
      blk3_3.frameNStop = frameN;  // exact frame index
      // update status
      blk3_3.status = PsychoJS.Status.FINISHED;
      blk3_3.setAutoDraw(false);
    }
    
    
    // *blk4_3* updates
    if (t >= 0.0 && blk4_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk4_3.tStart = t;  // (not accounting for frame time here)
      blk4_3.frameNStart = frameN;  // exact frame index
      
      blk4_3.setAutoDraw(true);
    }
    
    
    // if blk4_3 is active this frame...
    if (blk4_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk4_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk4_3.tStop = t;  // not accounting for scr refresh
      blk4_3.frameNStop = frameN;  // exact frame index
      // update status
      blk4_3.status = PsychoJS.Status.FINISHED;
      blk4_3.setAutoDraw(false);
    }
    
    
    // *blk5_3* updates
    if (t >= 0.0 && blk5_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk5_3.tStart = t;  // (not accounting for frame time here)
      blk5_3.frameNStart = frameN;  // exact frame index
      
      blk5_3.setAutoDraw(true);
    }
    
    
    // if blk5_3 is active this frame...
    if (blk5_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk5_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk5_3.tStop = t;  // not accounting for scr refresh
      blk5_3.frameNStop = frameN;  // exact frame index
      // update status
      blk5_3.status = PsychoJS.Status.FINISHED;
      blk5_3.setAutoDraw(false);
    }
    
    
    // *blk6_3* updates
    if (t >= 0.0 && blk6_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk6_3.tStart = t;  // (not accounting for frame time here)
      blk6_3.frameNStart = frameN;  // exact frame index
      
      blk6_3.setAutoDraw(true);
    }
    
    
    // if blk6_3 is active this frame...
    if (blk6_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk6_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk6_3.tStop = t;  // not accounting for scr refresh
      blk6_3.frameNStop = frameN;  // exact frame index
      // update status
      blk6_3.status = PsychoJS.Status.FINISHED;
      blk6_3.setAutoDraw(false);
    }
    
    
    // *blk7_3* updates
    if (t >= 0.0 && blk7_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk7_3.tStart = t;  // (not accounting for frame time here)
      blk7_3.frameNStart = frameN;  // exact frame index
      
      blk7_3.setAutoDraw(true);
    }
    
    
    // if blk7_3 is active this frame...
    if (blk7_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk7_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk7_3.tStop = t;  // not accounting for scr refresh
      blk7_3.frameNStop = frameN;  // exact frame index
      // update status
      blk7_3.status = PsychoJS.Status.FINISHED;
      blk7_3.setAutoDraw(false);
    }
    
    
    // *blk8_3* updates
    if (t >= 0.0 && blk8_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk8_3.tStart = t;  // (not accounting for frame time here)
      blk8_3.frameNStart = frameN;  // exact frame index
      
      blk8_3.setAutoDraw(true);
    }
    
    
    // if blk8_3 is active this frame...
    if (blk8_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk8_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk8_3.tStop = t;  // not accounting for scr refresh
      blk8_3.frameNStop = frameN;  // exact frame index
      // update status
      blk8_3.status = PsychoJS.Status.FINISHED;
      blk8_3.setAutoDraw(false);
    }
    
    
    // *blk9_3* updates
    if (t >= 0.0 && blk9_3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk9_3.tStart = t;  // (not accounting for frame time here)
      blk9_3.frameNStart = frameN;  // exact frame index
      
      blk9_3.setAutoDraw(true);
    }
    
    
    // if blk9_3 is active this frame...
    if (blk9_3.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (blk9_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      blk9_3.tStop = t;  // not accounting for scr refresh
      blk9_3.frameNStop = frameN;  // exact frame index
      // update status
      blk9_3.status = PsychoJS.Status.FINISHED;
      blk9_3.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    corsi_presentComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
      }
    });
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function corsi_presentRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'corsi_present' ---
    corsi_presentComponents.forEach( function(thisComponent) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    });
    psychoJS.experiment.addData('corsi_present.stopped', globalClock.getTime());
    // Run 'End Routine' code from setColor
    block_order[block_sequence.thisN].fillColor = new util.Color([1, 1, 1])
    
    if (routineForceEnded) {
        routineTimer.reset();} else if (corsi_presentMaxDurationReached) {
        corsi_presentClock.add(corsi_presentMaxDuration);
    } else {
        corsi_presentClock.add(0.500000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var corsi_respondMaxDurationReached;
var order_clicked;
var show;
var corsi_respondMaxDuration;
var corsi_respondComponents;
function corsi_respondRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'corsi_respond' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    corsi_respondClock.reset();
    routineTimer.reset();
    corsi_respondMaxDurationReached = false;
    // update component parameters for each repeat
    // setup some python lists for storing info about the corsi_mouse
    // current position of the mouse:
    corsi_mouse.x = [];
    corsi_mouse.y = [];
    corsi_mouse.leftButton = [];
    corsi_mouse.midButton = [];
    corsi_mouse.rightButton = [];
    corsi_mouse.time = [];
    corsi_mouse.clicked_name = [];
    gotValidClick = false; // until a click is received
    // Run 'Begin Routine' code from check_correct
    order_clicked = [];
    show = false;
    
    psychoJS.experiment.addData('corsi_respond.started', globalClock.getTime());
    corsi_respondMaxDuration = null
    // keep track of which components have finished
    corsi_respondComponents = [];
    corsi_respondComponents.push(blk1);
    corsi_respondComponents.push(blk2);
    corsi_respondComponents.push(blk3);
    corsi_respondComponents.push(blk4);
    corsi_respondComponents.push(blk5);
    corsi_respondComponents.push(blk6);
    corsi_respondComponents.push(blk7);
    corsi_respondComponents.push(blk8);
    corsi_respondComponents.push(blk9);
    corsi_respondComponents.push(corsi_mouse);
    corsi_respondComponents.push(submit_button);
    
    corsi_respondComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
       });
    return Scheduler.Event.NEXT;
  }
}


var _pj;
function corsi_respondRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'corsi_respond' ---
    // get current time
    t = corsi_respondClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *blk1* updates
    if (t >= 0.0 && blk1.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk1.tStart = t;  // (not accounting for frame time here)
      blk1.frameNStart = frameN;  // exact frame index
      
      blk1.setAutoDraw(true);
    }
    
    
    // if blk1 is active this frame...
    if (blk1.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk2* updates
    if (t >= 0.0 && blk2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk2.tStart = t;  // (not accounting for frame time here)
      blk2.frameNStart = frameN;  // exact frame index
      
      blk2.setAutoDraw(true);
    }
    
    
    // if blk2 is active this frame...
    if (blk2.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk3* updates
    if (t >= 0.0 && blk3.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk3.tStart = t;  // (not accounting for frame time here)
      blk3.frameNStart = frameN;  // exact frame index
      
      blk3.setAutoDraw(true);
    }
    
    
    // if blk3 is active this frame...
    if (blk3.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk4* updates
    if (t >= 0.0 && blk4.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk4.tStart = t;  // (not accounting for frame time here)
      blk4.frameNStart = frameN;  // exact frame index
      
      blk4.setAutoDraw(true);
    }
    
    
    // if blk4 is active this frame...
    if (blk4.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk5* updates
    if (t >= 0.0 && blk5.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk5.tStart = t;  // (not accounting for frame time here)
      blk5.frameNStart = frameN;  // exact frame index
      
      blk5.setAutoDraw(true);
    }
    
    
    // if blk5 is active this frame...
    if (blk5.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk6* updates
    if (t >= 0.0 && blk6.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk6.tStart = t;  // (not accounting for frame time here)
      blk6.frameNStart = frameN;  // exact frame index
      
      blk6.setAutoDraw(true);
    }
    
    
    // if blk6 is active this frame...
    if (blk6.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk7* updates
    if (t >= 0.0 && blk7.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk7.tStart = t;  // (not accounting for frame time here)
      blk7.frameNStart = frameN;  // exact frame index
      
      blk7.setAutoDraw(true);
    }
    
    
    // if blk7 is active this frame...
    if (blk7.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk8* updates
    if (t >= 0.0 && blk8.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk8.tStart = t;  // (not accounting for frame time here)
      blk8.frameNStart = frameN;  // exact frame index
      
      blk8.setAutoDraw(true);
    }
    
    
    // if blk8 is active this frame...
    if (blk8.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *blk9* updates
    if (t >= 0.0 && blk9.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      blk9.tStart = t;  // (not accounting for frame time here)
      blk9.frameNStart = frameN;  // exact frame index
      
      blk9.setAutoDraw(true);
    }
    
    
    // if blk9 is active this frame...
    if (blk9.status === PsychoJS.Status.STARTED) {
    }
    
    // *corsi_mouse* updates
    if (t >= 0.0 && corsi_mouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      corsi_mouse.tStart = t;  // (not accounting for frame time here)
      corsi_mouse.frameNStart = frameN;  // exact frame index
      
      corsi_mouse.status = PsychoJS.Status.STARTED;
      corsi_mouse.mouseClock.reset();
      prevButtonState = corsi_mouse.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if corsi_mouse is active this frame...
    if (corsi_mouse.status === PsychoJS.Status.STARTED) {
      _mouseButtons = corsi_mouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          // check if the mouse was inside our 'clickable' objects
          gotValidClick = false;
          corsi_mouse.clickableObjects = eval([blk1, blk2, blk3, blk4, blk5, blk6, blk7, blk8, blk9])
          ;// make sure the mouse's clickable objects are an array
          if (!Array.isArray(corsi_mouse.clickableObjects)) {
              corsi_mouse.clickableObjects = [corsi_mouse.clickableObjects];
          }
          // iterate through clickable objects and check each
          for (const obj of corsi_mouse.clickableObjects) {
              if (obj.contains(corsi_mouse)) {
                  gotValidClick = true;
                  corsi_mouse.clicked_name.push(obj.name);
              }
          }
          if (!gotValidClick) {
              corsi_mouse.clicked_name.push(null);
          }
          _mouseXYs = corsi_mouse.getPos();
          corsi_mouse.x.push(_mouseXYs[0]);
          corsi_mouse.y.push(_mouseXYs[1]);
          corsi_mouse.leftButton.push(_mouseButtons[0]);
          corsi_mouse.midButton.push(_mouseButtons[1]);
          corsi_mouse.rightButton.push(_mouseButtons[2]);
          corsi_mouse.time.push(corsi_mouse.mouseClock.getTime());
        }
      }
    }
    // Run 'Each Frame' code from check_correct
    var _pj;
    function _pj_snippets(container) {
        function in_es6(left, right) {
            if (((right instanceof Array) || ((typeof right) === "string"))) {
                return (right.indexOf(left) > (- 1));
            } else {
                if (((right instanceof Map) || (right instanceof Set) || (right instanceof WeakMap) || (right instanceof WeakSet))) {
                    return right.has(left);
                } else {
                    return (left in right);
                }
            }
        }
        container["in_es6"] = in_es6;
        return container;
    }
    _pj = {};
    _pj_snippets(_pj);
    for (var block, _pj_c = 0, _pj_a = respond_blocks, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
        block = _pj_a[_pj_c];
        if (corsi_mouse.isPressedIn(block)) {
            block.fillColor = [1, 0, 0];
            if ((! _pj.in_es6(block.name, order_clicked))) {
                order_clicked.push(block.name);
            }
        }
    }
    if ((corsi_mouse.clicked_name.length === nBlocks)) {
        show = true;
    }
    if (corsi_mouse.isPressedIn(submit_button)) {
        continueRoutine = false;
    }
    
    
    // *submit_button* updates
    if ((show) && submit_button.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      submit_button.tStart = t;  // (not accounting for frame time here)
      submit_button.frameNStart = frameN;  // exact frame index
      
      submit_button.setAutoDraw(true);
    }
    
    
    // if submit_button is active this frame...
    if (submit_button.status === PsychoJS.Status.STARTED) {
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    corsi_respondComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
      }
    });
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


var correct;
var correct_list;
function corsi_respondRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'corsi_respond' ---
    corsi_respondComponents.forEach( function(thisComponent) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    });
    psychoJS.experiment.addData('corsi_respond.stopped', globalClock.getTime());
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('corsi_mouse.x', corsi_mouse.x);
    psychoJS.experiment.addData('corsi_mouse.y', corsi_mouse.y);
    psychoJS.experiment.addData('corsi_mouse.leftButton', corsi_mouse.leftButton);
    psychoJS.experiment.addData('corsi_mouse.midButton', corsi_mouse.midButton);
    psychoJS.experiment.addData('corsi_mouse.rightButton', corsi_mouse.rightButton);
    psychoJS.experiment.addData('corsi_mouse.time', corsi_mouse.time);
    psychoJS.experiment.addData('corsi_mouse.clicked_name', corsi_mouse.clicked_name);
    
    // Run 'End Routine' code from check_correct
    correct = 0;
    console.log("order_clicked", order_clicked);
    console.log("correct_order", correct_order);
    correct_list = [];
    count = 0;
    for (var name, _pj_c = 0, _pj_a = order_clicked, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
        name = _pj_a[_pj_c];
        if ((name === correct_order[count])) {
            correct_list.push(1);
        } else {
            correct_list.push(0);
        }
        count += 1;
    }
    console.log(correct_list);
    psychoJS.experiment.addData("correct_list", correct_list);
    if ((util.sum(correct_list) === correct_list.length)) {
        correct = 1;
    }
    psychoJS.experiment.addData("corsi_correct", correct);
    if (correct) {
        nBlocks += 1;
    }
    if ((nBlocks > blocks.length)) {
        nBlocks = blocks.length;
    }
    
    // the Routine "corsi_respond" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var feedbackMaxDurationReached;
var thisfb;
var fbcol;
var feedbackMaxDuration;
var feedbackComponents;
function feedbackRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'feedback' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    feedbackClock.reset(routineTimer.getTime());
    routineTimer.add(1.000000);
    feedbackMaxDurationReached = false;
    // update component parameters for each repeat
    // Run 'Begin Routine' code from fbcode
    if (correct) {
        thisfb = "Correct!";
        fbcol = "green";
    } else {
        thisfb = "Incorrect!";
        fbcol = "red";
    }
    
    fbtxt.setColor(new util.Color(fbcol));
    fbtxt.setText(thisfb);
    // Run 'Begin Routine' code from reset_col_code
    for (var block, _pj_c = 0, _pj_a = respond_blocks, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
        block = _pj_a[_pj_c];
        block.fillColor = new util.Color([1 ,1, 1])
    }
    
    for (var block, _pj_c = 0, _pj_a = blocks, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
        block = _pj_a[_pj_c];
        block.fillColor = new util.Color([1 ,1, 1])
    }
    
    psychoJS.experiment.addData('feedback.started', globalClock.getTime());
    feedbackMaxDuration = null
    // keep track of which components have finished
    feedbackComponents = [];
    feedbackComponents.push(fbtxt);
    
    feedbackComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
       });
    return Scheduler.Event.NEXT;
  }
}


function feedbackRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'feedback' ---
    // get current time
    t = feedbackClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *fbtxt* updates
    if (t >= 0.0 && fbtxt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fbtxt.tStart = t;  // (not accounting for frame time here)
      fbtxt.frameNStart = frameN;  // exact frame index
      
      fbtxt.setAutoDraw(true);
    }
    
    
    // if fbtxt is active this frame...
    if (fbtxt.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (fbtxt.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      fbtxt.tStop = t;  // not accounting for scr refresh
      fbtxt.frameNStop = frameN;  // exact frame index
      // update status
      fbtxt.status = PsychoJS.Status.FINISHED;
      fbtxt.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    feedbackComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
      }
    });
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function feedbackRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'feedback' ---
    feedbackComponents.forEach( function(thisComponent) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    });
    psychoJS.experiment.addData('feedback.stopped', globalClock.getTime());
    // Run 'End Routine' code from end_task
    if ((! correct)) {
        incorrect_count += 1;
    }
    if ((incorrect_count > 3)) {
        corsi_task.finished = true;
    }
    
    if (routineForceEnded) {
        routineTimer.reset();} else if (feedbackMaxDurationReached) {
        feedbackClock.add(feedbackMaxDuration);
    } else {
        feedbackClock.add(1.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var endMaxDurationReached;
var endMaxDuration;
var endComponents;
function endRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'end' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    endClock.reset(routineTimer.getTime());
    routineTimer.add(7.000000);
    endMaxDurationReached = false;
    // update component parameters for each repeat
    text_2.setText(("\u4f60\u6240\u80fd\u8bb0\u4f4f\u7684\u6700\u9ad8\u65b9\u5757\u6570\u91cf\u4e3a: " + (nBlocks - 1).toString()));
    psychoJS.experiment.addData('end.started', globalClock.getTime());
    endMaxDuration = null
    // keep track of which components have finished
    endComponents = [];
    endComponents.push(text_2);
    
    endComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
       });
    return Scheduler.Event.NEXT;
  }
}


function endRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'end' ---
    // get current time
    t = endClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *text_2* updates
    if (t >= 0.0 && text_2.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      text_2.tStart = t;  // (not accounting for frame time here)
      text_2.frameNStart = frameN;  // exact frame index
      
      text_2.setAutoDraw(true);
    }
    
    
    // if text_2 is active this frame...
    if (text_2.status === PsychoJS.Status.STARTED) {
    }
    
    frameRemains = 0.0 + 7 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (text_2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      text_2.tStop = t;  // not accounting for scr refresh
      text_2.frameNStop = frameN;  // exact frame index
      // update status
      text_2.status = PsychoJS.Status.FINISHED;
      text_2.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    endComponents.forEach( function(thisComponent) {
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
      }
    });
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function endRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'end' ---
    endComponents.forEach( function(thisComponent) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    });
    psychoJS.experiment.addData('end.stopped', globalClock.getTime());
    if (routineForceEnded) {
        routineTimer.reset();} else if (endMaxDurationReached) {
        endClock.add(endMaxDuration);
    } else {
        endClock.add(7.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


function importConditions(currentLoop) {
  return async function () {
    psychoJS.importAttributes(currentLoop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}


async function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});
  
  return Scheduler.Event.QUIT;
}
