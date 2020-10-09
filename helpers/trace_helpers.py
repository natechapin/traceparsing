import csv
import json
import argparse

def loadJSONfile():
  parser = argparse.ArgumentParser()
  parser.add_argument("--input_file", help="path to the datafile to process")
  args = parser.parse_args()
  trace = [];
  with open(args.input_file, "r") as file:
    trace = json.load(file);
  return trace
  
def findMainFrame(trace):
  for slice in trace:
    if 'args' not in slice.keys():
      continue
    if 'data' not in slice['args'].keys():
      continue
    if 'frames' not in slice['args']['data'].keys():
      continue
    for frame in slice['args']['data']['frames']:
      if 'parent' not in frame.keys():
        return frame['frame']
  return None

def findSlicesForMainFrame(trace):
  frame = findMainFrame(trace)
  slices_for_frame = []
  for slice in trace:
    current_frame = None
    if 'args' in slice.keys() and 'frame' in slice['args'].keys():
      current_frame = slice['args']['frame']
    elif 'args' in slice.keys() and 'data' in slice['args'].keys() and 'frame' in slice['args']['data'].keys():
      current_frame = slice['args']['data']['frame']
    elif 'args' in slice.keys() and 'beginData' in slice['args'].keys() and 'frame' in slice['args']['beginData'].keys():
      current_frame = slice['args']['beginData']['frame']
    if current_frame != frame:
      continue;
    slices_for_frame.append(slice)
  return slices_for_frame

def findCommit(trace):
  for slice in trace:
    if slice['name'] == 'CommitLoad':
      return slice['ts']
  return None

def findFCP(trace):
  for slice in trace:
    if slice['name'] == 'firstContentfulPaint':
      return slice['ts']
  return None

def findLCP(trace):
  for slice in trace:
    if slice['name'] == 'largestContentfulPaint::Candidate':
      return slice['ts']
  return None
  
def findDCL(trace):
  for slice in trace:
    if slice['name'] == 'MarkDOMContent' and slice['args']['data']['isMainFrame']:
      return slice['ts']
  return None

def findAndPrintScriptsAfterDCL(trace, dcl):
  scripts = []
  for slice in trace:
    if slice['name'] == 'EvaluateScript' and slice['ts'] > dcl:
      scripts.append(slice);
  print('Script after DCL count: ' + str(len(scripts)) + ", Duration: " + str(sumDurations(scripts)) + " microseconds")

def sumDurations(trace):
  duration = 0
  for slice in trace:
    duration += slice['tdur']
  return duration

def findAndPrintTimers(trace, fcp, lcp, dcl):
  timers = []
  for slice in trace:
    if slice['name'] == 'TimerFire':
      timers.append(slice);
  print('Total timer count: ' + str(len(timers)))

  timers_before = []
  timers_after = []
  for timer in timers:
    if timer['ts'] < fcp or timer['ts'] < lcp or timer['ts'] < dcl:
      timers_before.append(timer)
    else:
      timers_after.append(timer)
  print('Before FCP/LCP/DCL: ' + str(len(timers_before)) + ", Duration: " + str(sumDurations(timers_before)) + " microseconds")
  print('After FCP/LCP/DCL: ' + str(len(timers_after)) + ", Duration: " + str(sumDurations(timers_after)) + " microseconds")

def recordScriptsAndTimers(trace):
  fcp = findFCP(trace)
  lcp = findLCP(trace)
  dcl = findDCL(trace)
  commit = findCommit(trace)
  print('Time from Commit to DCL: ' + str(dcl - commit) + " microseconds")
  findAndPrintScriptsAfterDCL(trace, dcl)
  findAndPrintTimers(trace, fcp, lcp, dcl)  

