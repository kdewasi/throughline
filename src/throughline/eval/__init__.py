"""Automated evaluation harness for flagging pipeline output.

Rules check a Trajectory against constraints derived from manual findings.
Each rule has a severity (error or warn); the runner aggregates results
into an EvalReport.
"""