import copy
import sys

from helpers import trace_helpers

def main():
  trace = trace_helpers.loadJSONfile()
  main_frame_slices = trace_helpers.findSlicesForMainFrame(trace)
  trace_helpers.recordScriptsAndTimers(main_frame_slices)

if __name__ == "__main__":
  main()
