import copy
import sys

from helpers import trace_helpers

def main():
  traces = trace_helpers.loadJSONfile()
  main_frame_traces = trace_helpers.findTracesForMainFrame(traces)
  trace_helpers.recordScriptsAndtimers(main_frame_traces)

if __name__ == "__main__":
  main()
