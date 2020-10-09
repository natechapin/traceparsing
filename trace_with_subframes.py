import copy
import sys

from helpers import trace_helpers

def main():
  trace = trace_helpers.loadJSONfile()
  trace_helpers.recordScriptsAndTimers(trace)

if __name__ == "__main__":
  main()
