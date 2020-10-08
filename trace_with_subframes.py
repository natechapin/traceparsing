import copy
import sys

from helpers import trace_helpers

def main():
  traces = trace_helpers.loadJSONfile()
  trace_helpers.recordScriptsAndtimers(traces)

if __name__ == "__main__":
  main()
