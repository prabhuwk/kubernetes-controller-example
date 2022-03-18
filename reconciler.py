#!/usr/bin/env python3
import sys
import yaml
import json

# Read current state from stdio.
state = sys.stdin
cr = yaml.safe_load(state.read())

# Reconcile object
manifest = cr.get('object')
phase = manifest.get('status',{}).get('phase', {})
if not phase or phase != 'completed':
    manifest['status'] = {}
    manifest['status']['phase'] = 'completed'

# Write new state to stdio.
state = sys.stdout
state.write(json.dumps(cr))