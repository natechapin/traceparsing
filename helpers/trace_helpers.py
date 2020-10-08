import csv
import json
import argparse

def loadJSONfile():
  parser = argparse.ArgumentParser()
  parser.add_argument("--input_file", help="path to the datafile to process")
  args = parser.parse_args()
  traces = [];
  with open(args.input_file, "r") as file:
    traces = json.load(file);
  return traces
  
def findMainFrame(traces):
  for trace in traces:
    if 'args' not in trace.keys():
      continue
    if 'data' not in trace['args'].keys():
      continue
    if 'frames' not in trace['args']['data'].keys():
      continue
    frames = trace['args']['data']['frames'];
    for frame in trace['args']['data']['frames']:
      if 'parent' not in frame.keys():
        return frame['frame']
  return None

def findTracesForMainFrame(traces):
  frame = findMainFrame(traces)
  traces_for_frame = []
  for trace in traces:
    current_frame = None
    if 'args' in trace.keys() and 'frame' in trace['args'].keys():
      current_frame = trace['args']['frame']
    elif 'args' in trace.keys() and 'data' in trace['args'].keys() and 'frame' in trace['args']['data'].keys():
      current_frame = trace['args']['data']['frame']
    elif 'args' in trace.keys() and 'beginData' in trace['args'].keys() and 'frame' in trace['args']['beginData'].keys():
      current_frame = trace['args']['beginData']['frame']
    if current_frame != frame:
      continue;
    traces_for_frame.append(trace)
  return traces_for_frame

def findCommit(traces):
  for trace in traces:
    if trace['name'] == 'CommitLoad':
      return trace['ts']
  return None

def findFCP(traces):
  for trace in traces:
    if trace['name'] == 'firstContentfulPaint':
      return trace['ts']
  return None

def findLCP(traces):
  for trace in traces:
    if trace['name'] == 'largestContentfulPaint::Candidate':
      return trace['ts']
  return None
  
def findDCL(traces):
  for trace in traces:
    if trace['name'] == 'MarkDOMContent' and trace['args']['data']['isMainFrame']:
      return trace['ts']
  return None

def findAndPrintScriptsAfterDCL(traces, dcl):
  scripts = []
  for trace in traces:
    if trace['name'] == 'EvaluateScript' and trace['ts'] > dcl:
      scripts.append(trace);
  print('Script after DCL count: ' + str(len(scripts)) + ", Duration: " + str(sumDurations(scripts)) + " microseconds")

def sumDurations(traces):
  duration = 0
  for trace in traces:
    duration += trace['tdur']
  return duration

def findAndPrintTimers(traces, fcp, lcp, dcl):
  timers = []
  for trace in traces:
    if trace['name'] == 'TimerFire':
      timers.append(trace);
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

def recordScriptsAndtimers(traces):
  fcp = findFCP(traces)
  lcp = findLCP(traces)
  dcl = findDCL(traces)
  commit = findCommit(traces)
  print('Time from Commit to DCL: ' + str(dcl - commit) + " microseconds")
  findAndPrintScriptsAfterDCL(traces, dcl)
  findAndPrintTimers(traces, fcp, lcp, dcl)  

